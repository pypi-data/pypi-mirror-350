from typing import List, NamedTuple, Tuple

import torch

from .utils import tensor_bitcount


def split_code(codes: torch.Tensor, n_bits: List[int] = [4, 4, 4]) -> List[torch.Tensor]:
    '''
    Split the encoded codes into multiple chunks.
    :param codes: [N,] int tensor, the codes to be split
    :param n_bits: [n1, n2, n3] int list, the number of code bits for each chunks
    :return: [chunk1, chunk2, ...] each chunk is a 1-dim int tensor
    '''
    chunks = []
    rest_codes = codes.clone()
    bitlength = tensor_bitcount(rest_codes) - 1
    for i in range(len(n_bits)):
        n_bit = n_bits[i]
        end_bit = sum(n_bits[:i + 1])
        n_clip_bit = bitlength - end_bit
        cliped_rest_codes = rest_codes >> n_clip_bit
        cliped_rest_codes[n_clip_bit < 0] = rest_codes[n_clip_bit < 0] << -n_clip_bit[n_clip_bit < 0]
        chunk = cliped_rest_codes & ((1 << n_bit) - 1)  # split out 1 layer
        done_mask = n_clip_bit <= 0
        rest_codes = rest_codes[~done_mask]  # collect rest codes
        bitlength = bitlength[~done_mask]
        chunks.append(chunk)
    return chunks


def format_leaf(codebook_leaf: torch.Tensor, n_bits: List[int]) -> torch.Tensor:
    bitlength = tensor_bitcount(codebook_leaf) - 1
    for i in range(len(n_bits)):
        end_bit = sum(n_bits[:i + 1])
        n_clip_bit = bitlength - end_bit
        move_idx = (n_clip_bit < 0) & (n_clip_bit > -n_bits[i])
        codebook_leaf[move_idx] = codebook_leaf[move_idx] << -n_clip_bit[move_idx]
    return codebook_leaf


def reverse_codebook(codebook: torch.Tensor) -> torch.Tensor:
    reversed_codebook = torch.zeros(codebook.max() + 1, dtype=codebook.dtype, device=codebook.device) + len(codebook)
    reversed_codebook[codebook] = torch.arange(len(codebook), dtype=codebook.dtype, device=codebook.device)
    return reversed_codebook


def split_codebook(codebook: torch.Tensor, leaf_idx: torch.Tensor, cluster_centers: torch.Tensor, n_bits: List[int] = [4, 4, 4]) -> List[Tuple[torch.Tensor, torch.Tensor]]:
    '''
    Split the codebook for multiple chunks.
    :param codebook: [N,] int tensor, all the codes
    :param leaf_idx: [M,] int tensor, identify the index of leaf codes in the codebook
    :param cluster_centers: [N, C] cluster centers with the same order as codebook
    :param n_bits: [n1, n2, n3] int list, the number of code bits for each chunks
    :return: [(codebook1, cluster_centers1, n_leaf1), (cb2, cc2, nl2), (cb3, cc3, nl3), ...] each chunk is a 1-dim int tensor
    '''
    codebook_leaf = format_leaf(codebook[leaf_idx], n_bits)
    codebook = codebook.clone()
    codebook[leaf_idx] = codebook_leaf
    sorted_codebook, sorted_idx = codebook.sort()
    is_leaf = torch.zeros(codebook.shape[0], dtype=torch.bool, device=codebook.device)
    is_leaf[leaf_idx] = True

    bitlength = tensor_bitcount(codebook_leaf) - 1
    chunks = []
    for i in range(len(n_bits)):
        end_bit = sum(n_bits[:i + 1])
        n_clip_bit = bitlength - end_bit
        chunk = codebook_leaf >> n_clip_bit
        codebook_layer = chunk.unique()

        is_leaf_layer = is_leaf[sorted_idx[torch.searchsorted(sorted_codebook, codebook_layer)]]
        codebook_layer = torch.cat([codebook_layer[is_leaf_layer], codebook_layer[~is_leaf_layer]])
        n_leaf = is_leaf_layer.sum().item()  # put non-leaf codes in the end, convenient for merging when decoding
        cluster_centers_layer = cluster_centers[sorted_idx[torch.searchsorted(sorted_codebook, codebook_layer)], ...]

        chunks.append((codebook_layer, cluster_centers_layer, n_leaf))

        done_mask = n_clip_bit <= 0
        codebook_leaf = codebook_leaf[~done_mask]
        bitlength = bitlength[~done_mask]
    assert codebook_leaf.shape[0] == 0
    return chunks


class Layer(NamedTuple):
    codes: torch.Tensor  # [N,] int tensor, code.max() < K
    codebook: torch.Tensor  # [K,] int tensor
    cluster_centers: torch.Tensor  # [K, C] float tensor, with the same order as codebook
    n_bit: int  # the number of code bits for this layer
    n_leaf: int  # the number of leaf codes for this layer, codebook[:n_leaf] are leaf codes


def split_layers(codes: torch.Tensor, codebook: torch.Tensor, leaf_idx: torch.Tensor, cluster_centers: torch.Tensor, n_bits: List[int] = [4, 4, 4]) -> List[Layer]:
    '''
    Split the encoded codes and codebook into multiple layers.
    :param codes: [N,] int tensor, the codes to be split
    :param codebook: [N,] int tensor, all the codes
    :param leaf_idx: [M,] int tensor, identify the index of leaf codes in the codebook
    :param cluster_centers: [N, C] cluster centers with the same order as codebook
    :param n_bits: [n1, n2, n3] int list, the number of code bits for each chunks
    :return: [layer0, layer1, ...] splitted layers
    '''
    code_layers = split_code(codes, n_bits)
    codebook_layers = split_codebook(codebook, leaf_idx, cluster_centers, n_bits)
    return [Layer(code, codebook, cluster_centers, n_bit, n_leaf) for code, (codebook, cluster_centers, n_leaf), n_bit in zip(code_layers, codebook_layers, n_bits)]
