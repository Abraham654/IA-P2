import random
import networkx as nx
import numpy as np

def graph_partitioning_conditioning(G, cut_set):
    # Convierte el grafo a matriz de adyacencia
    adjacency_matrix = nx.to_numpy_array(G)

    # Suma de conexiones por nodo (grado)
    degrees = np.sum(adjacency_matrix, axis=1)

    # Suma de pesos de las aristas en el corte
    cut_weight = sum(G[u][v]['weight'] for u, v in cut_set)

    # Suma de grados por componente conectada
    partition_volumes = [sum(degrees[u] for u in subset) 
                         for subset in nx.connected_components(G)]

    # Volumen mínimo (evita división por cero)
    min_volume = min(partition_volumes)

    # Retorna el valor del acondicionamiento
    return cut_weight / min_volume if min_volume > 0 else float('inf')

# -------- Ejemplo --------
G = nx.Graph()
# Aristas con peso
G.add_edges_from([
    (0, 1, {'weight': 1}),
    (1, 2, {'weight': 2}),
    (2, 3, {'weight': 1}),
    (3, 0, {'weight': 3})
])

# Aristas que se consideran parte del corte
cut_set = [(1, 2), (2, 3)]

# Evaluación del corte
conditioning_value = graph_partitioning_conditioning(G, cut_set)
print(f"Acondicionamiento del corte: {conditioning_value}")
