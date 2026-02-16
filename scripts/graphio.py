from __future__ import annotations
from typing import Dict, List, Tuple

def read_edgelist(path: str) -> Tuple[List[int], List[Tuple[int,int]]]:
    edges = []
    nodes_set = set()
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            a, b, *_ = line.split()
            u = int(a); v = int(b)
            if u == v:
                continue
            if u > v:
                u, v = v, u
            edges.append((u, v))
            nodes_set.add(u); nodes_set.add(v)
    nodes = sorted(nodes_set)
    return nodes, edges

def build_adj(nodes: List[int], edges: List[Tuple[int,int]]) -> Tuple[Dict[int,int], List[List[int]]]:
    idx = {u:i for i,u in enumerate(nodes)}
    n = len(nodes)
    adj = [[] for _ in range(n)]
    for (u,v) in edges:
        iu = idx[u]; iv = idx[v]
        adj[iu].append(iv)
        adj[iv].append(iu)
    for i in range(n):
        adj[i].sort()
    return idx, adj

def has_edge(adj: List[List[int]], i: int, j: int) -> int:
    # adj lists are sorted; binary search
    lo, hi = 0, len(adj[i])
    while lo < hi:
        mid = (lo + hi)//2
        x = adj[i][mid]
        if x == j:
            return 1
        if x < j:
            lo = mid + 1
        else:
            hi = mid
    return 0
