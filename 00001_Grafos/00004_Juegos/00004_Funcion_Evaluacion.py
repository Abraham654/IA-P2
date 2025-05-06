import networkx as nx

def evaluation_function(G, node):
    # Si el nodo ya tiene un valor, se devuelve directamente
    if 'value' in G.nodes[node]:
        return G.nodes[node]['value']
    
    # Extrae los valores definidos de los vecinos
    neighbor_values = [G.nodes[n]['value'] for n in G.neighbors(node) if 'value' in G.nodes[n]]
    
    # Si no hay vecinos con valor, devuelve 0
    if not neighbor_values:
        return 0

    # Calcula el promedio de los valores vecinos
    eval_value = sum(neighbor_values) / len(neighbor_values)
    return eval_value

# -------- Grafo del juego --------
G = nx.Graph()
G.add_nodes_from([
    (0, {"value": None}), (1, {"value": 4}), (2, {"value": 6}),
    (3, {"value": None}), (4, {"value": 3}), (5, {"value": 5})
])
G.add_edges_from([
    (0, 1), (0, 2), (0, 3),
    (3, 4), (3, 5)
])

# -------- Evaluación de nodos --------
node_eval_0 = evaluation_function(G, 0)
print(f"Valor de evaluación del nodo 0: {node_eval_0}")

node_eval_3 = evaluation_function(G, 3)
print(f"Valor de evaluación del nodo 3: {node_eval_3}")
