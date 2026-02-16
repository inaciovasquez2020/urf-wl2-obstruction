from __future__ import annotations
import sys, random
from collections import Counter
from typing import Dict, List, Tuple
from graphio import read_edgelist, build_adj, has_edge

Triple = Tuple[int,int,int]

def init_color(adj, a: int, b: int, c: int) -> Tuple[int,int,int,int,int,int]:
    # equality pattern + edge bits among pairs
    eq_ab = 1 if a == b else 0
    eq_ac = 1 if a == c else 0
    eq_bc = 1 if b == c else 0
    e_ab = has_edge(adj, a, b)
    e_ac = has_edge(adj, a, c)
    e_bc = has_edge(adj, b, c)
    return (eq_ab, eq_ac, eq_bc, e_ab, e_ac, e_bc)

def wl3_sampled(adj, rounds=2, k=50, s=2000, seed=0) -> Counter:
    rng = random.Random(seed)
    n = len(adj)

    W = [rng.randrange(n) for _ in range(min(k, n))]
    P: List[Triple] = [(rng.randrange(n), rng.randrange(n), rng.randrange(n)) for _ in range(s)]

    # closure Q under one-coordinate replacement by W
    Qset = set(P)
    for (a,b,c) in P:
        for w in W:
            Qset.add((w,b,c))
            Qset.add((a,w,c))
            Qset.add((a,b,w))
    Q = list(Qset)

    # init colors on Q
    colors: Dict[Triple, object] = {t: init_color(adj, *t) for t in Q}

    for _ in range(rounds):
        palette: Dict[Tuple, int] = {}
        nxt = 0
        new: Dict[Triple, int] = {}

        for (a,b,c) in Q:
            base = colors[(a,b,c)]

            M0 = [colors[(w,b,c)] for w in W]
            M1 = [colors[(a,w,c)] for w in W]
            M2 = [colors[(a,b,w)] for w in W]
            M0.sort(); M1.sort(); M2.sort()

            sig = (base, tuple(M0), tuple(M1), tuple(M2))
            col = palette.get(sig)
            if col is None:
                col = nxt
                palette[sig] = col
                nxt += 1
            new[(a,b,c)] = col

        colors = new

    # return multiset over sampled triples P
    return Counter(colors[t] for t in P)

def main():
    if len(sys.argv) < 2:
        print("usage: python3 scripts/wl3_sampled.py <graph.edgelist> [rounds k s seed]")
        raise SystemExit(2)
    path = sys.argv[1]
    rounds = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    k = int(sys.argv[3]) if len(sys.argv) > 3 else 50
    s = int(sys.argv[4]) if len(sys.argv) > 4 else 2000
    seed = int(sys.argv[5]) if len(sys.argv) > 5 else 0

    nodes, edges = read_edgelist(path)
    _, adj = build_adj(nodes, edges)
    print(wl3_sampled(adj, rounds=rounds, k=k, s=s, seed=seed))

if __name__ == "__main__":
    main()
