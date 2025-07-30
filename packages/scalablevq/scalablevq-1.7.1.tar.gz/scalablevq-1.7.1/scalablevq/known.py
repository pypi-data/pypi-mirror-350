from typing import List

import torch

from .split import Layer, split_code
from .merge import merge_codebook


def match_cluster_centers(cluster_centers_ref: torch.Tensor, cluster_centers: torch.Tensor) -> torch.Tensor:
    '''
    Match the cluster centers to the reference.
    :param cluster_centers_ref: [K, C] float tensor, the reference cluster centers
    :param cluster_centers: [K, C] float tensor, the cluster centers to be matched
    :return: [K,] int tensor, the matched index
    '''
    assert cluster_centers_ref.shape == cluster_centers.shape
    return torch.argmin(torch.cdist(cluster_centers, cluster_centers_ref), dim=1)


def encode_known_layers(quantized_data: torch.Tensor, cluster_centers: torch.Tensor, layers: List[Layer]) -> List[Layer]:
    context = merge_codebook(layers)
    transcode = match_cluster_centers(context.cluster_centers, cluster_centers)
    codes = context.codebook[transcode[quantized_data]]
    code_layers = split_code(codes, n_bits=[layer.n_bit for layer in layers])
    return [layer._replace(codes=codes) for layer, codes in zip(layers, code_layers)]
