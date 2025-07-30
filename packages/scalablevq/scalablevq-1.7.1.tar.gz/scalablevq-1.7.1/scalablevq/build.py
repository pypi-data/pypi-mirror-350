from typing import List, Tuple, Callable
import torch
import tqdm
import math


def split_into_clusters(n_clusters: int, data: torch.Tensor, quantized_data: torch.Tensor):
    """Split the data into clusters"""
    clusters = [None]*n_clusters
    for i in tqdm.tqdm(range(n_clusters), desc="Split data into clusters"):
        clusters[i] = data[quantized_data == i, ...]
    return clusters


def knn_cluster_centers(cluster_centers: torch.Tensor, n=2, batch=2**16):
    """Get k neighbor points for each point."""
    neighbors_idx = torch.zeros(cluster_centers.shape[0], n, dtype=torch.int64, device=cluster_centers.device)
    progress_bar = tqdm.tqdm(range(cluster_centers.shape[0]), desc="Init K-Nearest for cluster centers")
    dists = torch.zeros(cluster_centers.shape[0], n, dtype=cluster_centers.dtype, device=cluster_centers.device)
    for i in range(math.ceil(cluster_centers.shape[0]/batch)):
        dist = torch.norm(cluster_centers[i*batch:i*batch+batch, ...].unsqueeze(-2) - cluster_centers, p=2, dim=-1)
        knn = dist.topk(n + 1, largest=False)
        dists[i*batch:i*batch+batch, ...] = knn.values[:, 1:]
        neighbors_idx[i*batch:i*batch+batch, ...] = knn.indices[:, 1:]
        progress_bar.update(min(i*batch+batch, cluster_centers.shape[0])-i*batch)
    return neighbors_idx, dists


def merged_cluster(a: torch.Tensor, b: torch.Tensor):
    ab = torch.cat([a, b], dim=0)
    center = ab.mean(dim=0, keepdim=True)
    return ab, center


def vdistance(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
    """Virtual distance for quant cluster_tree. Just the avg distance from center to points after merge."""
    ab, center = merged_cluster(a, b)
    dist = torch.norm(ab-center, dim=1, p=2).mean()
    return dist


def distance_init(clusters: List[torch.Tensor], cluster_centers: torch.Tensor, neighbors_idx: torch.Tensor,
                  dist_func: Callable[[torch.Tensor, torch.Tensor], torch.Tensor] = vdistance):
    """Calculate the virtual distance between the point and their k neighbor points"""
    dists = torch.zeros(neighbors_idx.shape, dtype=cluster_centers.dtype, device=cluster_centers.device)
    for center_idx in tqdm.tqdm(range(cluster_centers.shape[0]), desc="Compute 'distance' among K-Nearest"):
        data_dequant = clusters[center_idx]
        for i, neighbor_idx in enumerate(neighbors_idx[center_idx, ...]):
            data_neighbor_dequant = clusters[neighbor_idx]
            dists[center_idx, i] = dist_func(data_dequant, data_neighbor_dequant)
    return dists


def merge(
    layerized_cluster_centers: torch.Tensor, cluster_tree: List[Tuple[int, int]],
    clusters: List[torch.Tensor], dists: torch.Tensor,
    tmp_cluster_centers: torch.Tensor, tmp_neighbors_idx: torch.Tensor,
    tmp_depth: torch.Tensor, depth_limit: int = 63,
    dist_func: Callable[[torch.Tensor, torch.Tensor], torch.Tensor] = vdistance
):
    """Merge the clusters and dists, and expand layerized_cluster_centers"""
    min_pos = (dists == dists.min()).nonzero()[0]
    min_idx, min_neighbors_idx = min_pos[0].item(), tmp_neighbors_idx[*min_pos].item()
    # concat to get new cluster and center
    new_cluster, new_center = merged_cluster(clusters[min_idx], clusters[min_neighbors_idx])
    new_depth = max(tmp_depth[min_idx], tmp_depth[min_neighbors_idx]) + 1
    # add new cluster
    new_center_idx = len(clusters)
    clusters.append(None)
    clusters[new_center_idx] = new_cluster if new_depth < depth_limit else None  # control the tree depth
    # delete old clusters
    clusters[min_idx] = clusters[min_neighbors_idx] = None
    # add new center
    tmp_cluster_centers = torch.cat([tmp_cluster_centers, new_center], dim=0)
    tmp_cluster_centers[-1, ...] = new_center if new_depth < depth_limit else torch.inf  # control the tree depth
    tmp_depth = torch.cat([tmp_depth, torch.tensor([new_depth], device=tmp_depth.device)], dim=0)
    layerized_cluster_centers = torch.cat([layerized_cluster_centers, new_center], dim=0)  # save result
    cluster_tree.append((min_idx, min_neighbors_idx))  # save result
    # delete old center
    tmp_cluster_centers[min_idx, ...] = torch.inf
    tmp_cluster_centers[min_neighbors_idx, ...] = torch.inf
    # which center should be updated
    should_update_idx = torch.logical_or(
        tmp_neighbors_idx == min_idx,
        tmp_neighbors_idx == min_neighbors_idx
    ).any(dim=1).nonzero()[..., 0]
    should_update_idx = should_update_idx[torch.logical_and(
        should_update_idx != min_idx, should_update_idx != min_neighbors_idx
    )]
    should_update_idx = torch.cat([
        should_update_idx,
        torch.tensor([new_center_idx], dtype=should_update_idx.dtype, device=should_update_idx.device)
    ], dim=0)
    # compute new neighbors idx
    new_kdist = torch.norm(tmp_cluster_centers[should_update_idx, ...].unsqueeze(-2) - tmp_cluster_centers, p=2, dim=-1)
    new_knn = new_kdist.topk(dists.shape[1] + 1, largest=False)
    # update neighbors idx
    tmp_neighbors_idx = torch.cat([tmp_neighbors_idx, torch.zeros_like(tmp_neighbors_idx[0:1, ...])], dim=0)
    tmp_neighbors_idx[should_update_idx, ...] = new_knn.indices[:, 1:]
    # update neighbors distance
    dists = torch.cat([dists, torch.zeros_like(dists[0:1, ...])], dim=0)
    for center_idx in tqdm.tqdm(should_update_idx, desc="Updating distance", position=1, leave=False):
        center_data = clusters[center_idx]
        for i, neighbor_idx in enumerate(tmp_neighbors_idx[center_idx, ...]):
            neighbor_data = clusters[neighbor_idx]
            if center_data is not None and neighbor_data is not None:
                dists[center_idx, i] = dist_func(center_data, neighbor_data)
            else:
                dists[center_idx, i] = torch.inf
    dists[min_idx, ...] = torch.inf
    dists[min_neighbors_idx, ...] = torch.inf
    return layerized_cluster_centers, cluster_tree, clusters, dists, tmp_cluster_centers, tmp_neighbors_idx, tmp_depth


def build_layers(cluster_centers: torch.Tensor, data: torch.Tensor, quantized_data: torch.Tensor, final_clusters: int, depth_limit=63,
                 dist_func: Callable[[torch.Tensor, torch.Tensor], torch.Tensor] = vdistance):
    clusters = split_into_clusters(cluster_centers.shape[0], data, quantized_data)
    neighbors_idx, _ = knn_cluster_centers(cluster_centers)
    dists = distance_init(clusters, cluster_centers, neighbors_idx, dist_func=dist_func).to(data.device)
    layerized_cluster_centers = cluster_centers.clone()
    cluster_tree = []
    tmp_cluster_centers = cluster_centers.clone()
    tmp_neighbors_idx = neighbors_idx.clone()
    tmp_depth = torch.ones(cluster_centers.shape[0], dtype=torch.int, device=cluster_centers.device)
    context = (layerized_cluster_centers, cluster_tree, clusters, dists, tmp_cluster_centers, tmp_neighbors_idx, tmp_depth)
    for _ in tqdm.tqdm(range(len(clusters)-final_clusters), desc="Merging clusters", position=0, leave=False):
        context = merge(*context, depth_limit=depth_limit, dist_func=dist_func)
        torch.cuda.empty_cache()
    (layerized_cluster_centers, cluster_tree, clusters, dists, tmp_cluster_centers, tmp_neighbors_idx, tmp_depth) = context
    return layerized_cluster_centers, cluster_tree
