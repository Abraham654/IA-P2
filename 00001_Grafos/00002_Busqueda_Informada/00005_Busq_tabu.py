import random
from collections import deque

def tabu_search(problema, estado_inicial, max_iter=1000, tamano_tabu=10):
    actual = estado_inicial
    mejor_estado = actual
    mejor_valor = problema.valor(actual)

    lista_tabu = deque(maxlen=tamano_tabu)  # Lista tabú con tamaño fijo

    for _ in range(max_iter):
        vecinos = problema.vecinos(actual)
        if not vecinos: break

        mejor_vecino = None
        mejor_valor_vecino = -float('inf')

        # Selecciona mejor vecino no tabú
        for vecino in vecinos:
            if vecino not in lista_tabu:
                val = problema.valor(vecino)
                if val > mejor_valor_vecino:
                    mejor_vecino = vecino
                    mejor_valor_vecino = val

        # Si todos los vecinos son tabú, toma el mejor de todos
        if mejor_vecino is None:
            mejor_vecino = max(vecinos, key=problema.valor)
            mejor_valor_vecino = problema.valor(mejor_vecino)

        actual = mejor_vecino
        lista_tabu.append(actual)  # Agrega a la lista tabú

        if mejor_valor_vecino > mejor_valor:
            mejor_estado = mejor_vecino
            mejor_valor = mejor_valor_vecino

    return mejor_estado, mejor_valor

class ProblemaMochila:
    def __init__(self, items, capacidad):
        self.items = items              # (valor, peso)
        self.capacidad = capacidad

    def valor(self, solucion):
        val, peso = 0, 0
        for i, usar in enumerate(solucion):
            if usar:
                val += self.items[i][0]
                peso += self.items[i][1]
        return val if peso <= self.capacidad else 0

    def vecinos(self, solucion):
        vecinos = []
        for i in range(len(solucion)):
            copia = solucion.copy()
            copia[i] = 1 - copia[i]  # Flip bit
            vecinos.append(copia)
        return vecinos

if __name__ == "__main__":
    items = [(60, 10), (100, 20), (120, 30)]
    capacidad = 50
    problema = ProblemaMochila(items, capacidad)

    inicial = [random.randint(0, 1) for _ in items]
    mejor_sol, mejor_val = tabu_search(problema, inicial)

    print("Solución inicial:", inicial)
    print("Valor inicial:", problema.valor(inicial))
    print("\nMejor solución:", mejor_sol)
    print("Valor óptimo:", mejor_val)
