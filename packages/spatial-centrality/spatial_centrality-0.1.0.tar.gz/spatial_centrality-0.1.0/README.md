# spatial_centrality

This package provides spatial centrality scores (`D`, `coverage`, and `D'`) for syntactic dependency trees, as introduced in this publication:

> Ferrer-i-Cancho, R., & Arias, M. (2025). *Who is the root in a syntactic dependency structure?* [arXiv:2501.15188](https://arxiv.org/abs/2501.15188)

The scores are designed for use with undirected syntactic dependency trees, combined with the linear order of words in a sentence. These measures help identify the root of a dependency tree using spatial and topological information.

**This package is an independent implementation** based on the algorithms described in the paper. All credit for the concepts and theoretical work goes to the original authors. This implementation is provided under an open-source license to facilitate use and experimentation by the NLP and computational linguistics community.

## Installation

```bash
pip install .
```

## Usage

```python
import networkx as nx
from spatial_centrality import d_centrality, coverage_centrality, d_prime_centrality

# Create an undirected syntactic dependency tree
G = nx.Graph()
G.add_edges_from([(0, 1), (1, 2), (1, 3)])  # edges represent syntactic relations

# Define the linear order of words in the sentence
linear_order = [0, 1, 2, 3]  # e.g., token indices from left to right

# Compute scores
print(d_centrality(G, linear_order))
print(coverage_centrality(G, linear_order))
print(d_prime_centrality(G, linear_order))
```

## License

MIT License

---

If you use this package in academic work, please cite the original paper and feel free to mention this implementation in your acknowledgments or supplementary materials.
