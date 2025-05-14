# Importa la clase deque del módulo collections. 'deque' es una implementación de una cola doblemente terminada,
# que es eficiente para operaciones de añadir y eliminar elementos de ambos lados. Es ideal para implementar
# colas (FIFO) que se necesitan en algoritmos de búsqueda como BFS y, en este caso, en la búsqueda bidireccional.
from collections import deque  # Cola eficiente para recorrido BFS

# Define la función para realizar una Búsqueda Bidireccional.
# Este algoritmo ejecuta dos búsquedas simultáneas (una desde el inicio y otra desde el objetivo)
# hasta que se encuentran en un nodo común.
# Recibe tres argumentos:
# - grafo: Un diccionario que representa el grafo.
# - inicio: El nodo desde el cual comienza la primera búsqueda.
# - objetivo: El nodo hacia el cual se dirige la segunda búsqueda.
def busqueda_bidireccional(grafo, inicio, objetivo):
    # Caso trivial: Si el nodo de inicio es el mismo que el nodo objetivo, ya hemos llegado.
    if inicio == objetivo:
        # Retorna una lista que contiene solo el nodo (el camino es simplemente el nodo).
        return [inicio]  # Caso trivial

    # Inicializa las estructuras de datos para la búsqueda desde el inicio (forward search).
    # cola_inicio: Cola de nodos a visitar desde el inicio. Empieza con el nodo 'inicio'.
    cola_inicio = deque([inicio])
    # visitado_inicio: Diccionario para rastrear los nodos visitados desde el inicio
    # y almacenar el predecesor (el nodo desde el que llegamos a este nodo).
    # Esto es crucial para reconstruir el camino después.
    visitado_inicio = {inicio: None} # {nodo: predecesor}

    # Inicializa las estructuras de datos para la búsqueda desde el objetivo (backward search).
    # cola_objetivo: Cola de nodos a visitar desde el objetivo (explorando "hacia atrás"). Empieza con el nodo 'objetivo'.
    cola_objetivo = deque([objetivo])
    # visitado_objetivo: Diccionario para rastrear los nodos visitados desde el objetivo
    # y almacenar el predecesor (el nodo desde el que llegamos a este nodo en la búsqueda hacia atrás).
    visitado_objetivo = {objetivo: None} # {nodo: predecesor}

    # Variable para almacenar el nodo donde se encuentran las dos búsquedas (la intersección). Inicialmente es None.
    nodo_interseccion = None

    # Inicia el bucle principal. Continúa mientras ambas colas tengan nodos para explorar.
    # Si alguna cola se vacía antes de encontrar una intersección, significa que no hay camino.
    while cola_inicio and cola_objetivo:
        # --- Expansión desde el Inicio ---
        # Saca el primer nodo de la cola de inicio (FIFO).
        actual_i = cola_inicio.popleft()

        # Comprueba si el nodo actual de la búsqueda desde el inicio ya ha sido visitado por la búsqueda desde el objetivo.
        # Esta es la condición de intersección.
        if actual_i in visitado_objetivo:
            # Si se encuentra una intersección, guarda el nodo de intersección.
            nodo_interseccion = actual_i
            # Rompe el bucle principal porque se ha encontrado un camino.
            break

        # Explora los vecinos del nodo actual de la búsqueda desde el inicio.
        for vecino in grafo[actual_i]:
            # Para cada vecino, comprueba si no ha sido visitado aún por la búsqueda desde el inicio.
            if vecino not in visitado_inicio:
                # Si no ha sido visitado, lo marca como visitado desde el inicio, registrando 'actual_i' como su predecesor.
                visitado_inicio[vecino] = actual_i
                # Añade el vecino al final de la cola de inicio para su posterior exploración.
                cola_inicio.append(vecino)

        # --- Expansión desde el Objetivo ---
        # Saca el primer nodo de la cola del objetivo (FIFO).
        actual_o = cola_objetivo.popleft()

        # Comprueba si el nodo actual de la búsqueda desde el objetivo ya ha sido visitado por la búsqueda desde el inicio.
        # Esta es la otra posible condición de intersección.
        if actual_o in visitado_inicio:
            # Si se encuentra una intersección, guarda el nodo de intersección.
            nodo_interseccion = actual_o
            # Rompe el bucle principal.
            break

        # Explora los vecinos del nodo actual de la búsqueda desde el objetivo.
        for vecino in grafo[actual_o]:
            # Para cada vecino, comprueba si no ha sido visitado aún por la búsqueda desde el objetivo.
            if vecino not in visitado_objetivo:
                # Si no ha sido visitado, lo marca como visitado desde el objetivo, registrando 'actual_o' como su predecesor.
                visitado_objetivo[vecino] = actual_o
                # Añade el vecino al final de la cola del objetivo.
                cola_objetivo.append(vecino)

    # Después del bucle principal, verifica si se encontró un nodo de intersección.
    if nodo_interseccion:
        # Si se encontró una intersección, reconstruye el camino completo.

        # --- Reconstrucción del camino desde el inicio hasta la intersección ---
        # Inicializa una lista para almacenar la primera parte del camino.
        camino = []
        # Comienza desde el nodo de intersección.
        nodo = nodo_interseccion
        # Retrocede desde la intersección hasta el inicio usando los predecesores almacenados en 'visitado_inicio'.
        while nodo is not None:
            # Añade el nodo actual a la lista (temporalmente estará en orden inverso).
            camino.append(nodo)
            # Se mueve al predecesor de este nodo en la búsqueda desde el inicio.
            nodo = visitado_inicio[nodo]
        # Invierte la lista para que el camino vaya desde el inicio hasta la intersección.
        camino.reverse()  # Orden correcto: inicio → intersección

        # --- Reconstrucción y unión de la parte desde la intersección hasta el objetivo ---
        # Comienza desde el predecesor del nodo de intersección en la búsqueda desde el objetivo.
        # No incluimos el 'nodo_interseccion' de nuevo porque ya está al final de la primera parte del camino.
        nodo = visitado_objetivo[nodo_interseccion]
        # Avanza desde el predecesor de la intersección (en la búsqueda hacia atrás) hasta el objetivo
        # usando los predecesores almacenados en 'visitado_objetivo'.
        while nodo is not None:
            # Añade el nodo actual a la lista del camino.
            camino.append(nodo)
            # Se mueve al predecesor de este nodo en la búsqueda desde el objetivo.
            nodo = visitado_objetivo[nodo]

        # Retorna el camino completo combinado.
        return camino

    # Si el bucle principal terminó y no se encontró un nodo de intersección, significa que no hay un camino
    # entre el nodo de inicio y el nodo objetivo en este grafo.
    return None  # Si no hay conexión entre los nodos

# Este bloque de código solo se ejecuta cuando el script se corre directamente.
# Contiene un ejemplo de cómo usar la función de búsqueda bidireccional.
if __name__ == "__main__":
    # Define la estructura del grafo de ejemplo usando un diccionario.
    grafo = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }

    # Define el nodo de inicio y el nodo objetivo para la búsqueda.
    inicio = 'A'
    objetivo = 'F'

    # Llama a la función de búsqueda bidireccional con el grafo, inicio y objetivo.
    # El resultado (el camino o None) se guarda en la variable 'camino'.
    camino = busqueda_bidireccional(grafo, inicio, objetivo)

    # Imprime el resultado. Usa una f-string y un operador ternario:
    # Si 'camino' existe (no es None), imprime "Camino encontrado: [lista del camino]".
    # Si 'camino' es None, imprime "No se encontró camino".
    print(f"Camino encontrado: {camino}" if camino else "No se encontró camino")