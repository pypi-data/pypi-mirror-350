#!/usr/bin/env python3

import networkx as nx
from spatial_centrality import d_centrality

def test_d_centrality():
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2)])
    linear_order = [0, 1, 2]
    scores = d_centrality(G, linear_order)
    assert isinstance(scores, dict)
    assert all(isinstance(v, float) or isinstance(v, int) for v in scores.values())
