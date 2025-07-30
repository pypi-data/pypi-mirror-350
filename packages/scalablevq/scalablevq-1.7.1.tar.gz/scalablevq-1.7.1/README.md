# ScalableVQ: Scalable Vector Quantization

## Project Overview

This project implements scalable vector quantization.
It construct hierarchical structures through merging clusters and assign bits to these cluster centers, providing scalability in data representation.

"Scalability" refers to the encoded data being partitioned into a base layer and multiple enhancement layers.
Decoding begins from the base layer, with each additional enhancement layer improving the fidelity of the reconstructed data.

>💡 This project itself does not perform vector quantization. The accuracy achieved depends on the vector quantization method you choose.

## Structure
- [`scalablevq`](./scalablevq): Core package containing modules for hierarchical clustering, bit assignment, splitting and merging codes, and data encoding/decoding.
- [`example.py`](./example.py): Illustrates clustering, encoding, and decoding processes using the library's main functionalities.

## Key Features

### Encoding

1. **Hierarchical Clustering**: Iteratively merges clusters to form a hierarchical cluster tree.
2. **Bit assign**: Allocates bits to clusters within the hierarchy.
3. **Splitting/Encoding**: Partitions quantized data and codebook into several layers based on the cluster hierarchy and assigned bits.

### Decoding
1. **Merging**: Combines the encoded layers to reconstruct quantized data and the associated codebook.
2. **Decoding**: Converts quantized data back to approximate the original data using the reconstructed codebook.

## Install

Install from pypi:
```sh
pip install scalablevq
```
or from source:
```sh
pip install git+https://github.com/yindaheng98/ScalableVQ
```

## Example Usage

>💡 Refer to [`example.py`](./example.py) for a complete example.

Before using this library, perform vector quantization using your preferred method (e.g. K-Means from `sklearn`):
```python
data = ... # your data, shape [N, C]
from sklearn.cluster import MiniBatchKMeans as KMeans
kmeans = KMeans(n_clusters=1024, init='random', random_state=0, n_init="auto")
quantized_data = torch.from_numpy(kmeans.fit_predict(data.cpu()))
cluster_centers = torch.from_numpy(kmeans.cluster_centers_)
```

Encoding:
```python
from scalablevq import encode_layers
n_bits_proposal = [4, 2, 2, 2, 2]
layers = encode_layers(data, quantized_data, cluster_centers, n_bits_proposal)
```

Decoding:
```python
from scalablevq import decode_layer
context = None
for layer in layers:
    decoded, context = decode_layer(layer, context)
```

Visualizztion:
```python
layerized_cluster_centers, cluster_tree = build_layers(cluster_centers, data, quantized_data, final_clusters=2**n_bits_proposal[0])
visualize_layers(cluster_centers.cpu(), layerized_cluster_centers.cpu(), cluster_tree, data=None)
```

>💡 Use GPU acceleration if possible, as large-scale clustering can be compute-intensive.

## Dependencies
- PyTorch  
- NumPy  
- tqdm
- scikit-learn (optional, for [`example.py`](./example.py))
- open3d (optional, for visualization)
