import heapq
import math

class BusquedaOnline:
    def __init__(self, grafo, heuristica):
        self.grafo = grafo                # Grafo de nodos y costos
        self.heuristica = heuristica      # h(n, objetivo)
        self.H = {}                       # Heurísticas aprendidas

    def lrta_star(self, inicio, objetivo):
        actual = inicio
        camino = [actual]

        while actual != objetivo:
            if actual not in self.H:
                self.H[actual] = self.heuristica(actual, objetivo)

            mejor_valor = math.inf
            mejor_vecino = None

            for vecino, costo in self.grafo[actual].items():
                h_vecino = self.H.get(vecino, self.heuristica(vecino, objetivo))
                valor = costo + h_vecino

                if valor < mejor_valor:
                    mejor_valor = valor
                    mejor_vecino = vecino

            self.H[actual] = mejor_valor  # Actualiza h(n) usando min
            actual = mejor_vecino
            camino.append(actual)

        return camino

if __name__ == "__main__":
    grafo = {
        'A': {'B': 1, 'D': 1},
        'B': {'A': 1, 'C': 1, 'E': 1},
        'C': {'B': 1, 'F': 1},
        'D': {'A': 1, 'E': 1},
        'E': {'B': 1, 'D': 1, 'F': 1, 'G': 1},
        'F': {'C': 1, 'E': 1, 'H': 1},
        'G': {'E': 1, 'H': 1},
        'H': {'F': 1, 'G': 1}
    }

    def h(nodo, objetivo):
        coords = {
            'A': (0,0), 'B': (1,0), 'C': (2,0),
            'D': (0,1), 'E': (1,1), 'F': (2,1),
            'G': (1,2), 'H': (2,2)
        }
        x1, y1 = coords[nodo]
        x2, y2 = coords[objetivo]
        return abs(x1 - x2) + abs(y1 - y2)

    buscador = BusquedaOnline(grafo, h)
    camino = buscador.lrta_star('A', 'H')

    print("Camino encontrado:", camino)
    print("Heurística aprendida:", buscador.H)
