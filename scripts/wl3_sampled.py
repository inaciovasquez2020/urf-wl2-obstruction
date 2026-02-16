#!/usr/bin/env python3
# WL-3 sampled baseline (dependency-free, operationally bounded).
#
# Semantics: colors live on a finite sampled/closed set Q ⊆ V^3. Each round refines
# c(a,b,c) using a base color + (sampled) multisets over one-coordinate substitutions.
#
# Key properties:
# - Dependency-free (stdlib only)
# - Q-closure enforced (no KeyError)
# - Hard caps prevent supercubic blow-up (no global sort of huge lists)
#
# Usage:
#   python3 scripts/wl3_sampled.py <graph.edgelist> [rounds Wsize Qsize seed]
# Defaults:
#   rounds=2, Wsize=20, Qsize=600, seed=0

import sys
import random
from collections import Counter
from pathlib import Path


def read_edgelist(path):
    nodes = set()
    edges = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue

            parts = line.split()
            if len(parts) != 2:
                continue  # ignore malformed / metadata lines

            a, b = parts
            a = int(a)
            b = int(b)

            nodes.add(a)
            nodes.add(b)
            edges.append((a, b))

    return sorted(nodes), edges

def build_adj(nodes, edges):
    idx = {v: i for i, v in enumerate(nodes)}
    n = len(nodes)
    adj = [set() for _ in range(n)]
    for u, v in edges:
        iu = idx[u]
        iv = idx[v]
        if iu == iv:
            continue
        adj[iu].add(iv)
        adj[iv].add(iu)
    return idx, adj


def init_color(adj, a, b, c):
    # Cheap WL-3 initial color: (equalities, adjacencies among coords)
    eq_ab = 1 if a == b else 0
    eq_ac = 1 if a == c else 0
    eq_bc = 1 if b == c else 0
    e_ab = 1 if b in adj[a] else 0
    e_ac = 1 if c in adj[a] else 0
    e_bc = 1 if c in adj[b] else 0
    return (eq_ab, eq_ac, eq_bc, e_ab, e_ac, e_bc)


def _close_Q(Qset, n, W, cap):
    """
    Enforce closure under (w,b,c),(a,w,c),(a,b,w) for all (a,b,c) in Q and w in W,
    with hard cap to prevent blow-up.
    """
    changed = True
    while changed:
        changed = False
        if len(Qset) >= cap:
            break
        # Iterate over a snapshot to avoid infinite growth while looping
        snapshot = list(Qset)
        for (a, b, c) in snapshot:
            for w in W:
                if len(Qset) >= cap:
                    return Qset
                t0 = (w, b, c)
                t1 = (a, w, c)
                t2 = (a, b, w)
                if t0 not in Qset:
                    Qset.add(t0)
                    changed = True
                    if len(Qset) >= cap:
                        return Qset
                if t1 not in Qset:
                    Qset.add(t1)
                    changed = True
                    if len(Qset) >= cap:
                        return Qset
                if t2 not in Qset:
                    Qset.add(t2)
                    changed = True
                    if len(Qset) >= cap:
                        return Qset
    return Qset


def wl3_sampled(nodes, edges, rounds=2, Wsize=20, Qsize=600, seed=0):
    _, adj = build_adj(nodes, edges)
    n = len(adj)

    rng = random.Random(seed)

    # Sample W ⊆ V
    if Wsize > n:
        Wsize = n
    W = rng.sample(range(n), Wsize)

    # Sample initial Q ⊆ V^3 (uniform iid triples), then close under W-substitutions.
    Q = set()
    while len(Q) < min(Qsize, n * n * n):
        Q.add((rng.randrange(n), rng.randrange(n), rng.randrange(n)))
        if len(Q) >= Qsize:
            break

    # Closure can increase Q; allow up to 4x before hard stop.
    Qcap = max(Qsize, min(n * n * n, 4 * Qsize))
    Q = _close_Q(Q, n, W, cap=Qcap)

    # Initialize colors only on Q
    colors = {t: init_color(adj, *t) for t in Q}

    for _round in range(rounds):
        palette = {}
        nxt = 0
        new = {}

        # Precompute once: for fast access to colors with default
        # (should not happen if closure is correct, but safe anyway)
        def getc(t):
            return colors.get(t)

        for (a, b, c) in Q:
            base = getc((a, b, c))
            # base must exist
            if base is None:
                base = init_color(adj, a, b, c)

            # Sampled multisets over coordinate substitutions:
            # We DO NOT sort huge lists. We compute bounded fingerprints.
            # Each multiset is represented by a capped histogram over colors.
            # Cap size to keep runtime bounded.
            cap_hist = 8

            M0 = []
            M1 = []
            M2 = []

            for w in W:
                v0 = getc((w, b, c))
                v1 = getc((a, w, c))
                v2 = getc((a, b, w))

                # Closure should guarantee these exist; fallback if not.
                if v0 is None:
                    v0 = init_color(adj, w, b, c)
                if v1 is None:
                    v1 = init_color(adj, a, w, c)
                if v2 is None:
                    v2 = init_color(adj, a, b, w)

                M0.append(v0)
                M1.append(v1)
                M2.append(v2)

            # Build capped histograms (Counter->sorted small list)
            # This avoids O(|W| log |W|) sorting of full lists in the hot loop.
            c0 = Counter(M0)
            c1 = Counter(M1)
            c2 = Counter(M2)

            # Keep only the top cap_hist entries deterministically
            # Order: by count desc, then by repr of key for stability.
            def top_items(C):
                items = list(C.items())
                items.sort(key=lambda kv: (-kv[1], repr(kv[0])))
                return tuple(items[:cap_hist])

            sig = (base, top_items(c0), top_items(c1), top_items(c2))

            col = palette.get(sig)
            if col is None:
                col = nxt
                palette[sig] = col
                nxt += 1
            new[(a, b, c)] = col

        colors = new

    # Return multiset of colors over Q (can also restrict to original sampled triples if desired)
    return Counter(colors.values())


def main():
    if len(sys.argv) < 2:
        print("usage: python3 scripts/wl3_sampled.py <graph.edgelist> [rounds Wsize Qsize seed]")
        raise SystemExit(2)

    path = sys.argv[1]
    rounds = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    Wsize = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    Qsize = int(sys.argv[4]) if len(sys.argv) > 4 else 600
    seed = int(sys.argv[5]) if len(sys.argv) > 5 else 0

    nodes, edges = read_edgelist(path)
    hist = wl3_sampled(nodes, edges, rounds=rounds, Wsize=Wsize, Qsize=Qsize, seed=seed)
    print(hist)


if __name__ == "__main__":
    main()

