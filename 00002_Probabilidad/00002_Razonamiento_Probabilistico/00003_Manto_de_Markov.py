import networkx as nx

def obtener_manto_markov(grafo, nodo):
    # Padres directos del nodo
    padres = set(grafo.predecessors(nodo))
    # Hijos directos del nodo
    hijos = set(grafo.successors(nodo))
    # Padres de los hijos (co-padres)
    co_padres = set()
    for hijo in hijos:
        co_padres.update(grafo.predecessors(hijo))
    # Manto = padres + hijos + co-padres, sin incluir el nodo
    manto = padres | hijos | co_padres
    manto.discard(nodo)
    return manto

# Crear grafo dirigido representando una red bayesiana
G = nx.DiGraph()
G.add_edges_from([
    ('A', 'C'),  # A → C
    ('B', 'C'),  # B → C
    ('C', 'E'),  # C → E
    ('D', 'E'),  # D → E
    ('F', 'D'),  # F → D
    ('G', 'F')   # G → F
])

# Calcular y mostrar manto de Markov para cada nodo objetivo
for nodo in ['C', 'E', 'F']:
    manto = obtener_manto_markov(G, nodo)
    print(f"Manto de Markov de '{nodo}': {sorted(manto)}")
