#!/usr/bin/env python3
import json
from itertools import combinations, product
from collections import defaultdict

def canon(ball):
    # canonical encoding: sorted adjacency lists
    return json.dumps(
        {str(k): sorted(v) for k, v in sorted(ball.items())},
        sort_keys=True
    )

def generate_balls():
    balls = {}
    root = 0

    for d in range(0, 4):  # root degree
        neighbors = list(range(1, d + 1))

        # each neighbor can have 0,1,2 children
        for child_counts in product([0, 1, 2], repeat=d):
            total_children = sum(child_counts)
            if total_children > 6:
                continue

            # build base tree
            ball = defaultdict(list)
            next_node = d + 1

            for i, c in enumerate(child_counts):
                u = neighbors[i]
                ball[root].append(u)
                ball[u].append(root)
                for _ in range(c):
                    v = next_node
                    next_node += 1
                    ball[u].append(v)
                    ball[v].append(u)

            # optional edges between neighbors (depth-1)
            for k in range(len(neighbors) + 1):
                for extra in combinations(neighbors, k):
                    b2 = {u: list(vs) for u, vs in ball.items()}
                    ok = True
                    for u, v in combinations(extra, 2):
                        if v not in b2[u]:
                            b2[u].append(v)
                            b2[v].append(u)
                        if len(b2[u]) > 3 or len(b2[v]) > 3:
                            ok = False
                            break
                    if not ok:
                        continue

                    key = canon(b2)
                    balls[key] = b2

    return balls

def build_overlap_automaton(balls):
    # conservative: allow overlap if root degrees match
    auto = defaultdict(list)
    keys = list(balls.keys())
    for k1 in keys:
        deg1 = len(balls[k1].get("0", balls[k1].get(0, [])))
        for k2 in keys:
            deg2 = len(balls[k2].get("0", balls[k2].get(0, [])))
            if deg1 == deg2:
                auto[k1].append(k2)
    return auto

def main():
    balls = generate_balls()
    auto = build_overlap_automaton(balls)

    out = {
        "Delta": 3,
        "R": 2,
        "ball_count": len(balls),
        "automaton_states": len(auto)
    }

    with open("artifacts/balls_d3_r2_automaton.json", "w") as f:
        json.dump(out, f, indent=2, sort_keys=True)

    print(json.dumps(out, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()

