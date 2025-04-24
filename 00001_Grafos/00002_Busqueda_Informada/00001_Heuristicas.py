import heapq  # Cola de prioridad (min-heap)

def busqueda_a_estrella(grafo, inicio, objetivo, heuristica):
    frontera = []  # Cola de prioridad: (f_score, nodo)
    heapq.heappush(frontera, (heuristica(inicio, objetivo), inicio))

    g_scores = {inicio: 0}      # Costo real desde el inicio
    padres = {inicio: None}     # Registro de padres para reconstruir camino

    while frontera:
        _, actual = heapq.heappop(frontera)  # Nodo con menor f_score

        if actual == objetivo:
            camino = []
            while actual is not None:
                camino.append(actual)
                actual = padres[actual]
            return camino[::-1], g_scores[camino[0]]  # Camino y costo total

        for vecino, costo in grafo[actual].items():
            g_tentativo = g_scores[actual] + costo
            if vecino not in g_scores or g_tentativo < g_scores[vecino]:
                padres[vecino] = actual
                g_scores[vecino] = g_tentativo
                f_score = g_tentativo + heuristica(vecino, objetivo)
                heapq.heappush(frontera, (f_score, vecino))

    return None, None  # No se encontró camino

def heuristica_manhattan(nodo, objetivo):
    x1, y1 = nodo
    x2, y2 = objetivo
    return abs(x1 - x2) + abs(y1 - y2)

if __name__ == "__main__":
    grafo = {
        (0, 0): {(0, 1): 1, (1, 0): 1},
        (0, 1): {(0, 0): 1, (0, 2): 1, (1, 1): 1.5},
        (0, 2): {(0, 1): 1, (1, 2): 1},
        (1, 0): {(0, 0): 1, (1, 1): 1, (2, 0): 1},
        (1, 1): {(0, 1): 1.5, (1, 0): 1, (1, 2): 1, (2, 1): 1},
        (1, 2): {(0, 2): 1, (1, 1): 1, (2, 2): 1},
        (2, 0): {(1, 0): 1, (2, 1): 1},
        (2, 1): {(1, 1): 1, (2, 0): 1, (2, 2): 1},
        (2, 2): {(1, 2): 1, (2, 1): 1}
    }

    inicio, objetivo = (0, 0), (2, 2)
    camino, costo = busqueda_a_estrella(grafo, inicio, objetivo, heuristica_manhattan)

    print("Camino encontrado:", camino)
    print("Costo total:", costo)
