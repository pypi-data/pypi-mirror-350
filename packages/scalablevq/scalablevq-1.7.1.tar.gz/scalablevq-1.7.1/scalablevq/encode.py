import math
from typing import Callable, List

import torch

from .build import build_layers, vdistance
from .assign import assign_bits
from .utils import bitcount
from .split import Layer, split_layers


def format_n_bits(n_bits_proposal: List[int], max_n_bits) -> str:
    n_bits = []
    while n_bits_proposal and max_n_bits > 0:
        n_bit = min(n_bits_proposal[0], max_n_bits)
        n_bits_proposal = n_bits_proposal[1:]
        n_bits.append(n_bit)
        max_n_bits -= n_bit
    if max_n_bits > 0:
        n_bits.append(max_n_bits)
    return n_bits


def encode_layers(
        data: torch.Tensor, quantized_data: torch.Tensor, cluster_centers: torch.Tensor,
        n_bit_baselayer: int = 4, n_bits_proposal: int | List[int] | Callable[[int, torch.Tensor, torch.Tensor], List[int]] = [4, 4, 4],
        n_bit_limit: int = 63, dist_func=vdistance, visualize=False) -> List[Layer]:
    '''
    Encode the layers.
    :param: data: [N, C] float tensor, the origional data
    :param: quantized_data: [N] long tensor, the quantized data
    :param: cluster_centers: [K, C] float tensor, the cluster centers
    :param: n_bits_proposal: list of int, bit width proposal for each layer
    :return: [layer0, layer1, ...] splitted layers
    '''
    assert quantized_data.unique().shape[0] == cluster_centers.shape[0], "No empty cluster is allowed"
    assert 2**n_bit_baselayer < cluster_centers.shape[0], "The number of clusters should be more than 2**n_bit_baselayer"

    layerized_cluster_centers, cluster_tree = build_layers(
        cluster_centers, data, quantized_data,
        final_clusters=2**n_bit_baselayer,
        depth_limit=n_bit_limit - n_bit_baselayer,
        dist_func=dist_func)
    if visualize:
        from .visualize import visualize_layers
        visualize_layers(cluster_centers, layerized_cluster_centers, cluster_tree, data=data, quantized_data=quantized_data)
    assigned_bits = assign_bits(cluster_tree, n_clusters=layerized_cluster_centers.shape[0])
    assigned_bits = torch.tensor(assigned_bits, device=quantized_data.device)
    assigned_bits_data = assigned_bits[quantized_data]

    max_n_bits = bitcount(assigned_bits.max().item()) - 1
    if isinstance(n_bits_proposal, int):
        n_bits = format_n_bits([n_bit_baselayer] + [n_bits_proposal] * math.ceil((max_n_bits - n_bit_baselayer) / n_bits_proposal), max_n_bits)
    elif isinstance(n_bits_proposal, list):
        n_bits = format_n_bits([n_bit_baselayer] + n_bits_proposal, max_n_bits)
    else:
        n_bits = format_n_bits(n_bits_proposal(n_bit_baselayer, assigned_bits, quantized_data), max_n_bits)

    leaf_idx = torch.arange(0, cluster_centers.shape[0], dtype=assigned_bits.dtype, device=assigned_bits_data.device)
    layers = split_layers(assigned_bits_data, assigned_bits, leaf_idx, layerized_cluster_centers, n_bits=n_bits)
    return layers
