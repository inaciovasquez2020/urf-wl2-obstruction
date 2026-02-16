#!/usr/bin/env python3
# Dependency-free sampled WL-3 with correct Q-closure
# Usage:
#   python3 scripts/wl3_sampled.py GRAPH.edgelist ROUNDS |W| |Q| SEED
#
# Output: multiset histogram of final colors on Q

import sys
import random
from collections import Counter

# ---------- basic graph loader (no deps) ----------

def read_edgelist(path):
    edges = set()
    nodes = set()
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            a,b = line.split()
            a = int(a); b = int(b)
            if a == b: 
                continue
            edges.add((a,b))
            edges.add((b,a))
            nodes.add(a); nodes.add(b)
    return sorted(nodes), edges

# ---------- WL-3 sampled ----------

def wl3_sampled(nodes, edges, rounds, Wsize, Qtarget, seed):
    rng = random.Random(seed)
    V = nodes
    n = len(V)

    # sample W ⊆ V
    if Wsize >= n:
        W = list(V)
    else:
        W = rng.sample(V, Wsize)

    # initial P ⊆ V^3
    P = set()
    while len(P) < Qtarget:
        a = rng.choice(V)
        b = rng.choice(V)
        c = rng.choice(V)
        P.add((a,b,c))

    # ---- closure: build Q ----
    Qset = set(P)
    changed = True
    while changed:
        changed = False
        new_items = set()
        for (a,b,c) in Qset:
            for w in W:
                t0 = (w,b,c)
                t1 = (a,w,c)
                t2 = (a,b,w)
                if t0 not in Qset: new_items.add(t0)
                if t1 not in Qset: new_items.add(t1)
                if t2 not in Qset: new_items.add(t2)
        if new_items:
            Qset |= new_items
            changed = True
    Q = list(Qset)

    # initial colors on Q
    # encode equality pattern + adjacency pattern
    colors = {}
    for (a,b,c) in Q:
        eq = (a==b, b==c, a==c)
        adj = (
            1 if (a,b) in edges else 0,
            1 if (b,c) in edges else 0,
            1 if (a,c) in edges else 0,
        )
        colors[(a,b,c)] = (eq, adj)

    # safety: closure guarantees these exist
    for (a,b,c) in Q:
        for w in W:
            assert (w,b,c) in colors
            assert (a,w,c) in colors
            assert (a,b,w) in colors

    # refinement rounds
    for _ in range(rounds):
        palette = {}
        nxt = 0
        newcolors = {}
        for (a,b,c) in Q:
            base = colors[(a,b,c)]
            agg = []
            for w in W:
                agg.append((
                    colors[(w,b,c)],
                    colors[(a,w,c)],
                    colors[(a,b,w)]
                ))
            agg.sort()
            sig = (base, tuple(agg))
            if sig not in palette:
                palette[sig] = nxt
                nxt += 1
            newcolors[(a,b,c)] = palette[sig]
        colors = newcolors

    return Counter(colors.values())

# ---------- main ----------

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("usage: wl3_sampled.py GRAPH ROUNDS WSIZE QSIZE SEED")
        sys.exit(1)

    graph = sys.argv[1]
    rounds = int(sys.argv[2])
    Wsize = int(sys.argv[3])
    Qsize = int(sys.argv[4])
    seed   = int(sys.argv[5])

    nodes, edges = read_edgelist(graph)
    hist = wl3_sampled(nodes, edges, rounds, Wsize, Qsize, seed)
    print(dict(hist))

