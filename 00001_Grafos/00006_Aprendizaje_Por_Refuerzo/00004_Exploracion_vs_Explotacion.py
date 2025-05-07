import numpy as np
import matplotlib.pyplot as plt

np.seterr(divide='ignore')  # Evita warnings por log(0)

class AgenteRL:
    def __init__(self, n_estados, n_acciones):
        self.Q = np.zeros((n_estados, n_acciones))
        self.conteo_visitas = np.zeros((n_estados, n_acciones))
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.c = 1.4

    def estrategia_epsilon_greedy(self, estado):
        if np.random.rand() < self.epsilon:
            return np.random.randint(self.Q.shape[1])
        return np.argmax(self.Q[estado])

    def estrategia_ucb(self, estado):
        total_visitas = np.sum(self.conteo_visitas[estado]) + 1  # evita log(0)
        ucb_values = [
            self.Q[estado, a] + self.c * np.sqrt(np.log(total_visitas) / (1 + self.conteo_visitas[estado, a]))
            for a in range(self.Q.shape[1])
        ]
        return np.argmax(ucb_values)

    def estrategia_softmax(self, estado, temperatura=1.0):
        q_vals = self.Q[estado]
        exp_q = np.exp(q_vals / temperatura)
        probas = exp_q / np.sum(exp_q)
        return np.random.choice(len(q_vals), p=probas)

    def actualizar_q(self, estado, accion, recompensa, estado_siguiente, alpha=0.1, gamma=0.9):
        mejor_q = np.max(self.Q[estado_siguiente])
        self.Q[estado, accion] += alpha * (recompensa + gamma * mejor_q - self.Q[estado, accion])
        self.conteo_visitas[estado, accion] += 1
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

class EntornoGrafo:
    def __init__(self):
        self.n_estados = 6
        self.n_acciones = 6
        self.estado_meta = 5
        self.grafo = np.array([
            [-1,  2, -1, -1, -1, -1],
            [ 2, -1,  3, -1, -1, -1],
            [-1,  3, -1,  4, -1, -1],
            [-1, -1,  4, -1,  5, -1],
            [-1, -1, -1,  5, -1, 10],
            [-1, -1, -1, -1, 10, -1],
        ])
        self.reset()

    def reset(self):
        self.estado_actual = 0
        return self.estado_actual

    def step(self, accion):
        if self.grafo[self.estado_actual, accion] == -1:
            return self.estado_actual, -2, False
        recompensa = self.grafo[self.estado_actual, accion]
        self.estado_actual = accion
        done = self.estado_actual == self.estado_meta
        return self.estado_actual, recompensa, done

def comparar_estrategias():
    entorno = EntornoGrafo()
    estrategias = {
        "ε-Greedy": AgenteRL(entorno.n_estados, entorno.n_acciones),
        "UCB": AgenteRL(entorno.n_estados, entorno.n_acciones),
        "Softmax": AgenteRL(entorno.n_estados, entorno.n_acciones),
    }
    resultados = {nombre: [] for nombre in estrategias}
    max_pasos = 50  # evita bucles infinitos

    for nombre, agente in estrategias.items():
        for episodio in range(200):  # puedes subir a 300 si quieres
            estado = entorno.reset()
            recompensa_total = 0
            for _ in range(max_pasos):
                if nombre == "ε-Greedy":
                    accion = agente.estrategia_epsilon_greedy(estado)
                elif nombre == "UCB":
                    accion = agente.estrategia_ucb(estado)
                else:
                    accion = agente.estrategia_softmax(estado, temperatura=1.0)

                estado_siguiente, recompensa, done = entorno.step(accion)
                agente.actualizar_q(estado, accion, recompensa, estado_siguiente)
                estado = estado_siguiente
                recompensa_total += recompensa
                if done:
                    break
            resultados[nombre].append(recompensa_total)

    plt.figure(figsize=(10, 5))
    for nombre, recompensas in resultados.items():
        plt.plot(recompensas, label=nombre)
    plt.xlabel("Episodios")
    plt.ylabel("Recompensa Acumulada")
    plt.title("Comparación de Estrategias de Exploración")
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    comparar_estrategias()
