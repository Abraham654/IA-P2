import numpy as np
from collections import defaultdict

# Algoritmo de búsqueda directa de política para grafos
class PolicySearch:
    def __init__(self, n_estados, n_acciones, gamma=0.95):
        self.politica = np.random.randint(n_acciones, size=n_estados)  # política inicial aleatoria
        self.V = np.zeros(n_estados)  # valores por estado
        self.n_estados = n_estados
        self.n_acciones = n_acciones
        self.gamma = gamma  # factor de descuento

    def evaluacion_politica(self, entorno, theta=1e-5):
        while True:
            delta = 0
            for s in range(self.n_estados):
                v = self.V[s]
                a = self.politica[s]
                resultados = entorno.resultados_posibles(s, a)
                self.V[s] = sum(p * (r + self.gamma * self.V[sig]) for sig, p, r in resultados)
                delta = max(delta, abs(v - self.V[s]))
            if delta < theta:
                break  # converge

    def mejora_politica(self, entorno):
        estable = True
        for s in range(self.n_estados):
            mejor_a = self.politica[s]
            valores = np.zeros(self.n_acciones)
            for a in range(self.n_acciones):
                resultados = entorno.resultados_posibles(s, a)
                valores[a] = sum(p * (r + self.gamma * self.V[sig]) for sig, p, r in resultados)
            nueva_a = np.argmax(valores)
            if mejor_a != nueva_a:
                estable = False
            self.politica[s] = nueva_a
        return estable  # True si ya no hay cambios

    def iteracion_politica(self, entorno):
        while True:
            self.evaluacion_politica(entorno)
            if self.mejora_politica(entorno):
                break  # termina cuando la política no cambia

# Entorno representado como grafo dirigido con transiciones probabilísticas
class GrafoEntorno:
    def __init__(self):
        self.n_estados = 5
        self.n_acciones = 5
        # cada estado tiene acciones con listas de (probabilidad, estado_sig, recompensa)
        self.grafo = {
            0: {1: [(0.8, 1, 2), (0.2, 2, -1)], 0: [(1.0, 0, -1)], 2: [(1.0, 2, -1)], 3: [(1.0, 3, 0)], 4: [(1.0, 4, 0)]},
            1: {1: [(0.7, 3, 1), (0.3, 4, 5)], 0: [(1.0, 1, 0)], 2: [(1.0, 2, 0)], 3: [(1.0, 3, 0)], 4: [(1.0, 4, 0)]},
            2: {1: [(0.6, 0, -1), (0.4, 3, 3)], 0: [(1.0, 2, 0)], 2: [(1.0, 2, 0)], 3: [(1.0, 3, 0)], 4: [(1.0, 4, 0)]},
            3: {1: [(1.0, 4, 10)], 0: [(1.0, 3, 0)], 2: [(1.0, 3, 0)], 3: [(1.0, 3, 0)], 4: [(1.0, 4, 0)]},
            4: {0: [(1.0, 4, 0)], 1: [(1.0, 4, 0)], 2: [(1.0, 4, 0)], 3: [(1.0, 4, 0)], 4: [(1.0, 4, 0)]}
        }

    def resultados_posibles(self, estado, accion):
        if estado in self.grafo and accion in self.grafo[estado]:
            return [(s, p, r) for p, s, r in self.grafo[estado][accion]]
        return [(estado, 1.0, -10)]  # penaliza acción inválida

# Prueba del algoritmo
if __name__ == "__main__":
    entorno = GrafoEntorno()
    agente = PolicySearch(entorno.n_estados, entorno.n_acciones)

    print("Política inicial:")
    print(agente.politica)

    print("\nEjecutando iteración de política...")
    agente.iteracion_politica(entorno)

    print("\nPolítica óptima:")
    print(agente.politica)

    print("\nValores estimados por estado:")
    for i, v in enumerate(agente.V):
        print(f"Estado {i}: {v:.2f}")
