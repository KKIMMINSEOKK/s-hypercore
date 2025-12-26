import queue
from collections import defaultdict
import func

def run(G, s):
    R = set()
    S = set()
    computed = set()
    ES = {}
    LB = {}
    Q = queue.Queue()
    map = func.get_map(G)

    # ===== Early elimination via upper bounds =====
    for node in G.nodes:
        degree = len(G.nodes[node].Edge)
        if degree < s:
            R.add(node)
    for node in R:
        G.del_node(node)

    # ===== Initial ES computation =====
    for node in G.nodes:
        core = node in S
        N = defaultdict(list)
        for hyperedge in G.nodes[node].Edge:
            for neighbor in G.hyperedges[hyperedge]:
                if (not core or neighbor not in S) and neighbor not in computed and neighbor != node:
                    N[neighbor].append(hyperedge)
        if node not in ES:
            ES[node] = 0
        for neighbor in N:
            DCS = func.getDCS(node, neighbor, N, G, map)
            if neighbor not in ES:
                ES[neighbor] = 0
            ES[neighbor] += DCS
            if not core:
                ES[node] += DCS
                if DCS >= s:
                    S.add(node)
                    S.add(neighbor)
                    core = True
            else:
                if neighbor not in LB:
                    LB[neighbor] = 0
                LB[neighbor] += DCS
                if LB[neighbor] >= s:
                    S.add(neighbor)
        if ES[node] < s:
            Q.put(node)
        computed.add(node)

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