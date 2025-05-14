# Define la función principal para la Búsqueda en Profundidad Iterativa (IDDFS).
# IDDFS combina BFS y DFS: realiza búsquedas en profundidad incrementando gradualmente un límite de profundidad.
# Garantiza encontrar el camino más corto en grafos no ponderados (como BFS) y usa menos memoria que BFS en muchos casos.
# Recibe tres argumentos:
# - grafo: Diccionario representando el grafo.
# - inicio: Nodo de inicio.
# - objetivo: Nodo a encontrar.
def busqueda_profundidad_iterativa(grafo, inicio, objetivo):
    # Define una función anidada 'dls' (Depth-Limited Search) que realiza la búsqueda en profundidad hasta un límite dado.
    # Esta función recursiva es la que se llama repetidamente con límites crecientes.
    # Recibe:
    # - nodo: El nodo actual que se está explorando.
    # - objetivo: El nodo a encontrar (el mismo que el de la función exterior).
    # - limite: La profundidad máxima restante para explorar desde este 'nodo'.
    def dls(nodo, objetivo, limite):
        # Caso base 1: Si el nodo actual es el objetivo, hemos encontrado el camino.
        if nodo == objetivo:
            # Retorna una lista que contiene solo el nodo actual. Esto inicia la reconstrucción del camino.
            return [nodo]
        # Caso base 2: Si el límite de profundidad ha llegado a 0 (o menos), no podemos ir más profundo en esta rama.
        if limite == 0:
            # Retorna None para indicar que el objetivo no se encontró en esta rama dentro del límite.
            return None
        # Si no es el objetivo y el límite no se ha alcanzado, explora los vecinos.
        for vecino in grafo[nodo]:
            # Realiza una llamada recursiva para explorar el 'vecino', decrementando el límite en 1.
            resultado = dls(vecino, objetivo, limite - 1)
            # Después de la llamada recursiva, comprueba si esa rama encontró el objetivo.
            if resultado:
                # Si la llamada recursiva retornó un camino (no None), significa que el objetivo está en esa rama.
                # Reconstruye el camino añadiendo el nodo actual al principio del camino retornado por la llamada recursiva.
                return [nodo] + resultado
        # Si el bucle termina y ninguna llamada recursiva encontró el objetivo en esta rama, retorna None.
        return None

    # --- Lógica principal de IDDFS ---
    # Inicializa el límite de profundidad para la primera búsqueda DLS.
    profundidad = 0  # Límite inicial

    # Inicia un bucle infinito que irá incrementando el límite de profundidad.
    while True:
        # Llama a la función DLS recursiva desde el nodo 'inicio' con la 'profundidad' actual como límite.
        resultado = dls(inicio, objetivo, profundidad)  # DFS limitada

        # Comprueba si la llamada DLS actual encontró el objetivo (si 'resultado' no es None).
        if resultado:
            # Si se encontró el objetivo, retorna el camino encontrado.
            return resultado

        # Nota Importante: Esta versión básica no maneja explicitamente la inalcanzabilidad del objetivo.
        # Si el objetivo no existe en el grafo, el bucle 'while True' continuará indefinidamente,
        # explorando a profundidades cada vez mayores. Para grafos finitos y alcanzables, esto funciona.
        # Una implementación más robusta podría necesitar una condición de parada si se determina
        # que no hay más nodos para explorar en todo el grafo (por ejemplo, si una DLS a profundidad P
        # no encuentra el objetivo y no visita ningún nodo nuevo más allá de la profundidad P-1).

        # Si el objetivo no se encontró en la DLS actual, incrementa el límite de profundidad para la siguiente iteración.
        profundidad += 1  # Aumenta el límite para intentar más profundo

# Define una segunda función para IDDFS, esta vez utilizando una implementación iterativa de DLS
# dentro del bucle principal, y gestionando un conjunto de visitados por cada iteración DLS.
def iddfs_completo(grafo, inicio, objetivo):
    # Inicializa el límite de profundidad.
    profundidad = 0

    # Bucle principal que incrementa el límite de profundidad en cada iteración.
    while True:
        # --- Lógica de una única búsqueda DLS iterativa ---
        # Inicializa un conjunto de visitados. SE REINICIA EN CADA NUEVA PROFUNDIDAD para permitir que
        # nodos en niveles superiores que fueron visitados puedan ser revisitados en niveles inferiores si hay un camino.
        visitados = set()
        # Inicializa la pila para la DLS iterativa. Cada elemento es (nodo, camino_hasta_nodo, nivel_de_profundidad).
        pila = [(inicio, [inicio], 0)]  # (nodo, camino actual, nivel)
        # Variable para almacenar el camino encontrado, si lo hay. Inicialmente None.
        encontrado = None

        # Bucle interno para la Búsqueda en Profundidad Limitada (DLS) para la 'profundidad' actual.
        while pila:
            # Saca el último elemento de la pila.
            nodo, camino, nivel = pila.pop()

            # Comprueba si el nodo actual es el objetivo.
            if nodo == objetivo:
                # Si es el objetivo, almacena el camino y rompe el bucle DLS interno.
                encontrado = camino
                break

            # Explora el nodo si está dentro del límite de profundidad actual Y no ha sido visitado
            # en esta iteración de DLS (para evitar ciclos *dentro* de esta DLS).
            if nivel < profundidad and nodo not in visitados:
                # Si cumple las condiciones, marca el nodo como visitado en esta iteración DLS.
                visitados.add(nodo)
                # Itera sobre los vecinos del nodo actual en orden inverso para mantener el comportamiento DFS.
                for vecino in reversed(grafo[nodo]):
                    # Si el vecino no ha sido visitado en esta iteración DLS:
                    if vecino not in visitados:
                         # Añade el vecino a la pila con el camino actualizado y el nivel de profundidad incrementado.
                         # La profundidad + 1 asegura que se explora un nivel más abajo.
                         pila.append((vecino, camino + [vecino], nivel + 1))

        # --- Fin de una única búsqueda DLS iterativa ---

        # Después de que la DLS para la profundidad actual termina:
        # Comprueba si se encontró el objetivo en esta iteración DLS.
        if encontrado:
            # Si se encontró, retorna el camino encontrado.
            return encontrado

        # Comprueba si la pila está vacía. Si está vacía y el objetivo no fue encontrado,
        # significa que se han explorado todos los nodos alcanzables dentro del límite de profundidad actual
        # y no hay más nodos en la pila para seguir explorando. Esto puede indicar que el objetivo es inalcanzable.
        # Sin embargo, en IDDFS, esto a menudo se combina con la condición de que no se visitó ningún nodo nuevo en el último nivel.
        # Una verificación más robusta de inalcanzabilidad podría requerir comparar los nodos visitados con la iteración anterior.
        # En este código, `if not pila` sirve como una condición de parada simple si la búsqueda se "agota" completamente.
        if not pila and not encontrado:
            # Si la pila está vacía y no se encontró el objetivo, rompemos el bucle principal (el objetivo es inalcanzable).
             break  # No quedan caminos por explorar dentro de este enfoque (puede indicar inalcanzabilidad)

        # Si el objetivo no se encontró y aún hay posibilidad de explorar más profundo (la pila no está vacía o se encontró un camino que no era el objetivo),
        # incrementa el límite de profundidad para la próxima iteración del bucle principal.
        profundidad += 1

    # Si el bucle principal 'while True' termina (porque se rompió), significa que el objetivo no fue encontrado
    # después de explorar todas las profundidades posibles.
    return None # Si no se encontró el objetivo después de todas las iteraciones de profundidad

# Este bloque de código se ejecuta solo cuando el script se corre directamente (no cuando es importado).
# Contiene el ejemplo de cómo usar ambas funciones de IDDFS.
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
    inicio, objetivo = 'A', 'F'

    # Muestra un encabezado para la primera versión (usando DLS recursiva).
    print("Versión básica (con DLS recursiva):")
    # Llama a la función IDDFS básica.
    camino = busqueda_profundidad_iterativa(grafo, inicio, objetivo)
    # Imprime el resultado. Si se encontró camino, lo une con " -> ". Si no, indica que no se encontró.
    print(" -> ".join(camino) if camino else "Camino no encontrado")

    # Muestra un encabezado para la segunda versión (con DLS iterativa y visitados por nivel).
    print("\nVersión completa (con DLS iterativa y seguimiento de visitados):")
    # Llama a la función IDDFS completa.
    camino_completo = iddfs_completo(grafo, inicio, objetivo)
    # Imprime el resultado de la versión completa.
    print(" -> ".join(camino_completo) if camino_completo else "Camino no encontrado")