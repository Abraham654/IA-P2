import random
import heapq
from copy import deepcopy

def algoritmo_genetico(problema, tam_poblacion=50, max_generaciones=100, prob_cruce=0.8, prob_mutacion=0.1):
    poblacion = [problema.crear_individuo() for _ in range(tam_poblacion)]

    for _ in range(max_generaciones):
        evaluaciones = [(problema.fitness(ind), ind) for ind in poblacion]

        # Selección por torneo binario
        padres = []
        for _ in range(tam_poblacion):
            a, b = random.sample(evaluaciones, 2)
            padres.append(a if a[0] > b[0] else b)

        nueva_poblacion = []
        for i in range(0, tam_poblacion, 2):
            p1 = padres[i][1]
            p2 = padres[i+1][1] if i+1 < tam_poblacion else padres[0][1]

            # Cruce con probabilidad
            if random.random() < prob_cruce:
                hijo1, hijo2 = problema.cruzar(deepcopy(p1), deepcopy(p2))
            else:
                hijo1, hijo2 = deepcopy(p1), deepcopy(p2)

            # Mutación con probabilidad
            if random.random() < prob_mutacion:
                hijo1 = problema.mutar(hijo1)
            if random.random() < prob_mutacion:
                hijo2 = problema.mutar(hijo2)

            nueva_poblacion.extend([hijo1, hijo2])

        # Reemplazo por elitismo (mejores k)
        evaluaciones = [(problema.fitness(ind), ind) for ind in nueva_poblacion]
        poblacion = [ind for (_, ind) in heapq.nlargest(tam_poblacion, evaluaciones)]

    mejor = max([(problema.fitness(ind), ind) for ind in poblacion])
    return mejor[1], mejor[0]

class ProblemaTSP:
    def __init__(self, ciudades, distancias):
        self.ciudades = ciudades
        self.distancias = distancias

    def crear_individuo(self):
        ind = self.ciudades.copy()
        random.shuffle(ind)
        return ind

    def fitness(self, ind):
        total = sum(self.distancias[ind[i]][ind[(i+1) % len(ind)]] for i in range(len(ind)))
        return -total  # Negativo para maximizar

    def cruzar(self, p1, p2):
        size = len(p1)
        a, b = sorted(random.sample(range(size), 2))
        h1, h2 = p1[a:b], p2[a:b]
        for x in [p2, p1]:
            for ciudad in x:
                if ciudad not in h1 and len(h1) < size:
                    h1.append(ciudad)
                if ciudad not in h2 and len(h2) < size:
                    h2.append(ciudad)
        return h1, h2

    def mutar(self, ind):
        i, j = random.sample(range(len(ind)), 2)
        ind[i], ind[j] = ind[j], ind[i]
        return ind

if __name__ == "__main__":
    ciudades = ['A', 'B', 'C', 'D']
    distancias = {
        'A': {'A': 0, 'B': 2, 'C': 9, 'D': 10},
        'B': {'A': 2, 'B': 0, 'C': 6, 'D': 4},
        'C': {'A': 9, 'B': 6, 'C': 0, 'D': 8},
        'D': {'A': 10, 'B': 4, 'C': 8, 'D': 0}
    }

    problema = ProblemaTSP(ciudades, distancias)
    mejor_ruta, mejor_val = algoritmo_genetico(problema)

    print("Mejor ruta:", mejor_ruta)
    print("Distancia total:", -mejor_val)
