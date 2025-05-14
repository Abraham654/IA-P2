# Importa la librería 'heapq'. Esta librería es fundamental para implementar colas de prioridad eficientes.
# La Búsqueda Voraz utiliza una cola de prioridad para siempre expandir el nodo que parece "más cercano" al objetivo
# según la función heurística.
import heapq  # Cola de prioridad (para elegir el nodo con menor heurística)

# Define la función que implementa el algoritmo de Búsqueda Voraz (Greedy Best-First Search).
# Este algoritmo es una forma de búsqueda informada que utiliza una heurística para guiar la exploración,
# expandiendo siempre el nodo en la frontera que tiene el menor valor heurístico (h(n)).
# Recibe cuatro argumentos:
# - grafo: Un diccionario que representa el grafo.
# - inicio: El nodo desde el cual comenzar la búsqueda.
# - objetivo: El nodo que se desea encontrar.
# - heuristica: Una función que toma dos nodos (el nodo actual y el nodo objetivo) y retorna una estimación
#               del costo o distancia desde el nodo actual hasta el objetivo (el valor heurístico h(n)).
def busqueda_voraz(grafo, inicio, objetivo, heuristica):
    # Inicializa la 'frontera' de exploración como una lista que actuará como una cola de prioridad (min-heap).
    # Los elementos en la frontera son tuplas (valor_de_prioridad, nodo). En Búsqueda Voraz, la prioridad es solo el valor heurístico.
    frontera = []  # Cola: (h(n), nodo)

    # Añade el nodo de inicio a la cola de prioridad. La prioridad es la heurística desde el inicio hasta el objetivo.
    # heapq.heappush(heap, item) inserta un item (la tupla) en el heap (la lista 'frontera').
    heapq.heappush(frontera, (heuristica(inicio, objetivo), inicio))

    # Inicializa un diccionario para almacenar el nodo predecesor (padre) de cada nodo en el camino encontrado hasta ahora.
    # Esto se utiliza para reconstruir el camino una vez que se alcanza el objetivo.
    # El nodo de inicio no tiene padre en el contexto de la búsqueda.
    padres = {inicio: None}  # Para reconstruir camino

    # Inicializa un conjunto para mantener un registro de los nodos que ya han sido extraídos de la frontera
    # (es decir, que han sido expandidos). Esto evita reprocesar el mismo nodo varias veces si se llega a él por distintos caminos.
    visitados = set()  # Para evitar reprocesar nodos

    # Inicia el bucle principal del algoritmo. Continúa mientras la frontera (cola de prioridad) no esté vacía.
    while frontera:
        # Extrae el nodo de la frontera que tiene la menor prioridad (el menor valor heurístico).
        # heapq.heappop(heap) extrae y devuelve el elemento más pequeño del heap (la tupla con el menor primer elemento).
        # Desempaquetamos la tupla, guardando el valor de prioridad (h_score) en '_' (lo descartamos) y el nodo en 'actual'.
        _, actual = heapq.heappop(frontera)  # Saca el nodo más prometedor (menor h)

        # Comprueba si el nodo actual extraído es el objetivo.
        if actual == objetivo:
            # Si es el objetivo, hemos encontrado un camino.
            # Nota: En Búsqueda Voraz, este camino no está garantizado que sea el más corto o el de menor costo.
            # Inicializa una lista vacía para construir el camino.
            camino = []
            # Retrocede desde el nodo objetivo hasta el inicio usando el diccionario 'padres'.
            while actual: # El bucle continúa mientras 'actual' no sea None (hasta llegar al nodo inicial).
                # Añade el nodo actual a la lista (temporalmente en orden inverso).
                camino.append(actual)
                # Se mueve al nodo padre de este nodo.
                actual = padres[actual]
            # Invierte la lista del camino para que vaya desde el inicio hasta el objetivo.
            return camino[::-1]  # De inicio a objetivo

        # Comprueba si el nodo actual ya ha sido visitado (expandido previamente).
        if actual in visitados:
            # Si ya fue visitado, salta al principio del bucle para procesar el siguiente nodo de la frontera.
            # Esto asegura que no expandamos un nodo más de una vez.
            continue  # Saltar si ya fue expandido

        # Si el nodo actual no ha sido visitado, lo marca como visitado.
        visitados.add(actual)

        # Explora los vecinos del nodo actual.
        for vecino in grafo[actual]:
            # Comprueba si el vecino no ha sido visitado Y si no tiene un padre asignado aún.
            # La segunda parte (`vecino not in padres`) es una forma de verificar si este vecino ya fue
            # encontrado y puesto en la frontera previamente a través de otro camino. Si ya tiene padre,
            # significa que ya está en la frontera o ya fue expandido, y no lo reprocesamos desde 'actual'.
            if vecino not in visitados and vecino not in padres:
                 # Si el vecino es un nodo nuevo (o no procesado aún en esta búsqueda):
                # Establece el nodo actual como el padre del vecino en el camino.
                padres[vecino] = actual
                # Calcula el valor heurístico para el vecino (estimación del costo al objetivo desde el vecino).
                # Añade el vecino a la cola de prioridad, con su valor heurístico como prioridad.
                # Esto lo pone en el lugar correcto en el heap según su distancia estimada al objetivo.
                heapq.heappush(frontera, (heuristica(vecino, objetivo), vecino))

    # Si el bucle 'while frontera:' termina (la frontera se vació) y no se encontró el objetivo,
    # significa que el objetivo no es alcanzable desde el nodo de inicio.
    return None  # No se encontró camino

# Define una función de heurística de ejemplo: la Distancia Euclidiana.
# Esta heurística calcula la distancia en línea recta entre dos puntos en un espacio Euclidiano.
# Es admisible si el movimiento es posible en cualquier dirección.
# Recibe dos nodos, se espera que representen puntos con coordenadas (x, y).
def heuristica_euclidiana(nodo, objetivo):
    # Desempaqueta las coordenadas (x, y) del primer nodo.
    x1, y1 = nodo
    # Desempaqueta las coordenadas (x, y) del segundo nodo (el objetivo).
    x2, y2 = objetivo
    # Calcula la distancia Euclidiana usando el teorema de Pitágoras: sqrt((x1-x2)^2 + (y1-y2)^2).
    # Se eleva a la potencia 0.5 para obtener la raíz cuadrada.
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

# Este bloque de código solo se ejecuta cuando el script se corre directamente.
# Contiene un ejemplo de cómo usar la función de búsqueda voraz con un grafo y una heurística.
if __name__ == "__main__":
    # Define la estructura del grafo de ejemplo. Los nodos son cadenas.
    grafo = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E', 'G'], # Añadimos un nodo 'G' y una arista a él.
        'G': ['F'] # Añadimos el nodo 'G' y su conexión de vuelta.
    }

    # Define las coordenadas para cada nodo. Esto es necesario para calcular la heurística geométrica.
    # Las claves son los nombres de los nodos, los valores son tuplas (x, y).
    coordenadas = {
        'A': (0, 0),
        'B': (1, 2),
        'C': (4, 0),
        'D': (1, 4),
        'E': (3, 3),
        'F': (4, 2),
        'G': (5, 5) # Coordenadas para el nuevo nodo 'G'.
    }

    # Define una función heurística 'h' que toma nombres de nodo y usa el diccionario 'coordenadas'
    # para obtener las coordenadas reales y luego aplicar la función 'heuristica_euclidiana'.
    def h(nodo, objetivo):
        # Obtiene las coordenadas del nodo actual y del objetivo usando el diccionario 'coordenadas'.
        # Llama a la función 'heuristica_euclidiana' con esas coordenadas.
        return heuristica_euclidiana(coordenadas[nodo], coordenadas[objetivo])

    # Define el nodo de inicio y el nodo objetivo para la búsqueda.
    inicio, objetivo = 'A', 'G' # Cambiamos el objetivo a 'G'.

    # Llama a la función de búsqueda voraz con el grafo, inicio, objetivo y la función heurística 'h'.
    # El resultado (el camino encontrado o None) se guarda en la variable 'camino'.
    camino = busqueda_voraz(grafo, inicio, objetivo, h)

    # Imprime el camino encontrado.
    print("Camino encontrado:", camino)