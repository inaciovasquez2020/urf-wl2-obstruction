from __future__ import annotations
import sys
from collections import Counter
from graphio import read_edgelist, build_adj, has_edge

def wl2_full_from_adj(adj, rounds=5):
    n = len(adj)

    # initial colors on ordered pairs (i,j)
    # (diag?, edge?)
    colors = {(i,j): (1 if i==j else 0, has_edge(adj,i,j)) for i in range(n) for j in range(n)}

    for _ in range(rounds):
        palette = {}
        nxt = 0
        new = {}
        for i in range(n):
            for j in range(n):
                base = colors[(i,j)]
                agg = [(colors[(i,w)], colors[(w,j)]) for w in range(n)]
                agg.sort()
                sig = (base, tuple(agg))
                c = palette.get(sig)
                if c is None:
                    c = nxt
                    palette[sig] = c
                    nxt += 1
                new[(i,j)] = c
        colors = new

    return Counter(colors.values())

def main():
    if len(sys.argv) < 2:
        print("usage: python3 scripts/wl2_full.py <graph.edgelist> [rounds]")
        sys.exit(2)
    path = sys.argv[1]
    rounds = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    nodes, edges = read_edgelist(path)
    _, adj = build_adj(nodes, edges)
    print(wl2_full_from_adj(adj, rounds=rounds))

if __name__ == "__main__":
    main()
