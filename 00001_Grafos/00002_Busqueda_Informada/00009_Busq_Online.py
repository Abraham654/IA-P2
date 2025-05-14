import heapq # Importa la librería 'heapq'. Aunque está importada, esta implementación específica de LRTA* no la utiliza para una cola de prioridad. Los nodos se seleccionan basándose en la mejor opción local después de actualizar la heurística.
import math # Importa la librería 'math', utilizada aquí para acceder a 'math.inf' (infinito positivo), usado como valor inicial para encontrar el mínimo.

# Define una clase para encapsular la lógica de búsqueda online, incluyendo el aprendizaje de la heurística.
# La búsqueda online implica que el agente explora el entorno paso a paso, aprendiendo a medida que avanza.
class BusquedaOnline:
    # Método constructor de la clase.
    # Recibe el grafo (aunque en un entorno puramente online, esto se "descubriría" a medida que se mueve)
    # y la función heurística inicial (una estimación del costo al objetivo).
    def __init__(self, grafo, heuristica):
        self.grafo = grafo # Almacena el grafo (nodos y costos de aristas).
        self.heuristica = heuristica # Almacena la función heurística inicial h_0(n, objetivo).
        # Diccionario para almacenar los valores de heurística aprendidos (h(n)). Inicialmente vacío, se llenará a medida que se visitan nodos.
        self.H = {} # Heurísticas aprendidas: {nodo: h(nodo)}

    # Implementa el algoritmo Learning Real-Time A* (LRTA*).
    # LRTA* es un algoritmo de búsqueda online que actualiza su estimación heurística
    # h(n) = min_{n' \in successors(n)} (costo(n, n') + h(n')). Se mueve al sucesor con el mínimo costo + h.
    # Recibe: el nodo de inicio y el nodo objetivo.
    def lrta_star(self, inicio, objetivo):
        # Inicializa el nodo actual al nodo de inicio.
        actual = inicio
        # Inicializa la lista del camino tomado por el agente.
        camino = [actual]

        # Bucle principal de LRTA*. Continúa mientras el nodo actual no sea el objetivo.
        # El agente se mueve paso a paso hasta alcanzar la meta.
        while actual != objetivo:
            # Si la heurística para el nodo actual no ha sido aprendida aún (no está en el diccionario H).
            if actual not in self.H:
                # Inicializa la heurística aprendida para este nodo con el valor de la heurística inicial (base).
                self.H[actual] = self.heuristica(actual, objetivo)

            # Inicializa variables para encontrar el mejor movimiento desde el nodo actual.
            # mejor_valor almacenará el mínimo valor de (costo_arista + h_aprendida_del_vecino).
            mejor_valor = math.inf # Inicializa con infinito para asegurar que el primer valor sea menor.
            # mejor_vecino almacenará el nodo sucesor que tiene el mejor valor.
            mejor_vecino = None

            # Explora los vecinos del nodo actual. En un agente online, esta información (vecinos y costos)
            # se obtiene del entorno al estar en el nodo 'actual'.
            # Itera sobre los pares (vecino, costo_arista) para todas las salidas del nodo 'actual'.
            for vecino, costo in self.grafo[actual].items():
                # Obtiene la heurística aprendida para el vecino. Si no está en H, usa la heurística inicial (base).
                # self.H.get(vecino, ...) es una forma segura de acceder a un diccionario con un valor por defecto.
                h_vecino = self.H.get(vecino, self.heuristica(vecino, objetivo))
                # Calcula el valor de ir a este vecino: costo de la arista + heurística aprendida del vecino.
                valor = costo + h_vecino

                # Si este valor es menor que el mejor valor encontrado hasta ahora entre los vecinos.
                if valor < mejor_valor:
                    # Actualiza el mejor valor encontrado.
                    mejor_valor = valor
                    # Actualiza el mejor vecino (el sucesor al que el agente elegirá moverse).
                    mejor_vecino = vecino

            # --- Paso de Aprendizaje Clave de LRTA* ---
            # Actualiza la heurística aprendida para el nodo actual.
            # La nueva heurística aprendida h(actual) es el mínimo valor encontrado entre sus sucesores
            # (costo al sucesor + h_aprendida del sucesor).
            # Esto garantiza que h(n) nunca sobreestime el costo real + h*(n'), donde h* es la heurística óptima.
            self.H[actual] = mejor_valor # Actualiza h(n) usando min_{n'} (costo(n, n') + h(n'))

            # El agente se mueve al mejor vecino encontrado.
            actual = mejor_vecino
            # Añade el nuevo nodo actual al camino recorrido.
            camino.append(actual)

        # Una vez que el bucle termina (cuando actual == objetivo), significa que el agente ha llegado a la meta.
        # Retorna el camino que el agente tomó.
        return camino

# Este bloque de código solo se ejecuta cuando el script se corre directamente.
# Contiene un ejemplo de cómo usar la clase BusquedaOnline y el algoritmo LRTA*.
if __name__ == "__main__":
    # Define un grafo de ejemplo. Los nodos son cadenas.
    # El grafo es un diccionario donde las claves son nodos y los valores son diccionarios
    # de vecinos con los costos de las aristas. Los costos son todos 1 en este ejemplo simple.
    grafo = {
        'A': {'B': 1, 'D': 1}, # Desde A, puedes ir a B o D con costo 1.
        'B': {'A': 1, 'C': 1, 'E': 1},
        'C': {'B': 1, 'F': 1},
        'D': {'A': 1, 'E': 1},
        'E': {'B': 1, 'D': 1, 'F': 1, 'G': 1},
        'F': {'C': 1, 'E': 1, 'H': 1},
        'G': {'E': 1, 'H': 1},
        'H': {'F': 1, 'G': 1}
    }

    # Define una función heurística base de ejemplo: la Distancia de Manhattan.
    # Esta heurística requiere conocer las coordenadas de los nodos.
    # Recibe el nodo actual y el nodo objetivo.
    def h(nodo, objetivo):
        # Diccionario que mapea cada nombre de nodo a sus coordenadas (x, y).
        coords = {
            'A': (0,0), 'B': (1,0), 'C': (2,0),
            'D': (0,1), 'E': (1,1), 'F': (2,1),
            'G': (1,2), 'H': (2,2)
        }
        # Desempaqueta las coordenadas del nodo actual.
        x1, y1 = coords[nodo]
        # Desempaqueta las coordenadas del nodo objetivo.
        x2, y2 = coords[objetivo]
        # Calcula la distancia de Manhattan (|x1-x2| + |y1-y2|) y la retorna.
        return abs(x1 - x2) + abs(y1 - y2)

    # Crea una instancia de la clase BusquedaOnline, pasando el grafo y la función heurística base.
    buscador = BusquedaOnline(grafo, h)

    # Llama al método lrta_star para encontrar un camino desde 'A' hasta 'H'.
    # La búsqueda se realiza de forma online y la heurística se actualiza durante el recorrido.
    camino = buscador.lrta_star('A', 'H')

    # Imprime el camino que el agente tomó para llegar al objetivo.
    print("Camino encontrado:", camino)
    # Imprime el diccionario H que contiene los valores de heurística aprendidos para los nodos visitados durante la búsqueda.
    print("Heurística aprendida:", buscador.H)