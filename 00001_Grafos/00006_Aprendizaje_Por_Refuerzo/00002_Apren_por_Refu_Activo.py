import numpy as np
from collections import defaultdict

class QLearning:
    def __init__(self, estados, acciones, gamma=0.95, alpha=0.1, epsilon=0.1):
        # Inicialización de parámetros y tabla Q
        self.estados = estados
        self.acciones = acciones
        self.gamma = gamma      # Factor de descuento
        self.alpha = alpha      # Tasa de aprendizaje
        self.epsilon = epsilon  # Probabilidad de exploración
        self.Q = defaultdict(lambda: np.zeros(len(acciones)))  # Tabla Q vacía
        self.accion_index = {a: i for i, a in enumerate(acciones)}  # Índices de acciones

    def seleccionar_accion(self, estado):
        # Estrategia ε-greedy: explora o elige mejor acción
        if np.random.random() < self.epsilon:
            return np.random.choice(self.acciones)
        return self.acciones[np.argmax(self.Q[estado])]

    def actualizar_q(self, estado, accion, recompensa, estado_siguiente, done):
        # Actualización Q con la ecuación de Bellman
        q_actual = self.Q[estado][self.accion_index[accion]]
        max_q_siguiente = np.max(self.Q[estado_siguiente]) if not done else 0
        self.Q[estado][self.accion_index[accion]] = q_actual + self.alpha * (
            recompensa + self.gamma * max_q_siguiente - q_actual
        )

    def entrenar(self, entorno, n_episodios=1000, max_pasos=100):
        # Entrena al agente en el entorno por varios episodios
        recompensas_episodios = []

        for _ in range(n_episodios):
            estado = entorno.reset()
            recompensa_total = 0
            done = False
            paso = 0

            while not done and paso < max_pasos:
                accion = self.seleccionar_accion(estado)
                estado_sig, recompensa, done, _ = entorno.step(accion)
                self.actualizar_q(estado, accion, recompensa, estado_sig, done)
                estado = estado_sig
                recompensa_total += recompensa
                paso += 1

            recompensas_episodios.append(recompensa_total)
            self.epsilon = max(0.01, self.epsilon * 0.995)  # Decaimiento de epsilon

        return recompensas_episodios

    def obtener_politica(self):
        # Deriva política óptima desde tabla Q
        return {s: self.acciones[np.argmax(self.Q[s])] for s in self.estados}

class GridWorld:
    def __init__(self):
        # Mundo 4x4 con meta y obstáculo
        self.estados = [(i, j) for i in range(4) for j in range(4)]
        self.acciones = ['Arriba', 'Abajo', 'Izquierda', 'Derecha']
        self.meta = (3, 3)
        self.obstaculo = (1, 1)
        self.estado_actual = None

    def reset(self):
        # Reinicia al estado inicial
        self.estado_actual = (0, 0)
        return self.estado_actual

    def step(self, accion):
        # Ejecuta la acción, devuelve nuevo estado y recompensa
        i, j = self.estado_actual

        if accion == 'Arriba':    i = max(i - 1, 0)
        elif accion == 'Abajo':   i = min(i + 1, 3)
        elif accion == 'Izquierda': j = max(j - 1, 0)
        elif accion == 'Derecha':  j = min(j + 1, 3)

        self.estado_actual = (i, j)

        if self.estado_actual == self.meta:
            return self.estado_actual, 10, True, {}
        elif self.estado_actual == self.obstaculo:
            return self.estado_actual, -10, True, {}
        return self.estado_actual, -1, False, {}

# Ejecución principal
if __name__ == "__main__":
    entorno = GridWorld()
    agente = QLearning(entorno.estados, entorno.acciones)

    print("Entrenando al agente...")
    recompensas = agente.entrenar(entorno, n_episodios=1000)

    print("\nPolítica aprendida:")
    politica = agente.obtener_politica()
    for estado in sorted(politica):
        print(f"Estado {estado}: {politica[estado]}")

    print("\nRecompensas (últimos 10 episodios):")
    print(recompensas[-10:])
