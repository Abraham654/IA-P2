# Importa la clase deque del módulo collections.
# 'deque' es una estructura de datos que permite añadir y eliminar elementos eficientemente de ambos extremos,
# lo que la hace perfecta para actuar como una cola (usando append y popleft) o como una pila (usando append y pop).
from collections import deque  # Cola doble para manejar FIFO (BFS) o LIFO (DFS)

# Define la función de búsqueda general que puede realizar BFS o DFS.
# Recibe tres argumentos obligatorios y uno opcional:
# - grafo: Un diccionario que representa el grafo.
# - inicio: El nodo desde el cual comenzar la búsqueda.
# - objetivo: El nodo que se desea encontrar.
# - estrategia: Una cadena ('bfs' o 'dfs') para determinar qué algoritmo usar. Por defecto es 'bfs'.
def busqueda_grafo(grafo, inicio, objetivo, estrategia='bfs'):
    # Caso trivial: Si el nodo de inicio es el mismo que el nodo objetivo, ya hemos llegado.
    if inicio == objetivo:
        # Retorna una lista que contiene solo el nodo (el camino es simplemente el nodo).
        return [inicio]  # Caso trivial

    # Inicializa la estructura que actuará como cola para BFS o pila para DFS.
    # Se inicializa con el nodo de inicio.
    cola = deque([inicio])  # Cola para BFS o pila para DFS

    # Inicializa un diccionario para rastrear los nodos visitados y su predecesor.
    # El predecesor es el nodo desde el cual llegamos a este nodo en la búsqueda.
    # Esto es necesario para reconstruir el camino una vez que se encuentra el objetivo.
    # El nodo inicial no tiene predecesor, se marca con None.
    visitados = {inicio: None}  # Guarda nodos visitados y su predecesor

    # Inicia el bucle principal de la búsqueda. Continúa mientras la cola (o pila) no esté vacía.
    while cola:
        # Decide qué elemento extraer según la estrategia:
        # - Si estrategia es 'bfs', usa popleft() para extraer el primer elemento (FIFO - Cola).
        # - Si estrategia es diferente de 'bfs' (esperamos 'dfs'), usa pop() para extraer el último elemento (LIFO - Pila).
        actual = cola.popleft() if estrategia == 'bfs' else cola.pop() # Extrae nodo según estrategia: BFS usa popleft, DFS usa pop

        # Comprueba si el nodo actual extraído es el objetivo.
        if actual == objetivo:
            # Si es el objetivo, hemos encontrado el camino.
            # Inicializa una lista vacía para construir el camino.
            camino = []
            # Retrocede desde el nodo objetivo hasta el inicio usando el diccionario 'visitados'.
            while actual is not None:
                # Añade el nodo actual a la lista (temporalmente estará en orden inverso: objetivo -> ... -> inicio).
                camino.append(actual)
                # Se mueve al predecesor de este nodo.
                actual = visitados[actual]
            # Invierte la lista del camino para que vaya desde el inicio hasta el objetivo.
            return camino[::-1]  # Invertir para ir de inicio a objetivo

        # Explora los vecinos del nodo actual.
        # grafo.get(actual, []) accede a la lista de vecinos del nodo 'actual'.
        # Si 'actual' no existe como clave en 'grafo', devuelve una lista vacía [], evitando un error Key Error.
        for vecino in grafo.get(actual, []):  # .get() evita errores si no tiene vecinos
            # Para cada vecino, comprueba si no ha sido visitado aún.
            if vecino not in visitados:
                # Si el vecino no ha sido visitado:
                # Lo marca como visitado y registra 'actual' como su predecesor.
                visitados[vecino] = actual
                # Añade el vecino a la cola (o pila) para su posterior exploración.
                # El método append() funciona correctamente tanto para colas (donde popleft saca del otro lado)
                # como para pilas (donde pop saca del mismo lado).
                cola.append(vecino)  # Mismo método para BFS y DFS

    # Si el bucle 'while cola:' termina (la cola/pila se vació) y no se encontró el objetivo,
    # significa que el objetivo no es alcanzable desde el nodo de inicio.
    return None  # No se encontró camino

# Este bloque de código solo se ejecuta cuando el script se corre directamente.
# Contiene ejemplos de cómo usar la función 'busqueda_grafo' con ambas estrategias.
if __name__ == "__main__":
    # Define la estructura del grafo de ejemplo usando un diccionario.
    grafo = {
        'A': ['B', 'C'], # El nodo 'A' tiene vecinos 'B' y 'C'.
        'B': ['A', 'D', 'E'], # El nodo 'B' tiene vecinos 'A', 'D' y 'E'.
        'C': ['A', 'F'], # ...y así sucesivamente.
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }

    # Define el nodo de inicio y el nodo objetivo para las búsquedas.
    inicio, objetivo = 'A', 'F'

    # --- Ejemplo de uso para BFS ---
    print("BFS (Anchura):")
    # Llama a la función 'busqueda_grafo' con estrategia 'bfs'.
    # Aunque el valor por defecto es 'bfs', lo especificamos explícitamente aquí por claridad.
    print("Camino:", busqueda_grafo(grafo, inicio, objetivo, 'bfs'))

    # --- Ejemplo de uso para DFS ---
    print("\nDFS (Profundidad):")
    # Llama a la función 'busqueda_grafo' con estrategia 'dfs'.
    print("Camino:", busqueda_grafo(grafo, inicio, objetivo, 'dfs'))