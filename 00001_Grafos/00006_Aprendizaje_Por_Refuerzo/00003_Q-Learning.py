import numpy as np
from collections import defaultdict

class QLearning:
    def __init__(self, n_estados, n_acciones, gamma=0.95, alpha=0.1, epsilon=0.1):
        self.Q = np.zeros((n_estados, n_acciones))  # Tabla Q [estados x acciones]
        self.gamma = gamma  # Factor de descuento
        self.alpha = alpha  # Tasa de aprendizaje
        self.epsilon = epsilon  # Exploración
        self.n_acciones = n_acciones

    def seleccionar_accion(self, estado):
        # Regla ε-greedy: explora con probabilidad ε, explota lo aprendido con 1-ε
        if np.random.random() < self.epsilon:
            return np.random.randint(self.n_acciones)
        return np.argmax(self.Q[estado])

    def actualizar(self, estado, accion, recompensa, estado_siguiente):
        # Ecuación de Bellman: actualiza el valor Q con el error TD
        mejor_q_siguiente = np.max(self.Q[estado_siguiente])
        td_error = recompensa + self.gamma * mejor_q_siguiente - self.Q[estado, accion]
        self.Q[estado, accion] += self.alpha * td_error

    def entrenar(self, entorno, n_episodios=1000, max_pasos=100):
        recompensas = []
        for _ in range(n_episodios):
            estado = entorno.reset()
            total = 0
            for _ in range(max_pasos):
                accion = self.seleccionar_accion(estado)
                sig_estado, recompensa, terminado = entorno.step(accion)
                self.actualizar(estado, accion, recompensa, sig_estado)
                estado = sig_estado
                total += recompensa
                if terminado:
                    break
            recompensas.append(total)
            self.epsilon = max(0.01, self.epsilon * 0.995)  # Decae la exploración
        return recompensas

    def obtener_politica(self):
        # Política óptima: acción con mayor Q por estado
        return np.argmax(self.Q, axis=1)

class GrafoEntorno:
    def __init__(self):
        self.n_estados = 5
        self.n_acciones = 5
        self.estado_meta = 4
        self.estado_actual = None
        # Grafo: -1 (sin conexión), 0 o 10 (recompensa por moverse)
        self.grafo = np.array([
            [-1, 0, -1, 0, -1],
            [0, -1, 0, -1, 0],
            [-1, 0, -1, 0, -1],
            [0, -1, 0, -1, 10],
            [-1, 0, -1, 0, -1]
        ])
    
    def reset(self):
        self.estado_actual = 0  # Inicia en nodo 0
        return self.estado_actual

    def step(self, accion):
        # Movimiento inválido: penalización
        if self.grafo[self.estado_actual, accion] == -1:
            return self.estado_actual, -10, False
        recompensa = self.grafo[self.estado_actual, accion]
        self.estado_actual = accion
        terminado = (self.estado_actual == self.estado_meta)
        return self.estado_actual, recompensa, terminado

# Ejecución del entrenamiento
if __name__ == "__main__":
    entorno = GrafoEntorno()
    agente = QLearning(entorno.n_estados, entorno.n_acciones)
    print("Entrenando al agente...")
    recompensas = agente.entrenar(entorno, n_episodios=500)

    print("\nTabla Q aprendida:")
    print(agente.Q)

    print("\nPolítica óptima:")
    politica = agente.obtener_politica()
    for estado, accion in enumerate(politica):
        print(f"Desde nodo {estado} -> Ir a nodo {accion}")

    print("\nRecompensas (últimos 10 episodios):")
    print(recompensas[-10:])
