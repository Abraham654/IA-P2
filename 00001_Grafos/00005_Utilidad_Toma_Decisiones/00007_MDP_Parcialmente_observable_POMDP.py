import numpy as np
from collections import defaultdict

class POMDP:
    def __init__(self, estados, acciones, observaciones, recompensas, transiciones, observaciones_prob, gamma=0.95):
        # Inicialización del modelo POMDP
        self.estados = estados
        self.acciones = acciones
        self.observaciones = observaciones
        self.recompensas = recompensas
        self.transiciones = transiciones
        self.observaciones_prob = observaciones_prob
        self.gamma = gamma
        self.V = defaultdict(float)  # Valores para creencias

    def actualizar_creencia(self, creencia, accion, observacion):
        # Filtro de Bayes: actualiza creencia posterior a acción y observación
        nueva_creencia = defaultdict(float)

        for s_next in self.estados:
            prob = 0
            for s in self.estados:
                prob += self.transiciones.get((s, accion, s_next), 0) * creencia[s]
            prob *= self.observaciones_prob.get((accion, s_next, observacion), 0)
            nueva_creencia[s_next] = prob

        total = sum(nueva_creencia.values())
        if total > 0:
            for s in nueva_creencia:
                nueva_creencia[s] /= total

        return nueva_creencia

    def iteracion_valores(self, epsilon=1e-3, max_iter=1000):
        # Iteración de valores aproximada para POMDP (con α-vectores)
        alpha_vectors = []
        for a in self.acciones:
            alpha = {s: self.recompensas.get((s, a), 0) for s in self.estados}
            alpha_vectors.append((alpha, a))

        for _ in range(max_iter):
            nuevas_alpha = []

            for a in self.acciones:
                alpha = defaultdict(float)

                for o in self.observaciones:
                    mejor_valor = -np.inf
                    mejor_alpha_vec = None

                    for alpha_vec, _ in alpha_vectors:
                        valor = sum(alpha_vec[s] for s in self.estados)
                        if valor > mejor_valor:
                            mejor_valor = valor
                            mejor_alpha_vec = alpha_vec

                    if mejor_alpha_vec:
                        for s in self.estados:
                            alpha[s] += self.gamma * sum(
                                self.transiciones.get((s, a, s_next), 0) *
                                self.observaciones_prob.get((a, s_next, o), 0) *
                                mejor_alpha_vec[s_next]
                                for s_next in self.estados
                            )

                for s in self.estados:
                    alpha[s] += self.recompensas.get((s, a), 0)

                nuevas_alpha.append((alpha, a))

            delta = max(
                abs(alpha[s] - alpha_vectors[i][0][s])
                for i, (alpha, _) in enumerate(nuevas_alpha)
                for s in self.estados
            )

            alpha_vectors = nuevas_alpha
            if delta < epsilon:
                break

        self.alpha_vectors = alpha_vectors

    def elegir_accion(self, creencia):
        # Selecciona acción óptima dado vector de creencia actual
        mejor_valor = -np.inf
        mejor_accion = None

        for alpha_vec, accion in self.alpha_vectors:
            valor = sum(creencia[s] * alpha_vec[s] for s in self.estados)
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_accion = accion

        return mejor_accion


# --- Simulación con robot en un laberinto ---
if __name__ == "__main__":
    estados = ['S1', 'S2', 'S3']
    acciones = ['Izq', 'Der', 'Obs']
    observaciones = ['Nada', 'Pared', 'Meta']

    recompensas = {
        ('S1', 'Izq'): -1, ('S1', 'Der'): -1, ('S1', 'Obs'): -1,
        ('S2', 'Izq'): -1, ('S2', 'Der'): -1, ('S2', 'Obs'): -1,
        ('S3', 'Izq'): -1, ('S3', 'Der'): 10, ('S3', 'Obs'): -1
    }

    transiciones = {
        ('S1', 'Izq', 'S1'): 1.0, ('S1', 'Der', 'S2'): 0.8, ('S1', 'Der', 'S1'): 0.2, ('S1', 'Obs', 'S1'): 1.0,
        ('S2', 'Izq', 'S1'): 0.8, ('S2', 'Izq', 'S2'): 0.2, ('S2', 'Der', 'S3'): 0.8, ('S2', 'Der', 'S2'): 0.2, ('S2', 'Obs', 'S2'): 1.0,
        ('S3', 'Izq', 'S2'): 0.8, ('S3', 'Izq', 'S3'): 0.2, ('S3', 'Der', 'S3'): 1.0, ('S3', 'Obs', 'S3'): 1.0
    }

    observaciones_prob = {
        ('Izq', 'S1', 'Pared'): 0.9, ('Izq', 'S1', 'Nada'): 0.1,
        ('Izq', 'S2', 'Nada'): 0.8, ('Izq', 'S2', 'Pared'): 0.2,
        ('Izq', 'S3', 'Meta'): 0.9, ('Izq', 'S3', 'Nada'): 0.1,
        ('Der', 'S1', 'Pared'): 0.9, ('Der', 'S1', 'Nada'): 0.1,
        ('Der', 'S2', 'Nada'): 0.8, ('Der', 'S2', 'Pared'): 0.2,
        ('Der', 'S3', 'Meta'): 0.9, ('Der', 'S3', 'Nada'): 0.1,
        ('Obs', 'S1', 'Pared'): 0.9, ('Obs', 'S1', 'Nada'): 0.1,
        ('Obs', 'S2', 'Nada'): 0.8, ('Obs', 'S2', 'Pared'): 0.2,
        ('Obs', 'S3', 'Meta'): 0.9, ('Obs', 'S3', 'Nada'): 0.1
    }

    pomdp = POMDP(estados, acciones, observaciones, recompensas, transiciones, observaciones_prob)
    pomdp.iteracion_valores()

    creencia_actual = {'S1': 0.5, 'S2': 0.3, 'S3': 0.2}

    for paso in range(5):
        accion = pomdp.elegir_accion(creencia_actual)
        print(f"Paso {paso+1}: Creencia {creencia_actual} -> Acción: {accion}")
        observacion = np.random.choice(observaciones, p=[0.1, 0.7, 0.2])
        print(f"Observación: {observacion}")
        creencia_actual = pomdp.actualizar_creencia(creencia_actual, accion, observacion)
