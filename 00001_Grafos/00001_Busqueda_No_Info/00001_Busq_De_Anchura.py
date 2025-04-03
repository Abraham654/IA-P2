from collections import deque

def busqueda_anchura(grafo, inicio, objetivo):
    """
    Implementación del algoritmo de Búsqueda en Anchura (BFS)
    
    Args:
        grafo (dict): Grafo representado como diccionario de listas de adyacencia
        inicio: Nodo inicial de la búsqueda
        objetivo: Nodo que queremos encontrar
    
    Returns:
        list: Camino desde el inicio hasta el objetivo, o None si no se encuentra
    """
    # Cola para los nodos a explorar
    cola = deque()
    cola.append(inicio)
    
    # Diccionario para registrar nodos visitados y sus predecesores
    visitados = {inicio: None}
    
    while cola:
        nodo_actual = cola.popleft()
        
        # Si encontramos el objetivo, reconstruimos el camino
        if nodo_actual == objetivo:
            camino = []
            while nodo_actual is not None:
                camino.append(nodo_actual)
                nodo_actual = visitados[nodo_actual]
            return camino[::-1]  # Invertimos el camino para que vaya de inicio a objetivo
        
        # Exploramos los vecinos del nodo actual
        for vecino in grafo[nodo_actual]:
            if vecino not in visitados:
                cola.append(vecino)
                visitados[vecino] = nodo_actual
    
    # Si la cola se vacía sin encontrar el objetivo
    return None

# Ejemplo de uso
if __name__ == "__main__":
    # Grafo de ejemplo (diccionario de listas de adyacencia)
    grafo = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }
    
    inicio = 'A'
    objetivo = 'F'
    
    print(f"Buscando camino desde {inicio} hasta {objetivo}...")
    camino = busqueda_anchura(grafo, inicio, objetivo)
    
    if camino:
        print("Camino encontrado:", " -> ".join(camino))
    else:
        print(f"No se encontró un camino desde {inicio} hasta {objetivo}")