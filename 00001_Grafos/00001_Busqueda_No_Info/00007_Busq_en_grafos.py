from collections import deque  # Cola doble para manejar FIFO (BFS) o LIFO (DFS)

def busqueda_grafo(grafo, inicio, objetivo, estrategia='bfs'):
    if inicio == objetivo:
        return [inicio]  # Caso trivial

    cola = deque([inicio])         # Cola para BFS o pila para DFS
    visitados = {inicio: None}     # Guarda nodos visitados y su predecesor

    while cola:
        # Extrae nodo según estrategia: BFS usa popleft, DFS usa pop
        actual = cola.popleft() if estrategia == 'bfs' else cola.pop()

        if actual == objetivo:
            camino = []
            while actual is not None:
                camino.append(actual)
                actual = visitados[actual]
            return camino[::-1]  # Invertir para ir de inicio a objetivo

        for vecino in grafo.get(actual, []):  # .get() evita errores si no tiene vecinos
            if vecino not in visitados:
                visitados[vecino] = actual
                cola.append(vecino)  # Mismo método para BFS y DFS

    return None  # No se encontró camino

# Ejemplo
if __name__ == "__main__":
    grafo = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }

    inicio, objetivo = 'A', 'F'

    print("BFS (Anchura):")
    print("Camino:", busqueda_grafo(grafo, inicio, objetivo, 'bfs'))

    print("\nDFS (Profundidad):")
    print("Camino:", busqueda_grafo(grafo, inicio, objetivo, 'dfs'))
