
from typing import Dict, List
import networkx as nx

def _get_positions(linear_order: List[int]) -> Dict[int, int]:
    return {node: idx for idx, node in enumerate(linear_order)}

def _linear_distance(pos: Dict[int, int], u: int, v: int) -> int:
    return abs(pos[u] - pos[v])

def d_centrality(G: nx.Graph, linear_order: List[int]) -> Dict[int, float]:
    pos = _get_positions(linear_order)
    return {
        v: sum(_linear_distance(pos, v, u) for u in G.neighbors(v))
        for v in G.nodes
    }

def coverage_centrality(G: nx.Graph, linear_order: List[int]) -> Dict[int, int]:
    pos = _get_positions(linear_order)
    return {
        v: max([pos[u] for u in [v] + list(G.neighbors(v))]) -
           min([pos[u] for u in [v] + list(G.neighbors(v))])
        for v in G.nodes
    }

def d_prime_centrality(G: nx.Graph, linear_order: List[int]) -> Dict[int, float]:
    pos = _get_positions(linear_order)
    n = len(linear_order)
    d_scores = d_centrality(G, linear_order)
    c_scores = coverage_centrality(G, linear_order)
    return {
        v: (c_scores[v] / (n - 1)) * d_scores[v] if n > 1 else 0.0
        for v in G.nodes
    }
