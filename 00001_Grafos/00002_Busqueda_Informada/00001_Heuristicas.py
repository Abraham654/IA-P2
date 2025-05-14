# Importa la librería 'heapq'. Esta librería implementa el algoritmo heap, que es
# una estructura de datos de árbol binario utilizada para implementar colas de prioridad eficientes.
# En una cola de prioridad (min-heap), el elemento más pequeño (en este caso, la tupla con el menor primer valor)
# siempre está en la raíz y se puede extraer rápidamente. Esto es fundamental para A* para siempre expandir
# el nodo con el menor f_score.
import heapq  # Cola de prioridad (min-heap)

# Define la función principal para la búsqueda A* (A-estrella).
# Este algoritmo busca el camino de menor costo desde un inicio a un objetivo en un grafo ponderado,
# utilizando una función heurística para guiar la búsqueda.
# Recibe cuatro argumentos:
# - grafo: Un diccionario que representa el grafo. Las claves son los nodos. Los valores son otros diccionarios
#          donde las claves son los nodos vecinos y los valores son los costos (pesos) de la arista hacia ese vecino.
# - inicio: El nodo desde el cual comenzar la búsqueda.
# - objetivo: El nodo que se desea encontrar.
# - heuristica: Una función que estima el costo desde un nodo dado hasta el nodo objetivo.
#               Debe ser una heurística admisible (nunca sobreestima el costo real) para garantizar la optimalidad del camino encontrado.
def busqueda_a_estrella(grafo, inicio, objetivo, heuristica):
    # Inicializa la 'frontera' de exploración como una lista que actuará como una cola de prioridad (min-heap).
    # Los elementos en la frontera son tuplas (f_score, nodo), donde f_score = g_score + h_score.
    frontera = []  # Cola de prioridad: (f_score, nodo)

    # Añade el nodo de inicio a la cola de prioridad. El f_score inicial es el valor de la heurística
    # desde el inicio hasta el objetivo, ya que el costo real desde el inicio a sí mismo (g_score) es 0.
    # heapq.heappush(heap, item) inserta un item en el heap (la lista 'frontera').
    heapq.heappush(frontera, (heuristica(inicio, objetivo), inicio))

    # Inicializa un diccionario para almacenar el costo real conocido para llegar a cada nodo desde el inicio (g_score).
    # El costo para llegar al nodo de inicio desde el inicio es 0.
    g_scores = {inicio: 0}  # Costo real desde el inicio

    # Inicializa un diccionario para almacenar el nodo predecesor (padre) de cada nodo en el camino más corto encontrado hasta ahora.
    # Esto se utiliza para reconstruir el camino una vez que se alcanza el objetivo.
    # El nodo de inicio no tiene padre en el contexto de la búsqueda.
    padres = {inicio: None}  # Registro de padres para reconstruir camino

    # Inicia el bucle principal del algoritmo A*. Continúa mientras la frontera (cola de prioridad) no esté vacía.
    while frontera:
        # Extrae el nodo con el menor f_score de la cola de prioridad.
        # heapq.heappop(heap) extrae y devuelve el elemento más pequeño del heap (la tupla con el menor f_score).
        # Desempaquetamos la tupla, guardando el f_score en '_' (indicando que no lo usaremos directamente después) y el nodo en 'actual'.
        _, actual = heapq.heappop(frontera)  # Nodo con menor f_score

        # Comprueba si el nodo actual extraído es el objetivo.
        if actual == objetivo:
            # Si es el objetivo, hemos encontrado el camino de menor costo (debido a las propiedades de A* con heurística admisible).
            # Inicializa una lista vacía para construir el camino.
            camino = []
            # Retrocede desde el nodo objetivo hasta el inicio usando el diccionario 'padres'.
            while actual is not None:
                # Añade el nodo actual a la lista del camino (temporalmente estará en orden inverso).
                camino.append(actual)
                # Se mueve al nodo padre de este nodo.
                actual = padres[actual]
            # Invierte la lista del camino para que vaya desde el inicio hasta el objetivo.
            # Retorna la lista del camino invertido y el costo total para llegar al objetivo, que es el g_score del nodo objetivo.
            # Nota: camino[0] será el objetivo después de la inversión, por eso se usa g_scores[camino[0]] o g_scores[objetivo].
            return camino[::-1], g_scores[camino[0]]  # Camino y costo total

        # Explora los vecinos del nodo actual.
        # Itera sobre los pares (vecino, costo_de_arista) en el diccionario de vecinos del nodo 'actual' en el 'grafo'.
        for vecino, costo in grafo[actual].items():
            # Calcula el costo tentativo para llegar al vecino a través del nodo 'actual'.
            # Es el g_score del nodo actual más el costo de la arista para llegar al vecino.
            g_tentativo = g_scores[actual] + costo

            # Condición clave de A* (y Dijkstra): Comprueba si este camino al vecino es el mejor encontrado hasta ahora.
            # Esto ocurre si el vecino no ha sido visitado antes (no tiene g_score) O si el costo tentativo por este camino
            # es menor que el g_score previamente registrado para el vecino.
            if vecino not in g_scores or g_tentativo < g_scores[vecino]:
                # Si este camino es mejor:
                # Establece el nodo actual como el padre del vecino en el camino óptimo encontrado hasta ahora.
                padres[vecino] = actual
                # Actualiza el g_score del vecino con el costo real más bajo encontrado hasta ahora.
                g_scores[vecino] = g_tentativo
                # Calcula el f_score para el vecino: g_score actualizado + el valor de la heurística desde el vecino al objetivo.
                f_score = g_tentativo + heuristica(vecino, objetivo)
                # Añade el vecino a la cola de prioridad con su f_score. La cola lo ordenará automáticamente.
                # Esto asegura que siempre expandamos el nodo con el menor costo estimado total.
                heapq.heappush(frontera, (f_score, vecino))

    # Si el bucle 'while frontera:' termina y no se encontró el objetivo (la frontera se vació),
    # significa que el objetivo no es alcanzable desde el nodo de inicio.
    # Retorna None para el camino y None para el costo.
    return None, None  # No se encontró camino

# Define una función de heurística de ejemplo: la Distancia de Manhattan.
# Esta heurística es comúnmente usada en cuadrículas (grids) y es admisible si el movimiento solo es ortogonal (horizontal/vertical).
# Recibe dos nodos, se espera que sean tuplas (x, y).
def heuristica_manhattan(nodo, objetivo):
    # Desempaqueta las coordenadas (x, y) del nodo actual.
    x1, y1 = nodo
    # Desempaqueta las coordenadas (x, y) del nodo objetivo.
    x2, y2 = objetivo
    # Calcula y retorna la distancia de Manhattan: |x1 - x2| + |y1 - y2|.
    return abs(x1 - x2) + abs(y1 - y2)

# Este bloque de código solo se ejecuta cuando el script se corre directamente.
# Contiene un ejemplo de cómo usar la función de búsqueda A* con un grafo y la heurística de Manhattan.
if __name__ == "__main__":
    # Define el grafo de ejemplo. Los nodos son tuplas (x, y).
    # El grafo es un diccionario donde las claves son nodos y los valores son diccionarios de vecinos con sus costos.
    grafo = {
        (0, 0): {(0, 1): 1, (1, 0): 1}, # Desde (0,0) puedes ir a (0,1) con costo 1 o a (1,0) con costo 1.
        (0, 1): {(0, 0): 1, (0, 2): 1, (1, 1): 1.5}, # Desde (0,1) puedes ir a (0,0) con costo 1, etc.
        (0, 2): {(0, 1): 1, (1, 2): 1},
        (1, 0): {(0, 0): 1, (1, 1): 1, (2, 0): 1},
        (1, 1): {(0, 1): 1.5, (1, 0): 1, (1, 2): 1, (2, 1): 1},
        (1, 2): {(0, 2): 1, (1, 1): 1, (2, 2): 1},
        (2, 0): {(1, 0): 1, (2, 1): 1},
        (2, 1): {(1, 1): 1, (2, 0): 1, (2, 2): 1},
        (2, 2): {(1, 2): 1, (2, 1): 1}
    }

    # Define el nodo de inicio y el nodo objetivo para la búsqueda.
    inicio, objetivo = (0, 0), (2, 2)

    # Llama a la función de búsqueda A* con el grafo, inicio, objetivo y la función de heurística de Manhattan.
    # El resultado es una tupla (camino, costo), que se desempaqueta en las variables correspondientes.
    camino, costo = busqueda_a_estrella(grafo, inicio, objetivo, heuristica_manhattan)

    # Imprime el camino encontrado.
    print("Camino encontrado:", camino)
    # Imprime el costo total del camino encontrado.
    print("Costo total:", costo)
