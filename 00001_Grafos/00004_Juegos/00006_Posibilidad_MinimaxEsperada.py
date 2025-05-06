import networkx as nx

def expected_minimax(G, node, depth, maximizing_player):
    # Fin si se alcanza la profundidad o es nodo terminal
    if depth == 0 or G.out_degree(node) == 0:
        return G.nodes[node].get('value', 0)

    if maximizing_player:
        best_value = float('-inf')
        for child in G.successors(node):  # Turno del maximizador
            prob = G[node][child].get('prob', 1)  # Probabilidad de transición
            value = expected_minimax(G, child, depth - 1, False)
            best_value = max(best_value, prob * value)  # Selección ponderada
        return best_value
    else:
        best_value = float('inf')
        for child in G.successors(node):  # Turno del minimizador
            prob = G[node][child].get('prob', 1)
            value = expected_minimax(G, child, depth - 1, True)
            best_value = min(best_value, prob * value)
        return best_value

# ------- Grafo con nodos y probabilidades -------
G = nx.DiGraph()
G.add_nodes_from([
    (0, {"value": None}), (1, {"value": None}), (2, {"value": None}),
    (3, {"value": 3}), (4, {"value": 7}),
    (5, {"value": 2}), (6, {"value": 8})
])
G.add_edges_from([
    (0, 1, {"prob": 0.6}), (0, 2, {"prob": 0.4}),
    (1, 3, {"prob": 0.7}), (1, 4, {"prob": 0.3}),
    (2, 5, {"prob": 0.5}), (2, 6, {"prob": 0.5})
])

# ------- Ejecución del algoritmo -------
expected_value = expected_minimax(G, 0, 3, True)
print(f"Valor esperado del nodo raíz: {expected_value}")
