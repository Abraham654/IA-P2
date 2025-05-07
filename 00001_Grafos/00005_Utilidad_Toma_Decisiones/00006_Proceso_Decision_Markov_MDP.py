import numpy as np

class MDP:
    def __init__(self, estados, acciones, recompensas, transiciones, gamma=0.9, epsilon=1e-6):
        # Inicializa parámetros del MDP
        self.estados = estados
        self.acciones = acciones
        self.recompensas = recompensas
        self.transiciones = transiciones
        self.gamma = gamma  # factor de descuento
        self.epsilon = epsilon  # tolerancia de convergencia
        self.V = {s: 0 for s in estados}  # función de valor
        self.politica = {s: None for s in estados}  # política óptima

    def calcular_recompensa_esperada(self, estado, accion):
        # Suma de recompensas ponderadas por su probabilidad
        return sum(
            prob * self.recompensas.get((estado, accion, s_next), 0)
            for (s, a, s_next), prob in self.transiciones.items()
            if s == estado and a == accion
        )

    def iteracion_valores(self):
        # Iteración de valores para hallar política óptima
        while True:
            delta = 0
            V_nuevo = self.V.copy()

            for estado in self.estados:
                if estado not in self.acciones:
                    continue  # omite estados terminales

                valores_acciones = []
                for accion in self.acciones[estado]:
                    recompensa = self.calcular_recompensa_esperada(estado, accion)
                    valor = recompensa + self.gamma * sum(
                        prob * self.V[s_next]
                        for (s, a, s_next), prob in self.transiciones.items()
                        if s == estado and a == accion
                    )
                    valores_acciones.append(valor)

                if valores_acciones:
                    V_nuevo[estado] = max(valores_acciones)
                    self.politica[estado] = self.acciones[estado][np.argmax(valores_acciones)]

                delta = max(delta, abs(V_nuevo[estado] - self.V[estado]))

            self.V = V_nuevo
            if delta < self.epsilon:
                break

    def mostrar_solucion(self):
        # Muestra la política y los valores de estado
        print("Política óptima:")
        for estado in sorted(self.estados):
            print(f"  Estado {estado}: {self.politica[estado]}")

        print("\nValores de los estados:")
        for estado in sorted(self.estados):
            print(f"  Estado {estado}: {self.V[estado]:.2f}")

# ---------------------- DEFINICIÓN DEL PROBLEMA ----------------------

if __name__ == "__main__":
    estados = [(0,0), (0,1), (0,2), (1,0), (1,2), (2,0), (2,1), (2,2)]

    acciones = {
        (0,0): ['Derecha', 'Abajo'],
        (0,1): ['Izquierda', 'Derecha'],
        (0,2): ['Izquierda', 'Abajo'],
        (1,0): ['Arriba', 'Derecha', 'Abajo'],
        (1,2): ['Arriba', 'Izquierda', 'Abajo'],
        (2,0): ['Arriba', 'Derecha'],
        (2,1): ['Izquierda', 'Derecha'],
        (2,2): ['Izquierda', 'Arriba']  # terminal
    }

    recompensas = {
        **{((2,2), a, (2,2)): 1 for a in acciones[(2,2)]},
        ((1,2), 'Abajo', (2,2)): 1,
        ((0,2), 'Abajo', (1,2)): 0,
        ((1,0), 'Derecha', (1,2)): 0,
        ((2,1), 'Derecha', (2,2)): 0,
        ((2,0), 'Derecha', (2,1)): 0,
        ((0,1), 'Derecha', (0,2)): 0,
        ((0,0), 'Derecha', (0,1)): 0,
        ((0,0), 'Abajo', (1,0)): 0,
        ((1,0), 'Abajo', (2,0)): 0,
        ((1,2), 'Izquierda', (1,0)): 0,
        ((0,1), 'Izquierda', (0,0)): 0,
        ((2,1), 'Izquierda', (2,0)): 0,
        ((0,2), 'Izquierda', (0,1)): 0,
        ((1,0), 'Arriba', (0,0)): 0,
        ((1,2), 'Arriba', (0,2)): 0,
        ((2,0), 'Arriba', (1,0)): 0,
        ((2,2), 'Arriba', (1,2)): 0,
        ((2,2), 'Izquierda', (2,1)): 0
    }

    transiciones = {
        **{((2,2), a, (2,2)): 1 for a in acciones[(2,2)]},
        ((0,0), 'Derecha', (0,1)): 1,
        ((0,0), 'Abajo', (1,0)): 1,
        ((0,1), 'Derecha', (0,2)): 1,
        ((0,1), 'Izquierda', (0,0)): 1,
        ((0,2), 'Izquierda', (0,1)): 1,
        ((0,2), 'Abajo', (1,2)): 1,
        ((1,0), 'Derecha', (1,2)): 1,
        ((1,0), 'Arriba', (0,0)): 1,
        ((1,0), 'Abajo', (2,0)): 1,
        ((1,2), 'Izquierda', (1,0)): 1,
        ((1,2), 'Arriba', (0,2)): 1,
        ((1,2), 'Abajo', (2,2)): 1,
        ((2,0), 'Arriba', (1,0)): 1,
        ((2,0), 'Derecha', (2,1)): 1,
        ((2,1), 'Izquierda', (2,0)): 1,
        ((2,1), 'Derecha', (2,2)): 1,
        ((2,2), 'Izquierda', (2,1)): 1,
        ((2,2), 'Arriba', (1,2)): 1
    }

    laberinto_mdp = MDP(estados, acciones, recompensas, transiciones)
    laberinto_mdp.iteracion_valores()
    laberinto_mdp.mostrar_solucion()
