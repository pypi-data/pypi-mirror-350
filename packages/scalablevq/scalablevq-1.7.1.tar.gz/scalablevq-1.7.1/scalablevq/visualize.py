from typing import List, Tuple
import open3d as o3d
import matplotlib
import numpy as np
import torch


def build_geometries(cluster_centers: torch.Tensor, layerized_cluster_centers: torch.Tensor, cluster_tree: List[Tuple[int, int]]):
    pcd_cluster_centers = o3d.geometry.PointCloud()
    pcd_cluster_centers.points = o3d.utility.Vector3dVector(cluster_centers.cpu())
    pcd_cluster_centers.colors = o3d.utility.Vector3dVector(np.array([[0, 0, 0]]*cluster_centers.shape[0]))

    leaf_n = cluster_centers.shape[0]
    lines = [(i+leaf_n, t[0]) for i, t in enumerate(cluster_tree)] + [(i+leaf_n, t[1]) for i, t in enumerate(cluster_tree)]
    line_set_layerized_cluster_centers = o3d.geometry.LineSet(
        points=o3d.utility.Vector3dVector(layerized_cluster_centers.cpu()),
        lines=o3d.utility.Vector2iVector(lines),
    )

    mat = o3d.visualization.rendering.MaterialRecord()
    mat.point_size = 5.0
    geometries = [
        {'name': 'cluster centers', 'geometry': pcd_cluster_centers, 'material': mat},
        {'name': 'layers', 'geometry': line_set_layerized_cluster_centers},
    ]
    return geometries


def build_clusters(data: torch.Tensor, quantized_data: torch.Tensor):
    geometries = []
    ids = quantized_data.unique()
    cmap = matplotlib.cm.get_cmap('rainbow')(np.linspace(0, 1, ids.shape[0]))
    for i in range(ids.shape[0]):
        cluster = data[quantized_data == ids[i], ...]
        pcd_cluster = o3d.geometry.PointCloud()
        pcd_cluster.points = o3d.utility.Vector3dVector(cluster.cpu())
        mat = o3d.visualization.rendering.MaterialRecord()
        mat.shader = 'defaultLitTransparency'
        mat.base_color = cmap[i, :3].tolist() + [0.8]
        mat.point_size = 1.0
        geometries.append({'name': f'cluster {i}', 'geometry': pcd_cluster, 'material': mat})
    return geometries


def visualize_layers(cluster_centers: torch.Tensor, layerized_cluster_centers: torch.Tensor, cluster_tree: List[Tuple[int, int]], data: torch.Tensor, quantized_data: torch.Tensor):
    o3d.visualization.draw(build_geometries(cluster_centers, layerized_cluster_centers, cluster_tree) + build_clusters(data, quantized_data))
