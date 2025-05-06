import networkx as nx

def horizon_effect_search(G, node, depth, maximizing_player):
    # Detiene si se alcanza la profundidad o si el nodo es terminal
    if depth == 0 or G.out_degree(node) == 0:
        return G.nodes[node].get('value', 0)

    if maximizing_player:
        best_value = float('-inf')
        for child in G.successors(node):  # Explora hijos (jugador maximizador)
            value = horizon_effect_search(G, child, depth - 1, False)
            best_value = max(best_value, value)
        return best_value
    else:
        best_value = float('inf')
        for child in G.successors(node):  # Explora hijos (jugador minimizador)
            value = horizon_effect_search(G, child, depth - 1, True)
            best_value = min(best_value, value)
        return best_value

# ------- Grafo del juego -------
G = nx.DiGraph()
G.add_nodes_from([
    (0, {"value": None}), (1, {"value": None}), (2, {"value": None}),
    (3, {"value": 3}), (4, {"value": 7}), (5, {"value": 2}), (6, {"value": 8})
])
G.add_edges_from([
    (0, 1), (0, 2),
    (1, 3), (1, 4),
    (2, 5), (2, 6)
])

# ------- Simulación con profundidad limitada -------
search_depth = 2
estimated_value = horizon_effect_search(G, 0, search_depth, True)
print(f"Valor estimado del nodo raíz con efecto horizonte: {estimated_value}")
