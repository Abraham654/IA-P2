import random
import heapq

def local_beam_search(problema, estados_iniciales, k=5, max_iter=1000):
    haz = [(problema.valor(e), e) for e in estados_iniciales]
    heapq.heapify(haz)                  # Ordenar por valor
    haz = heapq.nlargest(k, haz)       # Quedarse con los k mejores

    for _ in range(max_iter):
        vecinos = []
        for _, estado in haz:
            for v in problema.generar_vecinos(estado):
                vecinos.append((problema.valor(v), v))

        if not vecinos: break           # Si no hay vecinos, se detiene

        nuevo_haz = heapq.nlargest(k, vecinos)
        if nuevo_haz[0][0] == haz[0][0]: break  # Si no mejora, se detiene

        haz = nuevo_haz  # Actualiza el haz

    return haz[0][1], haz[0][0]         # Mejor estado y su valor

class ProblemaFuncion:
    def __init__(self, funcion):
        self.funcion = funcion

    def valor(self, x):
        return self.funcion(x)          # Evalúa f(x)

    def generar_vecinos(self, x, paso=0.1):
        return [x + random.uniform(-paso, paso) for _ in range(10)]  # 10 vecinos

if __name__ == "__main__":
    def funcion_obj(x): return -x**2 + 1.2*x  # Máximo cerca de x ≈ 0.6

    problema = ProblemaFuncion(funcion_obj)
    k = 3
    estados = [random.uniform(-10, 10) for _ in range(k)]

    mejor_x, mejor_valor = local_beam_search(problema, estados, k=k)

    print("Estados iniciales:", estados)
    print(f"Mejor solución: x = {mejor_x:.4f}, f(x) = {mejor_valor:.4f}")
