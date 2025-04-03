def busqueda_profundidad_iterativa(grafo, inicio, objetivo):
    """
    Implementación del algoritmo de Búsqueda en Profundidad Iterativa (IDDFS)
    que combina las ventajas de BFS y DFS.
    
    Args:
        grafo (dict): Grafo representado como diccionario de listas de adyacencia
        inicio: Nodo inicial de la búsqueda
        objetivo: Nodo que queremos encontrar
    
    Returns:
        list: Camino desde el inicio hasta el objetivo, o None si no se encuentra
    """
    # Función auxiliar de búsqueda en profundidad limitada (DLS)
    def dls(nodo_actual, objetivo, limite):
        if nodo_actual == objetivo:
            return [nodo_actual]
        
        if limite <= 0:
            return None
        
        for vecino in grafo[nodo_actual]:
            resultado = dls(vecino, objetivo, limite - 1)
            if resultado is not None:
                return [nodo_actual] + resultado
        return None
    
    # Incrementamos progresivamente el límite de profundidad
    profundidad = 0
    while True:
        resultado = dls(inicio, objetivo, profundidad)
        if resultado is not None:
            return resultado
        profundidad += 1

# Versión alternativa con seguimiento de camino y visitados
def iddfs_completo(grafo, inicio, objetivo):
    """
    Versión más completa de IDDFS con seguimiento de camino y nodos visitados
    """
    profundidad = 0
    while True:
        visitados = set()
        pila = [(inicio, [inicio], 0)]
        encontrado = None
        
        while pila:
            nodo, camino, nivel = pila.pop()
            
            if nodo == objetivo:
                encontrado = camino
                break
            
            if nivel < profundidad:
                if nodo not in visitados:
                    visitados.add(nodo)
                    for vecino in reversed(grafo[nodo]):
                        if vecino not in visitados:
                            pila.append((vecino, camino + [vecino], nivel + 1))
        
        if encontrado is not None:
            return encontrado
        if not pila and nivel >= profundidad:
            break
        profundidad += 1
    
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
    
    print("Versión básica:")
    print(f"Buscando camino desde {inicio} hasta {objetivo}...")
    camino = busqueda_profundidad_iterativa(grafo, inicio, objetivo)
    
    if camino:
        print("Camino encontrado:", " -> ".join(camino))
    else:
        print(f"No se encontró un camino desde {inicio} hasta {objetivo}")
    
    print("\nVersión completa con seguimiento de visitados:")
    camino_completo = iddfs_completo(grafo, inicio, objetivo)
    
    if camino_completo:
        print("Camino encontrado:", " -> ".join(camino_completo))
    else:
        print(f"No se encontró un camino desde {inicio} hasta {objetivo}")