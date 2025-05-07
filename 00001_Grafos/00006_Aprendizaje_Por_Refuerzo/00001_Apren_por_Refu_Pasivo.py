import numpy as np
import random
from collections import defaultdict

class RefuerzoPasivo:
    def __init__(self, estados, acciones, transiciones, recompensas, politica, gamma=0.9):
        # Inicializa atributos principales: lista de estados, acciones posibles, transiciones, recompensas, política a evaluar y gamma
        self.estados = list(estados)
        self.acciones = acciones
        self.transiciones = transiciones
        self.recompensas = recompensas
        self.politica = politica
        self.gamma = gamma
        self.V = {s: 0 for s in self.estados}  # Valor estimado de cada estado
        self.contador_visitas = defaultdict(int)

    def evaluacion_diferencia_temporal(self, alpha=0.1, n_episodios=1000):
        # Evalúa valores usando diferencia temporal (TD)
        for _ in range(n_episodios):
            estado = random.choice(self.estados)  # Selección aleatoria de estado inicial

            while True:
                accion = self.politica.get(estado)
                if accion is None:  # Fin del episodio si no hay acción
                    break

                # Obtener próximos estados posibles desde la transición actual
                proximos = [(s_next, p) for (s_act, a, s_next), p in self.transiciones.items()
                            if s_act == estado and a == accion]

                if not proximos:
                    break

                estados_next, probs = zip(*proximos)
                estado_next = random.choices(estados_next, weights=probs, k=1)[0]
                recompensa = self.recompensas.get((estado, accion, estado_next), 0)

                # Actualización TD del valor del estado actual
                self.V[estado] += alpha * (recompensa + self.gamma * self.V[estado_next] - self.V[estado])
                estado = estado_next

    def evaluacion_monte_carlo(self, n_episodios=1000):
        # Evalúa valores usando el método Monte Carlo (retornos promedio)
        returns = {s: [] for s in self.estados}

        for _ in range(n_episodios):
            episodio = []
            estado = random.choice(self.estados)

            while True:
                accion = self.politica.get(estado)
                if accion is None:
                    break

                proximos = [(s_next, p) for (s_act, a, s_next), p in self.transiciones.items()
                            if s_act == estado and a == accion]

                if not proximos:
                    break

                estados_next, probs = zip(*proximos)
                estado_next = random.choices(estados_next, weights=probs, k=1)[0]
                recompensa = self.recompensas.get((estado, accion, estado_next), 0)

                episodio.append((estado, accion, recompensa))
                estado = estado_next

            # Calcular retornos para el episodio
            G = 0
            visitados = set()
            for t in reversed(range(len(episodio))):
                estado_ep, _, recompensa = episodio[t]
                G = self.gamma * G + recompensa
                if estado_ep not in visitados:
                    visitados.add(estado_ep)
                    returns[estado_ep].append(G)
                    self.V[estado_ep] = np.mean(returns[estado_ep])

    def mostrar_valores(self):
        # Imprime los valores estimados para cada estado
        print("Valores estimados:")
        for estado in sorted(self.V.keys()):
            print(f"Estado {estado}: {self.V[estado]:.2f}")

# Ejemplo: Mundo 3x3 con política fija
if __name__ == "__main__":
    estados = [(0,0), (0,1), (0,2), 
               (1,0), (1,1), (1,2),
               (2,0), (2,1), (2,2)]

    acciones = ['Arriba', 'Abajo', 'Izquierda', 'Derecha']

    politica = {s: 'Derecha' for s in estados}
    politica[(2,2)] = None  # Estado terminal

    transiciones = {}
    for (i, j) in estados:
        if (i, j) == (2, 2):
            continue
        for accion in acciones:
            if accion == 'Arriba':
                next_i, next_j = max(i-1, 0), j
            elif accion == 'Abajo':
                next_i, next_j = min(i+1, 2), j
            elif accion == 'Izquierda':
                next_i, next_j = i, max(j-1, 0)
            elif accion == 'Derecha':
                next_i, next_j = i, min(j+1, 2)
            transiciones[((i, j), accion, (next_i, next_j))] = 1.0  # Transición determinista

    recompensas = {
        ((1,2), 'Derecha', (2,2)): 10,
        ((2,1), 'Abajo', (2,2)): -10
    }

    print("Evaluación con Diferencia Temporal:")
    rp = RefuerzoPasivo(estados, acciones, transiciones, recompensas, politica)
    rp.evaluacion_diferencia_temporal(n_episodios=1000)
    rp.mostrar_valores()

    print("\nEvaluación con Monte Carlo:")
    rp = RefuerzoPasivo(estados, acciones, transiciones, recompensas, politica)
    rp.evaluacion_monte_carlo(n_episodios=1000)
    rp.mostrar_valores()
