from typing import List, NamedTuple, Tuple

import torch

from .split import Layer
from .merge import MergingContext, merge_layers, merge_init, merge_next_layer


def extract_layers(layers: List[Layer]) -> Tuple[torch.Tensor, torch.Tensor]:
    '''
    Decode the layers.
    :param: layers: [layer0, layer1, ...] splitted layers
    :return: ([N, C], [K, C]) int tensor ids, float tensor cluster centers
    '''
    codes, context = merge_layers(layers)
    return context.sorted_codebook_idx[torch.searchsorted(context.sorted_codebook, codes)], context.cluster_centers


def decode_layers(layers: List[Layer]) -> torch.Tensor:
    '''
    Decode the layers.
    :param: layers: [layer0, layer1, ...] splitted layers
    :return: [N, C] float tensor
    '''
    ids, cluster_centers = extract_layers(layers)
    return cluster_centers[ids, ...]


class DecodingContext(NamedTuple):
    codes: torch.Tensor
    merging: MergingContext


def extract_layer(layer: Layer, context: DecodingContext = None) -> Tuple[torch.Tensor, torch.Tensor, DecodingContext]:
    '''
    Decode the layers.
    :param: layers: [layer0, layer1, ...] splitted layers
    :return: the decode result ([N, C] int tensor ids, [K, C] float tensor cluster centers) and the new context
    '''
    if context is None:
        codes, merging = merge_init(layer)
    else:
        codes, merging = merge_next_layer(layer, context.codes, context.merging)
    return merging.sorted_codebook_idx[torch.searchsorted(merging.sorted_codebook, codes)], merging.cluster_centers, DecodingContext(codes, merging)


def decode_layer(layer: Layer, context: DecodingContext = None) -> Tuple[torch.Tensor, DecodingContext]:
    '''
    Decode the layers.
    :param: layers: [layer0, layer1, ...] splitted layers
    :return: the decode result and the new context
    '''
    ids, cluster_centers, context = extract_layer(layer, context)
    return cluster_centers[ids, ...], context
