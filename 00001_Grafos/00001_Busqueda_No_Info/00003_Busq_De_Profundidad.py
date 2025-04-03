def busqueda_profundidad(grafo, inicio, objetivo):
    """
    Implementación del algoritmo de Búsqueda en Profundidad (DFS) usando una pila
    
    Args:
        grafo (dict): Grafo representado como diccionario de listas de adyacencia
        inicio: Nodo inicial de la búsqueda
        objetivo: Nodo que queremos encontrar
    
    Returns:
        list: Camino desde el inicio hasta el objetivo, o None si no se encuentra
    """
    # Pila para los nodos a explorar (último en entrar, primero en salir)
    pila = [(inicio, [inicio])]
    visitados = set()
    
    while pila:
        nodo_actual, camino = pila.pop()
        
        if nodo_actual == objetivo:
            return camino
        
        if nodo_actual not in visitados:
            visitados.add(nodo_actual)
            
            # Añadimos los vecinos a la pila (en orden inverso para procesar en orden)
            for vecino in reversed(grafo[nodo_actual]):
                if vecino not in visitados:
                    pila.append((vecino, camino + [vecino]))
    
    return None

# Versión recursiva alternativa
def busqueda_profundidad_recursiva(grafo, inicio, objetivo, visitados=None, camino=None):
    """
    Versión recursiva de DFS (menos eficiente para grafos grandes)
    """
    if visitados is None:
        visitados = set()
    if camino is None:
        camino = []
    
    visitados.add(inicio)
    camino = camino + [inicio]
    
    if inicio == objetivo:
        return camino
    
    for vecino in grafo[inicio]:
        if vecino not in visitados:
            resultado = busqueda_profundidad_recursiva(grafo, vecino, objetivo, visitados, camino)
            if resultado is not None:
                return resultado
    
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
    
    print("Versión iterativa:")
    print(f"Buscando camino desde {inicio} hasta {objetivo}...")
    camino = busqueda_profundidad(grafo, inicio, objetivo)
    
    if camino:
        print("Camino encontrado:", " -> ".join(camino))
    else:
        print(f"No se encontró un camino desde {inicio} hasta {objetivo}")
    
    print("\nVersión recursiva:")
    print(f"Buscando camino desde {inicio} hasta {objetivo}...")
    camino_rec = busqueda_profundidad_recursiva(grafo, inicio, objetivo)
    
    if camino_rec:
        print("Camino encontrado:", " -> ".join(camino_rec))
    else:
        print(f"No se encontró un camino desde {inicio} hasta {objetivo}")