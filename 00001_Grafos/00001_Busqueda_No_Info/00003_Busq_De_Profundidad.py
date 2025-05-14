# Define la función para realizar una Búsqueda en Profundidad de forma iterativa.
# Recibe tres argumentos:
# - grafo: Un diccionario que representa el grafo (clave: nodo, valor: lista de vecinos).
# - inicio: El nodo desde el cual comenzar la búsqueda.
# - objetivo: El nodo que se desea encontrar.
def busqueda_profundidad(grafo, inicio, objetivo):
    # Inicializa una pila (usando una lista de Python, donde pop() elimina el último elemento, imitando una pila).
    # Cada elemento en la pila es una tupla: (nodo_actual, lista_del_camino_hasta_este_nodo).
    # Empezamos con el nodo inicial y un camino que solo contiene el nodo inicial.
    pila = [(inicio, [inicio])]  # Pila: [(nodo actual, camino hasta él)]

    # Inicializa un conjunto para mantener un registro de los nodos ya visitados.
    # Usar un conjunto permite verificaciones rápidas (promedio O(1)) para evitar revisitar nodos y caer en ciclos infinitos.
    visitados = set()  # Conjunto para evitar ciclos

    # Inicia el bucle principal. Continúa mientras haya elementos en la pila.
    while pila:
        # Saca el último elemento (la tupla nodo, camino) de la pila.
        # En DFS, siempre exploramos el nodo añadido más recientemente (comportamiento de pila LIFO).
        actual, camino = pila.pop()  # Tomamos el último nodo insertado

        # Comprueba si el nodo actual es el objetivo que estamos buscando.
        if actual == objetivo:
            # Si es el objetivo, hemos encontrado un camino (no necesariamente el más corto, a diferencia de BFS).
            # Retorna la lista del camino que lleva desde el inicio hasta este nodo.
            return camino

        # Comprueba si el nodo actual no ha sido visitado aún.
        # Este chequeo es crucial para evitar procesar el mismo nodo varias veces y prevenir ciclos.
        if actual not in visitados:
            # Si el nodo no ha sido visitado:
            # Lo añade al conjunto de visitados para no procesarlo de nuevo.
            visitados.add(actual)

            # Explora los vecinos del nodo actual.
            # Iteramos sobre los vecinos en orden inverso. Esto se hace para que, al agregarlos a la pila,
            # el primer vecino en el orden original del grafo[actual] sea el *último* en entrar a la pila y,
            # por lo tanto, el *primero* en ser sacado y explorado en la siguiente iteración del bucle.
            # Esto asegura que la exploración siga el orden definido en el grafo para los vecinos.
            for vecino in reversed(grafo[actual]):
                # Para cada vecino, comprueba si no ha sido visitado.
                if vecino not in visitados:
                    # Si el vecino no ha sido visitado:
                    # Añade una nueva tupla (vecino, camino_extendido) a la pila.
                    # El camino_extendido es la lista del camino actual más el vecino.
                    pila.append((vecino, camino + [vecino]))

    # Si el bucle 'while pila:' termina y no se ha encontrado el objetivo (nunca se ejecutó el 'return camino'),
    # significa que el objetivo no es alcanzable desde el nodo de inicio en este grafo.
    return None  # Si no se encuentra camino

# Define la función para realizar una Búsqueda en Profundidad de forma recursiva.
# Recibe argumentos similares a la versión iterativa, más argumentos opcionales para mantener el estado de la recursión.
# - grafo, inicio, objetivo: Igual que en la versión iterativa.
# - visitados: Un conjunto para rastrear nodos visitados (se inicializa si es la primera llamada).
# - camino: Una lista para construir el camino actual (se inicializa si es la primera llamada).
def busqueda_profundidad_recursiva(grafo, inicio, objetivo, visitados=None, camino=None):
    # Comprueba si es la primera llamada a la función para inicializar el conjunto de visitados.
    if visitados is None:
        visitados = set()
    # Comprueba si es la primera llamada a la función para inicializar la lista del camino.
    if camino is None:
        camino = []

    # Marca el nodo 'inicio' (el nodo actual en la recursión) como visitado.
    visitados.add(inicio)
    # Añade el nodo 'inicio' al camino actual. Crea una nueva lista para evitar modificar la lista
    # que podría estar siendo usada por otras ramas de la recursión (imutabilidad en este paso).
    camino = camino + [inicio]

    # Comprueba si el nodo actual ('inicio') es el objetivo.
    if inicio == objetivo:
        # Si es el objetivo, retorna el camino actual. La recursión comenzará a "desenrollarse" desde aquí.
        return camino

    # Explora los vecinos del nodo actual.
    # Itera sobre cada vecino del nodo 'inicio' según la definición del 'grafo'.
    for vecino in grafo[inicio]:
        # Para cada vecino, comprueba si no ha sido visitado aún.
        if vecino not in visitados:
            # Si el vecino no ha sido visitado, realiza una llamada recursiva a la función
            # para explorar esa rama del grafo, pasando el vecino como nuevo 'inicio', el objetivo,
            # el conjunto de visitados actualizado y el camino actual.
            resultado = busqueda_profundidad_recursiva(grafo, vecino, objetivo, visitados, camino)
            # Después de que la llamada recursiva retorna, comprueba si encontró el objetivo en esa rama.
            if resultado:
                # Si la llamada recursiva encontró el objetivo (retornó un camino no nulo),
                # propaga ese resultado hacia arriba en la cadena de llamadas recursivas.
                return resultado

    # Si el bucle sobre los vecinos termina y ninguna llamada recursiva encontró el objetivo
    # desde este nodo, significa que el objetivo no está en esta rama del grafo.
    # Retorna None para indicar que no se encontró el camino desde este punto.
    return None

# Este bloque de código solo se ejecuta cuando el script se corre directamente.
# Contiene el ejemplo de cómo usar ambas funciones.
if __name__ == "__main__":
    # Define la estructura del grafo usando un diccionario, similar al ejemplo de BFS.
    # Las claves son los nodos y los valores son listas de sus vecinos.
    grafo = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }

    # Define el nodo de inicio y el nodo objetivo para la búsqueda.
    inicio, objetivo = 'A', 'F'

    # Muestra un encabezado para la versión iterativa.
    print("Versión iterativa:")
    # Llama a la función de búsqueda en profundidad iterativa.
    # El resultado (el camino o None) se guarda en la variable 'camino'.
    camino = busqueda_profundidad(grafo, inicio, objetivo)
    # Imprime el resultado. Usa un operador ternario: si 'camino' existe, une los nodos con " -> "; si no, imprime "No se encontró camino".
    print(" -> ".join(camino) if camino else "No se encontró camino")

    # Muestra un encabezado para la versión recursiva.
    print("\nVersión recursiva:")
    # Llama a la función de búsqueda en profundidad recursiva.
    # El resultado (el camino o None) se guarda en la variable 'camino_rec'.
    camino_rec = busqueda_profundidad_recursiva(grafo, inicio, objetivo)
    # Imprime el resultado de la versión recursiva, similar a la iterativa.
    print(" -> ".join(camino_rec) if camino_rec else "No se encontró camino")