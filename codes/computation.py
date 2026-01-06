import queue
from collections import defaultdict
import func
def run(G, s):
    R = set()
    S = set()
    T = set()
    ES = {}
    LB = {}
    Q = queue.Queue()
    map = func.get_map(G)

    # ===== Early elimination via upper bounds =====
    for node in G.nodes:
        degree = len(G.nodes[node].Edge)
        if degree < s:
            R.add(node) # By lemma 3
        else:
            ES[node] = 0
            LB[node] = 0
    for node in R:
        G.del_node(node)

    # ===== Initial ES computation =====
    for node in G.nodes:
        core = node in S
        N = defaultdict(list)
        for hyperedge in G.nodes[node].Edge:
            for neighbor in G.hyperedges[hyperedge]:
                if (not core or neighbor not in S) and neighbor not in T and neighbor != node:
                    N[neighbor].append(hyperedge)
        for neighbor in N:
            if core and neighbor in S:
                continue
            DCS = func.getDCS(node, neighbor, N, G, map)
            if core:
                ES[neighbor] += DCS
                LB[neighbor] += DCS
                if LB[neighbor] >= s:
                    S.add(neighbor) # By lemma 5
            elif neighbor in S:
                ES[node] += DCS
                LB[node] += DCS
                if LB[node] >= s:
                    S.add(node) # By lemma 5
                    core = True
            else:
                ES[node] += DCS
                ES[neighbor] += DCS
                if DCS >= s:
                    S.add(node) # By lemma 4
                    S.add(neighbor) # By lemma 4
                    core = True
        T.add(node)
        if ES[node] < s:
            Q.put(node)

    # ===== Peeling process =====
    while not Q.empty():
        node = Q.get()
        del ES[node]
        N = defaultdict(list)
        for hyperedge in G.nodes[node].Edge:
            for neighbor in G.hyperedges[hyperedge]:
                if neighbor != node and neighbor not in S and ES[neighbor] >= s:
                    N[neighbor].append(hyperedge)
        for neighbor in N:
            DCS = func.getDCS(node, neighbor, N, G, map)
            ES[neighbor] -= DCS
            if ES[neighbor] < s:
                Q.put(neighbor)
        G.del_node(node)

    # ===== Compute additional statistics =====
    results = {}
    results = func.get_statistics(G, ES, map)
    return G, results