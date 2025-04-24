from collections import deque  # Estructura eficiente para manejar la cola

def busqueda_anchura(grafo, inicio, objetivo):
    cola = deque([inicio])             # Cola FIFO con el nodo inicial
    visitados = {inicio: None}         # Almacena nodos visitados y sus padres

    while cola:
        actual = cola.popleft()        # Sacamos el primer nodo en la cola

        if actual == objetivo:         # Si encontramos el objetivo, reconstruimos el camino
            camino = []
            while actual is not None:
                camino.append(actual)
                actual = visitados[actual]
            return camino[::-1]        # Se invierte para ir de inicio a objetivo

        for vecino in grafo[actual]:   # Exploramos vecinos no visitados
            if vecino not in visitados:
                cola.append(vecino)
                visitados[vecino] = actual

    return None  # Si no se encuentra el objetivo

# Ejemplo de uso
if __name__ == "__main__":
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
    camino = busqueda_anchura(grafo, inicio, objetivo)

    if camino:
        print("Camino encontrado:", " -> ".join(camino))
    else:
        print("Camino no encontrado")
