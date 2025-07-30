from typing import List, Tuple
import numpy as np
from .utils import bitcount


def assign_bits(tree: List[Tuple[int, int]], n_clusters: int):
    n_clusters_init = n_clusters - len(tree)
    assigned = [[] for _ in range(n_clusters)]
    top = [True]*n_clusters

    def append_higherbits_until_leaf(k, bits):
        assigned[k] = bits + assigned[k]
        if k < n_clusters_init:
            return
        append_higherbits_until_leaf(tree[k-n_clusters_init][0], bits)
        append_higherbits_until_leaf(tree[k-n_clusters_init][1], bits)

    for l, r in tree:
        append_higherbits_until_leaf(l, [0])
        append_higherbits_until_leaf(r, [1])
        top[l] = top[r] = False

    top_idx, = np.where(top)
    lod0_bitwidth = bitcount(len(top_idx))
    for b, j in enumerate(top_idx):
        append_higherbits_until_leaf(j, [int(bit) for bit in format(b, f'0{lod0_bitwidth}b')])
    assigned_bits = [eval('0b' + ''.join([str(1)] + [str(bit) for bit in bits])) for bits in assigned]  # 1 on the hightest bit
    return assigned_bits
