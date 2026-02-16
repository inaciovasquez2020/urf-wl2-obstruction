import sys
import networkx as nx
from collections import Counter

def wl2_full(G, rounds=5):
    V = list(G.nodes())
    colors = {(u,v): (u==v, G.has_edge(u,v)) for u in V for v in V}

    for _ in range(rounds):
        palette = {}
        new = {}
        nxt = 0
        for u in V:
            for v in V:
                sig = (colors[(u,v)],
                       tuple(sorted((colors[(u,w)], colors[(w,v)]) for w in V)))
                if sig not in palette:
                    palette[sig] = nxt
                    nxt += 1
                new[(u,v)] = palette[sig]
        colors = new

    return Counter(colors.values())

if __name__ == "__main__":
    G = nx.read_edgelist(sys.argv[1], nodetype=int)
    r = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    print(wl2_full(G, r))
