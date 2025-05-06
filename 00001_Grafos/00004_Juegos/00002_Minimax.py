import networkx as nx

def minimax(G, node, depth, maximizing_player):
    # Si llegamos al límite o a una hoja, devolvemos su valor
    if depth == 0 or G.out_degree(node) == 0:
        return G.nodes[node]['value']
    
    if maximizing_player:
        # Jugador maximizador: elige el mayor valor entre los hijos
        return max(minimax(G, child, depth - 1, False) for child in G.successors(node))
    else:
        # Jugador minimizador: elige el menor valor entre los hijos
        return min(minimax(G, child, depth - 1, True) for child in G.successors(node))

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

# -------- Evaluación Minimax desde la raíz --------
optimal_value = minimax(G, 0, 3, True)
print(f"Valor óptimo del nodo raíz: {optimal_value}")
