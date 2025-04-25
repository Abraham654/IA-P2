import heapq

def a_star(grafo, inicio, objetivo, heuristica):
    frontera = []  # Cola: (f_score, nodo)
    heapq.heappush(frontera, (heuristica(inicio, objetivo), inicio))
    g_score = {inicio: 0}    # Costo real desde el inicio
    padres = {inicio: None}  # Rutas óptimas

    while frontera:
        _, actual = heapq.heappop(frontera)

        if actual == objetivo:
            camino = []
            while actual:
                camino.append(actual)
                actual = padres[actual]
            return camino[::-1], g_score[objetivo]

        for vecino, costo in grafo[actual].items():
            g_tentativo = g_score[actual] + costo
            if vecino not in g_score or g_tentativo < g_score[vecino]:
                padres[vecino] = actual
                g_score[vecino] = g_tentativo
                f_score = g_tentativo + heuristica(vecino, objetivo)
                heapq.heappush(frontera, (f_score, vecino))

    return None, None

def ao_star(grafo, inicio, objetivo, heuristica):
    solucion = {objetivo: (0, [objetivo])}
    expandido = set()

    def costo(nodo):
        if nodo in solucion:
            return solucion[nodo][0]

        if nodo in grafo:
            if isinstance(grafo[nodo], dict):  # OR
                mejor, camino = float('inf'), None
                for hijo, c in grafo[nodo].items():
                    total = c + costo(hijo)
                    if total < mejor:
                        mejor = total
                        camino = [nodo] + solucion[hijo][1]
                solucion[nodo] = (mejor, camino)
                return mejor
            else:  # AND
                total, camino = 0, [nodo]
                for conjunto in grafo[nodo]:
                    mejor, subcamino = float('inf'), []
                    for subnodo in conjunto:
                        val = conjunto[subnodo] + costo(subnodo)
                        if val < mejor:
                            mejor = val
                            subcamino = solucion[subnodo][1]
                    total += mejor
                    camino += subcamino
                solucion[nodo] = (total, camino)
                return total

        solucion[nodo] = (float('inf'), None)
        return float('inf')

    while inicio not in solucion or solucion[inicio][0] == float('inf'):
        nodo = inicio
        while True:
            if nodo not in expandido:
                break
            if nodo not in solucion or not solucion[nodo][1]:
                return None, None
            camino = solucion[nodo][1]
            nodo = camino[1] if len(camino) > 1 else None
            if nodo is None:
                return None, None

        expandido.add(nodo)
        costo(nodo)

    return solucion[inicio][1], solucion[inicio][0]

# Grafo para A*
grafo_a = {
    'A': {'B': 1, 'C': 3},
    'B': {'D': 2, 'E': 4},
    'C': {'F': 2},
    'D': {},
    'E': {'F': 1},
    'F': {}
}

def h_simple(n, objetivo): return 0  # Heurística nula

camino, costo = a_star(grafo_a, 'A', 'F', h_simple)
print(f"A*: Camino {camino}, Costo {costo}")

# Grafo para AO* con nodos AND-OR
grafo_ao = {
    'A': {'B': 1, 'C': 3},
    'B': [{'D': 2}, {'E': 4}],
    'C': {'F': 2},
    'D': {},
    'E': {'F': 1},
    'F': {}
}

camino_ao, costo_ao = ao_star(grafo_ao, 'A', 'F', h_simple)
print(f"AO*: Camino {camino_ao}, Costo {costo_ao}")
