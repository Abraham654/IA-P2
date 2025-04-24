import heapq  # Cola de prioridad (para elegir el nodo con menor heurística)

def busqueda_voraz(grafo, inicio, objetivo, heuristica):
    frontera = []  # Cola: (h(n), nodo)
    heapq.heappush(frontera, (heuristica(inicio, objetivo), inicio))

    padres = {inicio: None}  # Para reconstruir camino
    visitados = set()        # Para evitar reprocesar nodos

    while frontera:
        _, actual = heapq.heappop(frontera)  # Saca el nodo más prometedor (menor h)

        if actual == objetivo:
            camino = []
            while actual:
                camino.append(actual)
                actual = padres[actual]
            return camino[::-1]  # De inicio a objetivo

        if actual in visitados:
            continue  # Saltar si ya fue expandido

        visitados.add(actual)

        for vecino in grafo[actual]:
            if vecino not in visitados and vecino not in padres:
                padres[vecino] = actual
                heapq.heappush(frontera, (heuristica(vecino, objetivo), vecino))

    return None  # No se encontró camino

def heuristica_euclidiana(nodo, objetivo):
    x1, y1 = nodo
    x2, y2 = objetivo
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

if __name__ == "__main__":
    grafo = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E', 'G'],
        'G': ['F']
    }

    coordenadas = {
        'A': (0, 0),
        'B': (1, 2),
        'C': (4, 0),
        'D': (1, 4),
        'E': (3, 3),
        'F': (4, 2),
        'G': (5, 5)
    }

    def h(nodo, objetivo):
        return heuristica_euclidiana(coordenadas[nodo], coordenadas[objetivo])

    inicio, objetivo = 'A', 'G'
    camino = busqueda_voraz(grafo, inicio, objetivo, h)

    print("Camino encontrado:", camino)
