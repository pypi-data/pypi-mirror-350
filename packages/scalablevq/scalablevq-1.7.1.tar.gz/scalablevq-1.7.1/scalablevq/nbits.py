from typing import Callable, List
import torch

from scalablevq.utils import tensor_bitcount


def n_bits_proposal_by_layer_scores(n_bit_baselayer: int, n_layers: int, layer_scores: torch.Tensor) -> List[int]:
    n_bits = [n_bit_baselayer]
    layer_scores_rest = layer_scores[n_bit_baselayer:]
    layer_score_proposal = layer_scores_rest.sum() / (n_layers - 1)
    for _ in range(n_layers):
        n_bit = 1
        while n_bit < layer_scores_rest.shape[0] and layer_scores_rest[:n_bit].sum() < layer_score_proposal:
            n_bit += 1
        n_bits.append(n_bit)
        layer_scores_rest = layer_scores_rest[n_bit:]
        if layer_scores_rest.shape[0] <= 0:
            break
    return n_bits


def n_bits_proposal_balanced_clusters(n_layers: int) -> Callable[[int, torch.Tensor, torch.Tensor], List[int]]:
    def n_bits_proposal(n_bit_baselayer: int, assigned_bits: torch.Tensor, _) -> List[int]:
        total_n_clusters = tensor_bitcount(assigned_bits).bincount()[1:]
        return n_bits_proposal_by_layer_scores(n_bit_baselayer, n_layers, total_n_clusters)
    # TODO: n_bits_proposal_by_layer_scores is not 100% accurate, as the score of a merged layer is not the sum of the scores of the two layers
    return n_bits_proposal


def n_bits_proposal_balanced_values(n_layers: int) -> Callable[[int, torch.Tensor, torch.Tensor], List[int]]:
    def n_bits_proposal(n_bit_baselayer: int, assigned_bits: torch.Tensor, values: torch.Tensor) -> List[int]:
        value_n_bits = tensor_bitcount(assigned_bits[values]) - 1
        n_values = value_n_bits.bincount()[1:]
        total_n_values = torch.cumsum(n_values.flip(dims=[0]), dim=0).flip(dims=[0])
        return n_bits_proposal_by_layer_scores(n_bit_baselayer, n_layers, total_n_values)
    return n_bits_proposal
