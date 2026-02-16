#!/usr/bin/env python3

import sys
import random
from collections import Counter, defaultdict


def read_edgelist(path):
    adj = defaultdict(set)
    skipped = 0
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                skipped += 1
                continue
            parts = line.split()
            if len(parts) < 2:
                skipped += 1
                continue
            try:
                u = int(parts[0])
                v = int(parts[1])
            except ValueError:
                skipped += 1
                continue
            adj[u].add(v)
            adj[v].add(u)
    print(f"[wl3] skipped lines: {skipped}", file=sys.stderr)
    return adj


def wl3_sampled(adj, depth, iters, samples, seed):
    rng = random.Random(seed)

    nodes = sorted(adj.keys())
    n = len(nodes)

    if n == 0:
        # minimal safe behavior: return empty sample
        print("[wl3] warning: empty adjacency, returning empty sample", file=sys.stderr)
        return []

    # initial colors
    color = {v: 0 for v in nodes}

    for _ in range(iters):
        new_color = {}
        color_ids = {}
        next_id = 0

        for v in nodes:
            neigh_colors = sorted(color[u] for u in adj[v])
            sig = (color[v], tuple(neigh_colors))
            if sig not in color_ids:
                color_ids[sig] = next_id
                next_id += 1
            new_color[v] = color_ids[sig]

        color = new_color

    samples_out = []
    for _ in range(samples):
        if n >= 3:
            a, b, c = rng.sample(nodes, 3)
        else:
            a = rng.choice(nodes)
            b = rng.choice(nodes)
            c = rng.choice(nodes)

        sig = (
            color[a],
            color[b],
            color[c],
            tuple(sorted(color[u] for u in adj[a])),
            tuple(sorted(color[u] for u in adj[b])),
            tuple(sorted(color[u] for u in adj[c])),
        )
        samples_out.append(hash(sig))

    return samples_out


def main():
    if len(sys.argv) != 6:
        print(
            "usage: wl3_sampled.py <edgelist> <depth> <iters> <samples> <seed>",
            file=sys.stderr,
        )
        sys.exit(1)

    path = sys.argv[1]
    depth = int(sys.argv[2])   # interface compatibility
    iters = int(sys.argv[3])
    samples = int(sys.argv[4])
    seed = int(sys.argv[5])

    adj = read_edgelist(path)
    samples_out = wl3_sampled(adj, depth, iters, samples, seed)

    raw_counter = Counter(samples_out)

    collapsed = Counter()
    for k in raw_counter:
        collapsed[k] = 1

    print(collapsed)


if __name__ == "__main__":
    main()

