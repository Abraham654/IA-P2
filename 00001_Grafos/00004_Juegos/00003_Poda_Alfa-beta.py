import networkx as nx

def alphabeta(G, node, depth, alpha, beta, maximizing_player):
    # Si se llega al fondo o a una hoja, devuelve su valor
    if depth == 0 or G.out_degree(node) == 0:
        return G.nodes[node]['value']
    
    if maximizing_player:
        best_value = float('-inf')
        for child in G.successors(node):  # Explora hijos
            value = alphabeta(G, child, depth - 1, alpha, beta, False)
            best_value = max(best_value, value)  # Guarda el mejor valor
            alpha = max(alpha, best_value)  # Actualiza alfa
            if beta <= alpha: break  # Poda
        return best_value
    else:
        best_value = float('inf')
        for child in G.successors(node):
            value = alphabeta(G, child, depth - 1, alpha, beta, True)
            best_value = min(best_value, value)  # Guarda el peor valor
            beta = min(beta, best_value)  # Actualiza beta
            if beta <= alpha: break  # Poda
        return best_value

# -------- Grafo del juego --------
G = nx.DiGraph()
G.add_nodes_from([
    (0, {"value": None}), (1, {"value": None}), (2, {"value": None}),
    (3, {"value": 3}), (4, {"value": 5}),
    (5, {"value": 2}), (6, {"value": 4})
])
G.add_edges_from([
    (0, 1), (0, 2),
    (1, 3), (1, 4),
    (2, 5), (2, 6)
])

# -------- Evaluación Alfa-Beta desde la raíz --------
optimal_value = alphabeta(G, 0, 3, float('-inf'), float('inf'), True)
print(f"Valor óptimo del nodo raíz: {optimal_value}")
