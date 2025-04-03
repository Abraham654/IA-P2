def busqueda_profundidad_limitada(grafo, inicio, objetivo, limite):
    """
    Implementación del algoritmo de Búsqueda en Profundidad Limitada (DLS)
    
    Args:
        grafo (dict): Grafo representado como diccionario de listas de adyacencia
        inicio: Nodo inicial de la búsqueda
        objetivo: Nodo que queremos encontrar
        limite (int): Profundidad máxima de búsqueda
    
    Returns:
        list: Camino desde el inicio hasta el objetivo, o None si no se encuentra
    """
    # Versión iterativa usando una pila que almacena (nodo, camino, profundidad)
    pila = [(inicio, [inicio], 0)]
    visitados = set()
    
    while pila:
        nodo_actual, camino, profundidad = pila.pop()
        
        if nodo_actual == objetivo:
            return camino
        
        if nodo_actual not in visitados and profundidad < limite:
            visitados.add(nodo_actual)
            
            # Añadimos los vecinos a la pila (en orden inverso para procesar en orden)
            for vecino in reversed(grafo[nodo_actual]):
                if vecino not in visitados:
                    pila.append((vecino, camino + [vecino], profundidad + 1))
    
    return None

# Versión recursiva alternativa
def dls_recursiva(grafo, nodo, objetivo, limite, visitados=None, camino=None):
    """
    Versión recursiva de DLS
    """
    if visitados is None:
        visitados = set()
    if camino is None:
        camino = []
    
    visitados.add(nodo)
    camino = camino + [nodo]
    
    if nodo == objetivo:
        return camino
    
    if limite <= 0:
        return None
    
    for vecino in grafo[nodo]:
        if vecino not in visitados:
            resultado = dls_recursiva(grafo, vecino, objetivo, limite-1, visitados, camino)
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
    limite_profundidad = 3
    
    print("Versión iterativa:")
    print(f"Buscando camino desde {inicio} hasta {objetivo} con límite {limite_profundidad}...")
    camino = busqueda_profundidad_limitada(grafo, inicio, objetivo, limite_profundidad)
    
    if camino:
        print("Camino encontrado:", " -> ".join(camino))
    else:
        print(f"No se encontró un camino dentro del límite de profundidad {limite_profundidad}")
    
    print("\nVersión recursiva:")
    print(f"Buscando camino desde {inicio} hasta {objetivo} con límite {limite_profundidad}...")
    camino_rec = dls_recursiva(grafo, inicio, objetivo, limite_profundidad)
    
    if camino_rec:
        print("Camino encontrado:", " -> ".join(camino_rec))
    else:
        print(f"No se encontró un camino dentro del límite de profundidad {limite_profundidad}")