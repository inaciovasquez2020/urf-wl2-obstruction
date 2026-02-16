#!/usr/bin/env python3
import argparse
import json
import hashlib
import os
import random
from typing import List, Tuple

Edge = Tuple[int, int]

def normalize_edges(edges: List[Edge]) -> List[Edge]:
    out = []
    for u, v in edges:
        if u == v:
            raise ValueError("self-loop")
        a, b = (u, v) if u < v else (v, u)
        out.append((a, b))
    out = sorted(set(out))
    return out

def base_graph_H():
    n = 4
    edges = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        (0, 2)
    ]
    return n, normalize_edges(edges)

def lift_2(n: int, edges: List[Edge], seed: int):
    rng = random.Random(seed)
    edges = normalize_edges(edges)

    def vid(u, bit):
        return 2 * u + bit

    new_edges = []
    for (u, v) in edges:
        sign = rng.getrandbits(1)
        if sign == 0:
            pairs = [(vid(u,0), vid(v,0)), (vid(u,1), vid(v,1))]
        else:
            pairs = [(vid(u,0), vid(v,1)), (vid(u,1), vid(v,0))]
        for a, b in pairs:
            x, y = (a, b) if a < b else (b, a)
            new_edges.append((x, y))

    return 2 * n, normalize_edges(new_edges)

def generate_Tn(t: int, seed: int):
    n, edges = base_graph_H()
    meta = {
        "base_graph": "H4_cycle_plus_chord",
        "seed": seed,
        "t": t,
        "steps": []
    }

    for i in range(1, t + 1):
        step_seed = seed + i
        n, edges = lift_2(n, edges, step_seed)
        meta["steps"].append({
            "i": i,
            "seed": step_seed,
            "n": n,
            "m": len(edges)
        })

    return n, edges, meta

def write_edgelist(n: int, edges: List[Edge], path: str) -> str:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    lines = [f"n {n} m {len(edges)}\n"]
    for u, v in edges:
        lines.append(f"{u} {v}\n")
    data = "".join(lines).encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    return hashlib.sha256(data).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--t", type=int, required=True)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--outdir", default="artifacts")
    ap.add_argument("--name", default=None)
    args = ap.parse_args()

    n, edges, meta = generate_Tn(args.t, args.seed)
    name = args.name or f"Tn_n{n}_t{args.t}_seed{args.seed}"
    out_path = os.path.join(args.outdir, f"{name}.edgelist")

    sha = write_edgelist(n, edges, out_path)
    meta["output"] = {
        "name": name,
        "path": out_path,
        "n": n,
        "m": len(edges),
        "sha256": sha
    }

    meta_path = os.path.join(args.outdir, f"{name}.meta.json")
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2, sort_keys=True)

    print(json.dumps(meta["output"], indent=2, sort_keys=True))

if __name__ == "__main__":
    main()

