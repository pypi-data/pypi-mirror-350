from typing import List, Tuple, NamedTuple

import torch

from .split import Layer


class MergingContext(NamedTuple):
    codebook: torch.Tensor  # [K,] int tensor
    cluster_centers: torch.Tensor  # [K, C] float tensor, with the same order as codebook
    n_leaf: int  # the number of leaf codes for this layer, codebook[:n_leaf] are leaf codes

    sorted_codebook: torch.Tensor
    sorted_codebook_idx: torch.Tensor


def construct_context(codebook: torch.Tensor, cluster_centers: torch.Tensor, n_leaf: int) -> MergingContext:
    sorted_codebook, sorted_idx = codebook.sort()
    return MergingContext(codebook, cluster_centers, n_leaf, sorted_codebook, sorted_idx)


def init_codebook(layer: Layer) -> MergingContext:
    return construct_context(layer.codebook, layer.cluster_centers, layer.n_leaf)


def append_codebook(layer: Layer, context: MergingContext) -> MergingContext:
    codebook = torch.cat([context.codebook[:context.n_leaf], layer.codebook])
    cluster_centers = torch.cat([context.cluster_centers[:context.n_leaf], layer.cluster_centers])
    n_leaf = context.n_leaf + layer.n_leaf
    return construct_context(codebook, cluster_centers, n_leaf)


def merge_init(layer: Layer) -> Tuple[torch.Tensor, MergingContext]:
    '''
    Init the merging by the lowest layer.
    :param layer: the lowest layer.
    :return: the codes and the context.
    '''
    codes = layer.codes + (1 << layer.n_bit)
    context = init_codebook(layer)
    return codes, context


def merge_next_layer(layer: Layer, codes: torch.Tensor, context: MergingContext) -> Tuple[torch.Tensor, MergingContext]:
    '''
    Merging the next layer.
    :param layer: the next layer.
    :param codes: the current codes.
    :param context: the current context.
    :return: the new codes and the new context.
    '''
    is_leaf = context.sorted_codebook_idx[torch.searchsorted(context.sorted_codebook, codes)] < context.n_leaf
    codes[~is_leaf] = (codes[~is_leaf] << layer.n_bit) + layer.codes
    context = append_codebook(layer, context)
    return codes, context


def merge_layers(layers: List[Layer]) -> Tuple[torch.Tensor, MergingContext]:
    '''
    Merge multiple layers.
    :param: layers: [layer0, layer1, ...] splitted layers
    :return: the codes and the context.
    '''
    codes, context = merge_init(layers[0])
    for layer in layers[1:]:
        codes, context = merge_next_layer(layer, codes, context)
    return codes, context


def merge_codebook(layers: List[Layer]) -> MergingContext:
    '''
    Merge only the codebook.
    :param: layers: [layer0, layer1, ...] splitted layers
    :return: the context.
    '''
    context = init_codebook(layers[0])
    for layer in layers[1:]:
        context = append_codebook(layer, context)
    return context
