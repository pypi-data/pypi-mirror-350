from typing import Callable, Dict, Tuple, Union
import logging
import os
import torch
from jaxtyping import Float
from transformers import AutoModel, AutoTokenizer
from transformer_lens.ActivationCache import ActivationCache
from transformer_lens.hook_points import HookedRootModule
import transformer_lens.utils as utils
from mechir.modelling.patched import PatchedMixin
from mechir.modelling.sae import SAEMixin
from mechir.modelling.hooked.loading_from_pretrained import get_official_model_name
from mechir.util import batched_dot_product, linear_rank_function
from mechir.modelling.architectures import HookedEncoder

logger = logging.getLogger(__name__)

POOLING = {
    "cls": lambda x: x[:, 0, :],
    "mean": lambda x: x.mean(dim=1),
}


class Dot(HookedRootModule, PatchedMixin, SAEMixin):
    def __init__(
        self,
        model_name_or_path: str,
        pooling_type: str = "cls",
        tokenizer=None,
        special_token: str = "a",
        return_cache: bool = False,
    ) -> None:
        super().__init__()
        self.tokenizer = (
            AutoTokenizer.from_pretrained(model_name_or_path)
            if tokenizer is None
            else tokenizer
        )
        self.special_token = special_token
        torch.set_grad_enabled(False)
        self._device = utils.get_device()
        self.model_name_or_path = get_official_model_name(model_name_or_path)
        self.__hf_model = (
            AutoModel.from_pretrained(model_name_or_path).eval().to(self._device)
        )
        self._model = HookedEncoder.from_pretrained(
            self.model_name_or_path, device=self._device, hf_model=self.__hf_model
        )

        self._pooling_type = pooling_type
        self._pooling = POOLING[pooling_type]
        self._return_cache = return_cache

        self.setup()

    def forward(
        self,
        input_ids: Float[torch.Tensor, "batch seq"],
        attention_mask: Float[torch.Tensor, "batch seq"],
        token_type_ids: Float[torch.Tensor, "batch seq"] = None,
    ):
        model_output = self._model(
            input=input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            return_type="embeddings",
        )
        return self._pooling(model_output)

    def get_act_patch_block_every(
        self,
        corrupted_tokens: Float[torch.Tensor, "batch pos"],
        clean_cache: ActivationCache,
        reps_q: Float[torch.Tensor, "batch pos model"],
        patching_metric: Callable[[Float[torch.Tensor, "batch pos d_vocab"]], float],
        scores: Float[torch.Tensor, "batch pos"],
        scores_p: Float[torch.Tensor, "batch pos"],
        **kwargs,
    ) -> Float[torch.Tensor, "3 layer pos"]:
        """
        Returns an array of results of patching each position at each layer in the residual
        stream, using the value from the clean cache.

        The results are calculated using the patching_metric function, which should be
        called on the model's logit output.
        """

        _, seq_len = corrupted_tokens["input_ids"].size()
        results = torch.zeros(
            3,
            self._model.cfg.n_layers,
            seq_len,
            device=self._device,
            dtype=torch.float32,
        )

        for index, output in self._get_act_patch_block_every(
            corrupted_tokens=corrupted_tokens, clean_cache=clean_cache
        ):
            output = batched_dot_product(reps_q, output)
            results[index] = patching_metric(output, scores, scores_p).mean()

        return results

    def get_act_patch_attn_head_out_all_pos(
        self,
        corrupted_tokens: Float[torch.Tensor, "batch pos"],
        clean_cache: ActivationCache,
        reps_q: Float[torch.Tensor, "batch pos model"],
        patching_metric: Callable,
        scores: Float[torch.Tensor, "batch pos"],
        scores_p: Float[torch.Tensor, "batch pos"],
        **kwargs,
    ) -> Float[torch.Tensor, "layer head"]:
        """
        Returns an array of results of patching at all positions for each head in each
        layer, using the value from the clean cache.

        The results are calculated using the patching_metric function, which should be
        called on the model's embedding output.
        """

        results = torch.zeros(
            self._model.cfg.n_layers,
            self._model.cfg.n_heads,
            device=self._device,
            dtype=torch.float32,
        )

        for index, output in self._get_act_patch_attn_head_out_all_pos(
            corrupted_tokens=corrupted_tokens, clean_cache=clean_cache
        ):
            output = batched_dot_product(reps_q, output)
            results[index] = patching_metric(output, scores, scores_p).mean()

        return results

    def get_act_patch_attn_head_by_pos(
        self,
        corrupted_tokens: Float[torch.Tensor, "batch pos"],
        reps_q: Float[torch.Tensor, "batch pos model"],
        clean_cache: ActivationCache,
        layer_head_list,
        patching_metric: Callable,
        scores: Float[torch.Tensor, "batch pos"],
        scores_p: Float[torch.Tensor, "batch pos"],
        **kwargs,
    ) -> Float[torch.Tensor, "layer pos head"]:

        _, seq_len = corrupted_tokens["input_ids"].size()
        results = torch.zeros(
            2, len(layer_head_list), seq_len, device=self._device, dtype=torch.float32
        )

        for index, output in self._get_act_patch_attn_head_by_pos(
            corrupted_tokens=corrupted_tokens,
            clean_cache=clean_cache,
            layer_head_list=layer_head_list,
        ):
            output = batched_dot_product(reps_q, output)
            results[index] = patching_metric(output, scores, scores_p).mean()

        return results
    
    def run_with_cache(
        self,
        *model_args,
        return_cache_object: bool = True,
        cache_as_dict: bool = False,
        remove_batch_dim: bool = False,
        **kwargs,
    ) -> Tuple[
        Float[torch.Tensor, "batch pos d_vocab"],
        Union[ActivationCache, Dict[str, torch.Tensor]],
    ]:
        """
        Wrapper around run_with_cache in HookedRootModule. If return_cache_object is True, this will return an ActivationCache object, with a bunch of useful HookedTransformer specific methods, otherwise it will return a dictionary of activations as in HookedRootModule. This function was copied directly from HookedTransformer.
        """
        out, cache_dict = super().run_with_cache(
            *model_args, remove_batch_dim=remove_batch_dim, **kwargs
        )
        if return_cache_object:
            if not cache_as_dict:
                cache = ActivationCache(
                    cache_dict, self, has_batch_dim=not remove_batch_dim
                )
            return out, cache
        else:
            return out, None

    def score(self, queries: dict, documents: dict, reps_q=None, cache=False, cache_as_dict=False):
        if reps_q is None:
            reps_q = self.forward(queries["input_ids"], queries["attention_mask"])
        if cache:
            reps_d, cache_d = self.run_with_cache(
                documents["input_ids"], documents["attention_mask"], cache_as_dict=cache_as_dict
            )
            return batched_dot_product(reps_q, reps_d), reps_q, reps_d, cache_d
        reps_d = self.forward(documents["input_ids"], documents["attention_mask"])
        return batched_dot_product(reps_q, reps_d), reps_q, reps_d, None

    def patch(
        self,
        queries: dict,
        documents: dict,
        documents_p: dict,
        patch_type: str = "block_all",
        layer_head_list: list = [],
        patching_metric: Callable = linear_rank_function,
    ):
        assert (
            patch_type in self._patch_funcs
        ), f"Patch type {patch_type} not recognized. Choose from {self._patch_funcs.keys()}"
        scores, reps_q, _, _ = self.score(queries, documents)
        scores_p, _, _, cache_d = self.score(
            queries, documents_p, cache=True, reps_q=reps_q
        )

        patching_kwargs = {
            "corrupted_tokens": documents,
            "clean_cache": cache_d,
            "reps_q": reps_q,
            "patching_metric": patching_metric,
            "layer_head_list": layer_head_list,
            "scores": scores,
            "scores_p": scores_p,
        }

        patched_output = self._patch_funcs[patch_type](**patching_kwargs)
        if self._return_cache:
            return patched_output, cache_d
        return patched_output, None  # PatchingOutput(output, scores, scores_p)
