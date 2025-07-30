import torch
import numpy as np


def bitcount(a: int):
    max_n_bits = int(np.ceil(np.log2(a)))
    counts = 0
    for i in range(0, max_n_bits):
        counts += 1 if (a >> i) > 0 else 0
    return counts


def tensor_bitcount(a: torch.Tensor):
    max_n_bits = int(torch.ceil(torch.log2(a.max())))
    counts = torch.zeros_like(a)
    for i in range(0, max_n_bits):
        counts[(a >> i) > 0] += 1
    return counts
