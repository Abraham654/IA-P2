import random
import math

def simulated_annealing(problema, estado_inicial, temp_inicial=1000, enfriamiento=0.95, iter_por_temp=100, temp_final=0.1):
    actual = estado_inicial
    mejor_estado = actual
    mejor_valor = problema.valor(actual)
    temp = temp_inicial

    while temp > temp_final:
        for _ in range(iter_por_temp):
            vecino = problema.vecino_aleatorio(actual)
            delta = problema.valor(vecino) - problema.valor(actual)

            # Acepta si mejora o con probabilidad (si es peor)
            if delta > 0 or random.random() < math.exp(delta / temp):
                actual = vecino

            if problema.valor(actual) > mejor_valor:
                mejor_estado = actual
                mejor_valor = problema.valor(actual)

        temp *= enfriamiento  # Reduce la temperatura

    return mejor_estado, mejor_valor

class ProblemaTSP:
    def __init__(self, ciudades, distancias):
        self.ciudades = ciudades
        self.distancias = distancias

    def valor(self, ruta):
        total = sum(self.distancias[ruta[i]][ruta[i+1]] for i in range(len(ruta)-1))
        total += self.distancias[ruta[-1]][ruta[0]]  # Regresa al inicio
        return -total  # Negativo para maximizar

    def vecino_aleatorio(self, ruta):
        vecino = ruta.copy()
        i, j = random.sample(range(len(ruta)), 2)
        vecino[i], vecino[j] = vecino[j], vecino[i]  # Swap
        return vecino

if __name__ == "__main__":
    ciudades = ['A', 'B', 'C', 'D']
    distancias = {
        'A': {'B': 2, 'C': 9, 'D': 10},
        'B': {'A': 2, 'C': 6, 'D': 4},
        'C': {'A': 9, 'B': 6, 'D': 8},
        'D': {'A': 10, 'B': 4, 'C': 8}
    }

    problema = ProblemaTSP(ciudades, distancias)
    ruta_inicial = ciudades.copy()
    random.shuffle(ruta_inicial)

    mejor_ruta, mejor_valor = simulated_annealing(problema, ruta_inicial)

    print("Ruta inicial:", ruta_inicial, f"(Distancia: {-problema.valor(ruta_inicial)})")
    print("Mejor ruta:", mejor_ruta, f"(Distancia: {-mejor_valor})")
