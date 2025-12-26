# ===== Node class: represents a single node in the hypergraph =====
class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.NodeCnt = 0
        self.EdgeCnt = 0
        self.Edge = set()

# ===== Hypergraph class: represents the overall hypergraph structure =====
class Hypergraph:
    def __init__(self):
        self.nodes = {}
        self.hyperedges = {}

    def load_from_file(self, file_path):
        """Loads hyperedges from file (comma or space separated)"""
        with open(file_path, 'r') as file:
            for line in file:
                if ',' in line:
                    current_nodes = {int(node.strip()) for node in line.strip().split(',')}
                elif '\t' in line:
                    current_nodes = {int(node.strip()) for node in line.strip().split('\t')}
                else:
                    current_nodes = {int(node.strip()) for node in line.strip().split(' ')}

                self.add_hyperedge(current_nodes)

    def add_hyperedge(self, edge_nodes):
        """Adds a new hyperedge and updates node-hyperedge relations"""
        hyperedge_id = len(self.hyperedges) + 1
        self.hyperedges[hyperedge_id] = edge_nodes

        for node in edge_nodes:
            if node not in self.nodes:
                self.nodes[node] = Node(node)
            self.nodes[node].Edge.add(hyperedge_id)

    def del_node(self, node):
        """Deletes a node from the hypergraph and updates all connected hyperedges"""
        if node in self.nodes:
            for hyperedge in self.nodes[node].Edge:
                self.hyperedges[hyperedge].remove(node)
            del self.nodes[node]

    def del_edge(self, edge):
        """Deletes a hyperedge from the hypergraph"""
        if edge in self.hyperedges:
            for node in self.hyperedges[edge]:
                self.nodes[node].Edge.remove(edge)
            del self.hyperedges[edge]

# ===== Helper functions =====
def get_map(G):
    map = {}
    for id, edge_set in G.hyperedges.items():
        map[id] = len(edge_set)
    return map

def getDCS(u, v, N, G, map):
    common_edges = N[v]
    sum_of_decay_weight = sum(decayWeight(map, e) for e in common_edges)
    jacc = len(common_edges) / (len(G.nodes[u].Edge) + len(G.nodes[v].Edge) - len(common_edges))
    return sum_of_decay_weight * jacc

def decayWeight(map, e):
    return 1 / ((map[e] - 1))

def jaccard(A, B):
    intersection = len(A & B)
    union = len(A) + len(B) - intersection
    if union == 0:
        return 0.0
    return intersection / union

# ===== Statistics and metrics =====
def get_statistics(G, ES, map):
    induced_hyperedges = get_hyperedges(G)
    results = {}
    results['# of nodes'] = len(G.nodes)
    results['# of hyp.'] = len(induced_hyperedges)
    results['avg. ES'] = get_avg_ES(ES)
    results['avg. # of nb.'] = get_avg_num_of_neighbors(G, ES)
    results['avg. DCS'] = 0 if results['avg. # of nb.'] == 0 else results['avg. ES'] / results['avg. # of nb.']
    results['induced density'] = 0 if results['# of nodes'] == 0 else results['# of hyp.'] / results['# of nodes']
    results['avg. jacc.'], results['avg. supp.'], results['avg. card.'] = get_avg_jaccard_and_support_and_cardinality(G, ES, map)
    return results

def get_hyperedges(G):
    hyperedges = {}
    for node in G.nodes:
        for hyperedge in G.nodes[node].Edge:
            if hyperedge not in hyperedges:
                hyperedges[hyperedge] = 1
            else:
                hyperedges[hyperedge] += 1
    induced_hyperedges = {hyperedge for hyperedge, count in hyperedges.items() if count >= 2}
    return induced_hyperedges

def get_avg_ES(ES):
    total_ES = sum(es for es in ES.values())
    if len(ES) == 0:
        return 0
    return total_ES / len(ES)

def get_neighbors(G, node, ES):
    neighbors = set()
    for hyperedge in G.nodes[node].Edge:
        neighbors.update(G.hyperedges[hyperedge])
    ES_neighbors = set()
    for neighbor in neighbors:
        if neighbor in ES and neighbor is not node:
            ES_neighbors.add(neighbor)
    return ES_neighbors

def get_avg_num_of_neighbors(G, ES):
    total_neighbors = 0
    for node in G.nodes:
        total_neighbors += len(get_neighbors(G, node, ES))
    if len(G.nodes) == 0:
        return 0
    return total_neighbors / len(G.nodes)

def get_avg_jaccard_and_support_and_cardinality(G, ES, map):
    jacc_sum = 0
    supp_sum = 0
    card_sum = 0
    total_neighbors = 0
    for node in G.nodes:
        neighbors = get_neighbors(G, node, ES)
        total_neighbors += len(neighbors)
        for neighbor in neighbors:
            intersection = G.nodes[node].Edge & G.nodes[neighbor].Edge
            jacc_sum += len(intersection) / (len(G.nodes[node].Edge) + len(G.nodes[neighbor].Edge) - len(intersection))
            supp_sum += len(intersection)
            card_temp = 0
            for hyperedge in intersection:
                card_temp += map[hyperedge]
            card_sum += card_temp / len(intersection)
    if total_neighbors == 0:
        return 0, 0, 0
    return jacc_sum / total_neighbors, supp_sum / total_neighbors, card_sum / total_neighbors