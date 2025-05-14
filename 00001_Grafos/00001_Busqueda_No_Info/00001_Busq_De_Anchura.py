# Importa la clase deque del módulo collections. deque (double-ended queue) es una estructura de datos
# similar a una lista pero optimizada para añadir y eliminar elementos eficientemente de ambos extremos.
# Es ideal para implementar colas (FIFO - First In, First Out).
from collections import deque  # Estructura eficiente para manejar la cola

# Define la función principal que implementa el algoritmo de Búsqueda en Anchura.
# Recibe tres argumentos:
# - grafo: Un diccionario que representa el grafo (clave: nodo, valor: lista de vecinos).
# - inicio: El nodo desde el cual comenzar la búsqueda.
# - objetivo: El nodo que se desea encontrar.
def busqueda_anchura(grafo, inicio, objetivo):
    # Inicializa la cola con el nodo de inicio. La cola almacena los nodos a visitar.
    # Usamos deque para operaciones eficientes de 'popleft'.
    cola = deque([inicio])  # Cola FIFO con el nodo inicial

    # Inicializa un diccionario para rastrear los nodos visitados y quién fue su "padre"
    # (el nodo desde el cual llegamos a ellos). Esto es crucial para reconstruir el camino.
    # El nodo inicial se marca como visitado y su padre es None (no llegamos a él desde otro nodo en la búsqueda).
    visitados = {inicio: None}  # Almacena nodos visitados y sus padres

    # Inicia el bucle principal del algoritmo. Continúa mientras haya nodos en la cola por visitar.
    while cola:
        # Saca el primer nodo de la cola. Esta es la característica FIFO de la búsqueda en anchura.
        actual = cola.popleft()  # Sacamos el primer nodo en la cola

        # Comprueba si el nodo actual es el objetivo que estamos buscando.
        if actual == objetivo:  # Si encontramos el objetivo, reconstruimos el camino
            # Si el nodo actual es el objetivo, hemos encontrado el camino más corto desde el inicio (en número de aristas).
            # Inicializamos una lista vacía para almacenar el camino.
            camino = []
            # Iniciamos un bucle para reconstruir el camino hacia atrás desde el objetivo hasta el inicio
            # usando el diccionario 'visitados'.
            while actual is not None:
                # Añade el nodo actual al principio del camino (o al final temporalmente para invertirlo después).
                camino.append(actual)
                # Se mueve al nodo padre del nodo actual usando el diccionario 'visitados'.
                actual = visitados[actual]
            # Retorna el camino invertido (para que vaya de inicio a objetivo) usando slicing [::-1].
            return camino[::-1]  # Se invierte para ir de inicio a objetivo

        # Si el nodo actual no es el objetivo, exploramos sus vecinos.
        # Itera sobre cada vecino del nodo 'actual' según la definición del 'grafo'.
        for vecino in grafo[actual]:  # Exploramos vecinos no visitados
            # Comprueba si el vecino actual ya ha sido visitado.
            if vecino not in visitados:
                # Si el vecino no ha sido visitado:
                # Lo añade al final de la cola para ser visitado posteriormente.
                cola.append(vecino)
                # Lo marca como visitado y registra que llegamos a él desde el nodo 'actual'.
                visitados[vecino] = actual

    # Si el bucle 'while cola:' termina y no se ha encontrado el objetivo (nunca se ejecutó el 'return camino[::-1]'),
    # significa que el objetivo no es alcanzable desde el nodo de inicio.
    return None  # Si no se encuentra el objetivo

# Este bloque de código solo se ejecuta cuando el script se corre directamente (no cuando es importado como módulo).
# Es una práctica común para incluir ejemplos de uso o pruebas.
if __name__ == "__main__":
    # Define la estructura del grafo usando un diccionario.
    # Las claves son los nodos y los valores son listas de sus vecinos (nodos adyacentes).
    grafo = {
        'A': ['B', 'C'], # El nodo 'A' tiene vecinos 'B' y 'C'.
        'B': ['A', 'D', 'E'], # El nodo 'B' tiene vecinos 'A', 'D' y 'E'.
        'C': ['A', 'F'], # ... y así sucesivamente.
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }

    # Define el nodo de inicio para la búsqueda.
    inicio = 'A'
    # Define el nodo objetivo para la búsqueda.
    objetivo = 'F'
    # Llama a la función de búsqueda en anchura con el grafo, inicio y objetivo definidos.
    # El resultado (el camino o None) se guarda en la variable 'camino'.
    camino = busqueda_anchura(grafo, inicio, objetivo)

    # Comprueba si se encontró un camino (si 'camino' no es None).
    if camino:
        # Si se encontró un camino, lo imprime.
        # " -> ".join(camino) une los elementos de la lista 'camino' con la cadena " -> ".
        print("Camino encontrado:", " -> ".join(camino))
    else:
        # Si 'camino' es None (no se encontró el objetivo), imprime un mensaje indicándolo.
        print("Camino no encontrado")