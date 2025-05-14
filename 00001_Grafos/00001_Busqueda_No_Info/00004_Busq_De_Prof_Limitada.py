# Define la función para realizar una Búsqueda en Profundidad Limitada de forma iterativa.
# Recibe cuatro argumentos:
# - grafo: Un diccionario que representa el grafo (clave: nodo, valor: lista de vecinos).
# - inicio: El nodo desde el cual comenzar la búsqueda.
# - objetivo: El nodo que se desea encontrar.
# - limite: La profundidad máxima a la que se explorará el grafo.
def busqueda_profundidad_limitada(grafo, inicio, objetivo, limite):
    # Inicializa una pila (usando una lista). Cada elemento es una tupla:
    # (nodo_actual, lista_del_camino_hasta_este_nodo, profundidad_actual_del_nodo).
    # Empezamos con el nodo inicial, un camino que solo lo contiene, y una profundidad de 0.
    pila = [(inicio, [inicio], 0)]  # Pila: [(nodo, camino, profundidad)]

    # Inicializa un conjunto para mantener un registro de los nodos visitados en esta exploración.
    # Ayuda a evitar ciclos si el grafo los tiene dentro del límite de profundidad.
    visitados = set()

    # Inicia el bucle principal. Continúa mientras haya elementos en la pila.
    while pila:
        # Saca el último elemento (la tupla nodo, camino, profundidad) de la pila.
        actual, camino, profundidad = pila.pop()

        # Comprueba si el nodo actual es el objetivo.
        if actual == objetivo:
            # Si es el objetivo, retorna el camino encontrado. Hemos llegado al objetivo.
            return camino

        # Comprueba si el nodo actual no ha sido visitado Y si la profundidad actual es menor que el límite permitido.
        # Solo exploramos los vecinos de un nodo si no hemos excedido la profundidad máxima Y no lo hemos visitado ya (en esta rama).
        if actual not in visitados and profundidad < limite:
            # Si cumplimos las condiciones, marcamos el nodo actual como visitado.
            visitados.add(actual)

            # Explora los vecinos del nodo actual.
            # Itera sobre los vecinos en orden inverso para que el orden de exploración sea consistente con DFS.
            # (El primer vecino en el orden original del grafo es el último en la lista invertida, por lo tanto, el primero en ser añadido a la pila y explorado).
            for vecino in reversed(grafo[actual]):
                # Para cada vecino, si no ha sido visitado:
                # Nota: Este 'if vecino not in visitados' es opcional en DLS si el grafo no tiene ciclos o si los ciclos
                # no son más profundos que el límite. Pero ayuda a evitar trabajo redundante si hay ciclos superficiales.
                if vecino not in visitados:
                     # Añade una nueva tupla (vecino, camino_extendido, profundidad_aumentada) a la pila.
                    # El camino se extiende con el vecino, y la profundidad se incrementa en 1.
                    pila.append((vecino, camino + [vecino], profundidad + 1))

    # Si el bucle 'while pila:' termina y no se ha encontrado el objetivo (nunca se ejecutó el 'return camino'),
    # significa que el objetivo no existe dentro del límite de profundidad especificado.
    return None  # No se encontró el objetivo en el límite dado

# Define la función para realizar una Búsqueda en Profundidad Limitada de forma recursiva.
# Recibe argumentos similares, incluyendo el límite, más argumentos opcionales para el estado de la recursión.
# - grafo, nodo (actual), objetivo: Similar a la versión iterativa.
# - limite: El límite de profundidad restante para la exploración desde este nodo.
# - visitados, camino: Argumentos opcionales para mantener el estado a través de las llamadas recursivas.
def dls_recursiva(grafo, nodo, objetivo, limite, visitados=None, camino=None):
    # Inicializa el conjunto de visitados si es la primera llamada.
    if visitados is None:
        visitados = set()
    # Inicializa la lista del camino si es la primera llamada.
    if camino is None:
        camino = []

    # Marca el nodo actual como visitado.
    visitados.add(nodo)
    # Añade el nodo actual al camino. Crea una nueva lista para evitar modificar la lista original de la llamada anterior.
    camino = camino + [nodo]

    # Comprueba si el nodo actual es el objetivo.
    if nodo == objetivo:
        # Si es el objetivo, retorna el camino encontrado.
        return camino

    # Comprueba si el límite de profundidad ha sido alcanzado o excedido.
    if limite <= 0:
        # Si el límite es <= 0, significa que no podemos explorar más profundamente desde este nodo.
        # Retorna None, indicando que el objetivo no fue encontrado en esta rama dentro del límite restante.
        return None  # Se alcanza el límite de profundidad

    # Explora los vecinos del nodo actual.
    # Itera sobre cada vecino del nodo 'nodo'.
    for vecino in grafo[nodo]:
        # Para cada vecino, comprueba si no ha sido visitado.
        # Es importante chequear visitados aquí para evitar llamadas recursivas a nodos ya explorados (y posibles ciclos).
        if vecino not in visitados:
            # Si el vecino no ha sido visitado, realiza una llamada recursiva para explorar esa rama.
            # Pasa el vecino como nuevo nodo actual, el objetivo, el límite decrementado en 1,
            # el conjunto de visitados actualizado y el camino actual.
            resultado = dls_recursiva(grafo, vecino, objetivo, limite - 1, visitados, camino)
            # Después de la llamada recursiva, comprueba si la exploración de esa rama encontró el objetivo.
            if resultado:
                # Si la rama recursiva encontró el objetivo, retorna el camino encontrado.
                return resultado

    # Si el bucle sobre los vecinos termina y ninguna llamada recursiva encontró el objetivo
    # desde este nodo dentro del límite restante, retorna None.
    return None  # Si ningún camino fue válido desde este nodo dentro del límite

# Este bloque de código se ejecuta solo cuando el script se corre directamente.
# Contiene el ejemplo de cómo usar ambas funciones de DLS.
if __name__ == "__main__":
    # Define la estructura del grafo de ejemplo.
    grafo = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }

    # Define el nodo de inicio, el nodo objetivo y el límite de profundidad.
    inicio = 'A'
    objetivo = 'F'
    limite = 3 # Establecemos un límite de profundidad, por ejemplo, 3.

    # Muestra un encabezado para la versión iterativa.
    print("Versión iterativa:")
    # Llama a la función de búsqueda en profundidad limitada iterativa.
    # El resultado (el camino o None) se guarda en 'camino'.
    camino = busqueda_profundidad_limitada(grafo, inicio, objetivo, limite)
    # Imprime el resultado. Si se encontró camino, lo une con " -> ". Si no, indica que no se encontró dentro del límite.
    print(" -> ".join(camino) if camino else f"No se encontró camino con límite {limite}")

    # Muestra un encabezado para la versión recursiva.
    print("\nVersión recursiva:")
    # Llama a la función de búsqueda en profundidad limitada recursiva.
    # El resultado se guarda en 'camino_rec'.
    camino_rec = dls_recursiva(grafo, inicio, objetivo, limite)
    # Imprime el resultado de la versión recursiva, similar a la iterativa.
    print(" -> ".join(camino_rec) if camino_rec else f"No se encontró camino con límite {limite}")