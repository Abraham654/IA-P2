import random

def hill_climbing(problema, estado_inicial, max_iter=1000):
    actual = estado_inicial
    valor_actual = problema.valor(actual)

    for _ in range(max_iter):
        vecinos = problema.vecinos(actual)
        if not vecinos: break  # Sin vecinos, se detiene

        mejor_vecino = None
        mejor_valor = -float('inf')  # Para maximizar

        for vecino in vecinos:
            v = problema.valor(vecino)
            if v > mejor_valor:
                mejor_vecino = vecino
                mejor_valor = v

        if mejor_valor <= valor_actual: break  # No mejora, fin

        actual = mejor_vecino
        valor_actual = mejor_valor

    return actual, valor_actual

class ProblemaTSP:
    def __init__(self, ciudades, distancias):
        self.ciudades = ciudades
        self.distancias = distancias

    def valor(self, ruta):
        total = sum(self.distancias[ruta[i]][ruta[i+1]] for i in range(len(ruta)-1))
        total += self.distancias[ruta[-1]][ruta[0]]  # Vuelta al inicio
        return -total  # Negativo para usarlo como maximización

    def vecinos(self, ruta):
        vecinos = []
        for i in range(len(ruta)):
            for j in range(i+1, len(ruta)):
                vecino = ruta.copy()
                vecino[i], vecino[j] = vecino[j], vecino[i]  # Intercambio
                vecinos.append(vecino)
        return vecinos

if __name__ == "__main__":
    ciudades = ['A', 'B', 'C', 'D']
    distancias = {
        'A': {'A': 0, 'B': 2, 'C': 9, 'D': 10},
        'B': {'A': 1, 'B': 0, 'C': 6, 'D': 4},
        'C': {'A': 15, 'B': 7, 'C': 0, 'D': 8},
        'D': {'A': 6, 'B': 3, 'C': 12, 'D': 0}
    }

    problema = ProblemaTSP(ciudades, distancias)
    ruta_inicial = ciudades.copy()
    random.shuffle(ruta_inicial)

    mejor_ruta, mejor_valor = hill_climbing(problema, ruta_inicial)

    print("Ruta inicial:", ruta_inicial)
    print("Longitud inicial:", -problema.valor(ruta_inicial))
    print("Mejor ruta:", mejor_ruta)
    print("Longitud óptima:", -mejor_valor)
