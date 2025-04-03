import heapq

def busqueda_costo_uniforme(grafo, inicio, objetivo):
    """
    Implementación del algoritmo de Búsqueda de Costo Uniforme (UCS)
    que expande el nodo con el menor costo acumulado.
    
    Args:
        grafo (dict): Grafo representado como diccionario de listas de tuplas (nodo, costo)
        inicio: Nodo inicial de la búsqueda
        objetivo: Nodo que queremos encontrar
    
    Returns:
        tuple: (costo_total, camino) desde el inicio hasta el objetivo, o None si no se encuentra
    """
    # Cola de prioridad para los nodos a explorar, ordenados por costo acumulado
    cola_prioridad = []
    heapq.heappush(cola_prioridad, (0, inicio))
    
    # Diccionario para registrar nodos visitados y sus predecesores y costos
    visitados = {inicio: (None, 0)}
    
    while cola_prioridad:
        costo_acumulado, nodo_actual = heapq.heappop(cola_prioridad)
        
        # Si encontramos el objetivo, reconstruimos el camino
        if nodo_actual == objetivo:
            camino = []
            while nodo_actual is not None:
                camino.append(nodo_actual)
                nodo_actual, _ = visitados[nodo_actual]
            return (costo_acumulado, camino[::-1])  # Invertimos el camino
        
        # Exploramos los vecinos del nodo actual
        for vecino, costo in grafo[nodo_actual]:
            nuevo_costo = costo_acumulado + costo
            
            # Si el vecino no ha sido visitado o encontramos un camino más barato
            if vecino not in visitados or nuevo_costo < visitados[vecino][1]:
                heapq.heappush(cola_prioridad, (nuevo_costo, vecino))
                visitados[vecino] = (nodo_actual, nuevo_costo)
    
    # Si la cola se vacía sin encontrar el objetivo
    return None

# Ejemplo de uso
if __name__ == "__main__":
    # Grafo de ejemplo con costos (diccionario de listas de tuplas (nodo, costo))
    grafo = {
        'A': [('B', 1), ('C', 4)],
        'B': [('A', 1), ('D', 5), ('E', 2)],
        'C': [('A', 4), ('F', 3)],
        'D': [('B', 5)],
        'E': [('B', 2), ('F', 1)],
        'F': [('C', 3), ('E', 1)]
    }
    
    inicio = 'A'
    objetivo = 'F'
    
    print(f"Buscando camino de menor costo desde {inicio} hasta {objetivo}...")
    resultado = busqueda_costo_uniforme(grafo, inicio, objetivo)
    
    if resultado:
        costo, camino = resultado
        print(f"Camino encontrado (costo total: {costo}):", " -> ".join(camino))
    else:
        print(f"No se encontró un camino desde {inicio} hasta {objetivo}")