#!/usr/bin/env python3
# Deterministic Cai–Fürer–Immerman construction over Petersen graph
# mode = 0 or 1 selects the non-isomorphic CFI twist

import sys

def petersen_edges():
    # Standard Petersen graph on vertices 0..9
    outer = [(0,1),(1,2),(2,3),(3,4),(4,0)]
    inner = [(5,7),(7,9),(9,6),(6,8),(8,5)]
    spokes = [(0,5),(1,6),(2,7),(3,8),(4,9)]
    return outer + inner + spokes

def main():
    if len(sys.argv) != 2:
        print("usage: cfi_petersen.py {0|1}", file=sys.stderr)
        sys.exit(1)

    mode = int(sys.argv[1])
    edges = petersen_edges()

    # CFI lift: each vertex v -> (v,0),(v,1)
    # Twist parity controlled by mode
    for (u,v) in edges:
        for a in (0,1):
            b = a ^ (mode if (u+v) % 2 == 0 else 0)
            print(f"{2*u+a} {2*v+b}")
            print(f"{2*v+b} {2*u+a}")

if __name__ == "__main__":
    main()

