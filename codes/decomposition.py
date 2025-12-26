import queue
import heapq
from collections import defaultdict
import func

def run(G):
    # ===== Initial setup =====
    ES = {}
    C = {}
    computed = set()
    Q = queue.Queue()
    U = set()
    pq = []
    map = func.get_map(G)

    # ===== Initial ES computation =====
    for node in G.nodes:
        N = defaultdict(list)
        for hyperedge in G.nodes[node].Edge:
            for neighbor in G.hyperedges[hyperedge]:
                if neighbor not in computed and neighbor != node:
                    N[neighbor].append(hyperedge)
        if node not in ES:
            ES[node] = 0
        for neighbor in N:
            DCS = func.getDCS(node, neighbor, N, G, map)
            ES[node] += DCS
            if neighbor not in ES:
                ES[neighbor] = 0
            ES[neighbor] += DCS
        computed.add(node)
        heapq.heappush(pq, (ES[node], node))
    if pq:
        min_val, min_node = heapq.heappop(pq)
    else:
        return C, {}
    Q.put(min_node)
    coreness = min_val

    # ===== Peeling process =====
    while not Q.empty():
        node = Q.get()
        C[node] = coreness
        del ES[node]
        neighbors = defaultdict(list)
        for hyperedge in G.nodes[node].Edge:
            for neighbor in G.hyperedges[hyperedge]:
                if neighbor != node and neighbor in ES and ES[neighbor] > coreness:
                    neighbors[neighbor].append(hyperedge)
        for neighbor in neighbors:
            DCS = func.getDCS(node, neighbor, neighbors, G, map)
            ES[neighbor] -= DCS
            if ES[neighbor] <= coreness:
                Q.put(neighbor)
            else:
                U.add(neighbor)
        G.del_node(node)

        if Q.empty() and G.nodes:
            for node in U:
                if node in ES:
                    heapq.heappush(pq, (ES[node], node))
            U = set()
            while pq:
                coreness, min_node = heapq.heappop(pq)
                if min_node in ES:
                    break
            Q.put(min_node)

    results = {}
    return C, results