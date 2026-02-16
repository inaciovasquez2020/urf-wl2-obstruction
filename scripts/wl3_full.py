from __future__ import annotations
import sys
from collections import Counter
from graphio import read_edgelist, build_adj, has_edge

def init_color(adj, a: int, b: int, c: int):
    eq_ab = 1 if a == b else 0
    eq_ac = 1 if a == c else 0
    eq_bc = 1 if b == c else 0
    e_ab = has_edge(adj, a, b)
    e_ac = has_edge(adj, a, c)
    e_bc = has_edge(adj, b, c)
    return (eq_ab, eq_ac, eq_bc, e_ab, e_ac, e_bc)

def wl3_full(adj, rounds=3):
    n = len(adj)

    # colors on ordered triples
    colors = {(a,b,c): init_color(adj,a,b,c) for a in range(n) for b in range(n) for c in range(n)}

    for _ in range(rounds):
        palette = {}
        nxt = 0
        new = {}

        for a in range(n):
            for b in range(n):
                for c in range(n):
                    base = colors[(a,b,c)]
                    M0 = [colors[(w,b,c)] for w in range(n)]
                    M1 = [colors[(a,w,c)] for w in range(n)]
                    M2 = [colors[(a,b,w)] for w in range(n)]
                    M0.sort(); M1.sort(); M2.sort()
                    sig = (base, tuple(M0), tuple(M1), tuple(M2))
                    col = palette.get(sig)
                    if col is None:
                        col = nxt
                        palette[sig] = col
                        nxt += 1
                    new[(a,b,c)] = col

        colors = new

    return Counter(colors.values())

def main():
    if len(sys.argv) < 2:
        print("usage: python3 scripts/wl3_full.py <graph.edgelist> [rounds]")
        raise SystemExit(2)
    path = sys.argv[1]
    rounds = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    nodes, edges = read_edgelist(path)
    _, adj = build_adj(nodes, edges)
    n = len(adj)
    if n > 18:
        print(f"ERROR: n={n} too large for wl3_full (set a smaller limit or use wl3_sampled)")
        raise SystemExit(1)
    print(wl3_full(adj, rounds=rounds))

if __name__ == "__main__":
    main()
