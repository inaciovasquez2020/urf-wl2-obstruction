from __future__ import annotations
import sys
from typing import Dict, List, Tuple
from graphio import read_edgelist, build_adj

EVEN_MASKS_DEG3 = (0, 3, 5, 6)  # 000,011,101,110

def edge_id(u: int, v: int) -> Tuple[int,int]:
    return (u, v) if u < v else (v, u)

def build_cfi(base_path: str, parity: int, out_path: str) -> None:
    # read base graph (assume simple undirected)
    nodes, edges = read_edgelist(base_path)
    _, adj = build_adj(nodes, edges)

    # verify 3-regular
    for i,u in enumerate(nodes):
        if len(adj[i]) != 3:
            raise SystemExit(f"ERROR: base graph not 3-regular at vertex {u} (deg={len(adj[i])})")

    # neighbor ordering per vertex in base labels (not indices)
    neigh: Dict[int, List[int]] = {}
    idx_of: Dict[int, int] = {u:i for i,u in enumerate(nodes)}
    for u in nodes:
        i = idx_of[u]
        neigh[u] = [nodes[j] for j in adj[i]]
        neigh[u].sort()

    # canonical edge list in base labels
    E = sorted({edge_id(u, v) for (u, v) in edges})

    # choose twist set with required parity: twist lexicographically smallest edge iff parity=1
    twist = set()
    if parity % 2 == 1:
        twist.add(E[0])

    # node naming -> int
    name2id: Dict[Tuple, int] = {}
    next_id = 0

    def nid(tag: Tuple) -> int:
        nonlocal next_id
        if tag not in name2id:
            name2id[tag] = next_id
            next_id += 1
        return name2id[tag]

    out_edges: List[Tuple[int,int]] = []

    def add(a: int, b: int) -> None:
        if a == b:
            return
        if a > b:
            a, b = b, a
        out_edges.append((a, b))

    # For each base vertex u:
    #   gadget nodes G(u,mask) for mask in EVEN_MASKS_DEG3
    #   connector nodes X(u,e,b) for each incident base edge e and bit b in {0,1}
    #
    # Internal connections:
    #   G(u,mask) -- X(u,e_i, bit(mask,i))
    # where e_i is the i-th incident edge in neighbor order.
    for u in nodes:
        nu = neigh[u]  # 3 neighbors sorted
        inc_edges = [edge_id(u, v) for v in nu]  # aligned with positions 0,1,2

        # create gadget nodes
        Gmask = {mask: nid(("G", u, mask)) for mask in EVEN_MASKS_DEG3}

        # create connector nodes
        X = {}
        for i, e in enumerate(inc_edges):
            X[(i,0)] = nid(("X", u, e, 0))
            X[(i,1)] = nid(("X", u, e, 1))

        # connect
        for mask in EVEN_MASKS_DEG3:
            gu = Gmask[mask]
            for i in range(3):
                bit = (mask >> i) & 1
                add(gu, X[(i, bit)])

    # Inter-vertex connections for each base edge e=(a,b):
    # Untwisted: X(a,e,0)--X(b,e,0) and X(a,e,1)--X(b,e,1)
    # Twisted:   X(a,e,0)--X(b,e,1) and X(a,e,1)--X(b,e,0)
    #
    # Need local index i at each endpoint (position in neighbor order).
    for (a, b) in E:
        e = (a, b)
        # indices at endpoints
        ia = neigh[a].index(b)
        ib = neigh[b].index(a)

        xa0 = nid(("X", a, e, 0))
        xa1 = nid(("X", a, e, 1))
        xb0 = nid(("X", b, e, 0))
        xb1 = nid(("X", b, e, 1))

        if e in twist:
            add(xa0, xb1)
            add(xa1, xb0)
        else:
            add(xa0, xb0)
            add(xa1, xb1)

    # dedup + sort
    out_edges = sorted(set(out_edges))

    # write
    with open(out_path, "w", encoding="utf-8") as f:
        for (u, v) in out_edges:
            f.write(f"{u} {v}\n")

    # quick report
    n = next_id
    m = len(out_edges)
    print(f"OK: wrote {out_path}  n={n} m={m}  twists={len(twist)} parity={parity}")

def main():
    if len(sys.argv) < 4:
        print("usage: python3 scripts/cfi.py <base.edgelist> <parity 0|1> <out.edgelist>")
        raise SystemExit(2)
    base = sys.argv[1]
    parity = int(sys.argv[2])
    outp = sys.argv[3]
    build_cfi(base, parity, outp)

if __name__ == "__main__":
    main()
