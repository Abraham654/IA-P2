import heapq # Importa la librería 'heapq', que proporciona una implementación de una cola de prioridad (min-heap). Necesaria para A* y Búsqueda Voraz para extraer eficientemente el nodo con menor costo estimado.

# --- Implementación del algoritmo de Búsqueda A* (A-estrella) ---
# A* es un algoritmo de búsqueda del camino más corto en un grafo ponderado que utiliza una función heurística
# para guiar su búsqueda, combinando el costo real desde el inicio (g_score) con una estimación del costo hasta el objetivo (h_score).
# La prioridad de un nodo se basa en f_score = g_score + h_score.
# Recibe: grafo, inicio, objetivo, y una función heuristica h(nodo, objetivo).
def a_star(grafo, inicio, objetivo, heuristica):
    # Inicializa la 'frontera' como una cola de prioridad. Almacena tuplas (f_score, nodo).
    # heapq ordena por el primer elemento de la tupla.
    frontera = []  # Cola: (f_score, nodo)

    # Añade el nodo de inicio a la frontera. Su g_score es 0, por lo que su f_score inicial es h(inicio, objetivo).
    # heapq.heappush(heap, item) inserta el item en el heap.
    heapq.heappush(frontera, (heuristica(inicio, objetivo), inicio))

    # Diccionario para almacenar el costo real conocido (g_score) desde el nodo de inicio hasta cada nodo visitado.
    # Inicialmente, solo conocemos el costo al inicio, que es 0.
    g_score = {inicio: 0}  # Costo real desde el inicio

    # Diccionario para almacenar el nodo predecesor (padre) para reconstruir el camino óptimo.
    # El nodo de inicio no tiene padre.
    padres = {inicio: None}  # Rutas óptimas

    # Bucle principal del algoritmo A*. Continúa mientras haya nodos en la frontera.
    while frontera:
        # Extrae el nodo de la frontera con el menor f_score.
        # heapq.heappop(heap) extrae el elemento con menor prioridad.
        # Desempaquetamos la tupla, ignorando el f_score extraído (lo guardamos en _) y tomando el nodo.
        _, actual = heapq.heappop(frontera) # Saca el nodo con menor f_score

        # Comprueba si el nodo actual es el objetivo.
        if actual == objetivo:
            # Si es el objetivo, hemos encontrado el camino óptimo.
            # Inicializa una lista para reconstruir el camino.
            camino = []
            # Retrocede desde el objetivo usando el diccionario de padres.
            while actual: # Continúa hasta que lleguemos al nodo inicial (donde el padre es None).
                # Añade el nodo actual al camino.
                camino.append(actual)
                # Se mueve al nodo padre.
                actual = padres[actual]
            # Invierte el camino para que vaya de inicio a objetivo.
            # Retorna el camino invertido y el costo total para llegar al objetivo (el g_score del objetivo).
            return camino[::-1], g_score[objetivo] # Camino y costo total

        # Explora los vecinos del nodo actual.
        # Itera sobre los pares (vecino, costo_de_arista) del diccionario de vecinos en el grafo.
        for vecino, costo in grafo[actual].items():
            # Calcula el g_score tentativo para el vecino si llegamos a él a través del nodo actual.
            # Es el g_score del nodo actual más el costo de la arista hacia el vecino.
            g_tentativo = g_score[actual] + costo

            # Comprueba si este camino al vecino es mejor que cualquier camino encontrado anteriormente.
            # Esto ocurre si el vecino no ha sido visitado antes (no tiene g_score registrado)
            # O si el costo tentativo es menor que el g_score registrado para el vecino.
            if vecino not in g_score or g_tentativo < g_score[vecino]:
                # Si este camino es mejor:
                # Actualiza el padre del vecino para apuntar al nodo actual.
                padres[vecino] = actual
                # Actualiza el g_score del vecino con el costo real más bajo encontrado hasta ahora.
                g_score[vecino] = g_tentativo
                # Calcula el f_score para el vecino: g_score actualizado + heurística desde el vecino al objetivo.
                f_score = g_tentativo + heuristica(vecino, objetivo)
                # Añade el vecino a la cola de prioridad con su nuevo f_score.
                heapq.heappush(frontera, (f_score, vecino))

    # Si el bucle termina y no se encontró el objetivo, significa que es inalcanzable.
    # Retorna None para el camino y None para el costo.
    return None, None # No se encontró camino

# --- Implementación del algoritmo AO* ---
# AO* es un algoritmo de búsqueda del camino óptimo en grafos AND-OR.
# Los nodos OR implican que se puede elegir cualquiera de sus sub-problemas para resolver el problema actual.
# Los nodos AND implican que TODOS sus sub-problemas (representados como conjuntos) deben ser resueltos.
# El grafo para AO* tiene una estructura diferente a la de los grafos para A* o BFS/DFS.
# Recibe: grafo (con estructura AND/OR), inicio, objetivo, y una función heuristica h(nodo, objetivo).
def ao_star(grafo, inicio, objetivo, heuristica):
    # Diccionario para almacenar la solución encontrada hasta ahora para cada nodo.
    # La clave es el nodo, el valor es una tupla (costo óptimo estimado/conocido, camino óptimo encontrado hasta ahora).
    # Inicialmente, solo conocemos la solución para el objetivo (costo 0, camino a sí mismo).
    solucion = {objetivo: (0, [objetivo])}

    # Conjunto para rastrear los nodos que ya han sido expandidos (sus sucesores han sido considerados).
    expandido = set()

    # Función recursiva anidada para calcular/recalcular el costo óptimo desde un nodo y su camino.
    # Esto se hace propagando los costos hacia arriba desde los nodos expandidos.
    def costo(nodo):
        # Si la solución para este nodo ya ha sido calculada (está en 'solucion'), la retorna.
        if nodo in solucion:
            return solucion[nodo][0]

        # Si el nodo es un nodo en el grafo (no un nodo hoja no objetivo no definido).
        if nodo in grafo:
            # Comprueba si el nodo es un nodo OR (sus sucesores están en un diccionario con costos de arista).
            if isinstance(grafo[nodo], dict): # OR
                # Inicializa el mejor costo y camino para este nodo OR a infinito y None.
                mejor, camino = float('inf'), None
                # Itera sobre los hijos de este nodo OR y el costo de la arista hacia ellos.
                for hijo, c in grafo[nodo].items():
                    # Calcula el costo total tentativo para resolver el problema desde este nodo OR a través de este 'hijo'.
                    # Es el costo de la arista al hijo (c) más el costo (recursivo) para resolver el problema desde el 'hijo'.
                    total = c + costo(hijo) # Llamada recursiva a costo(hijo)
                    # Si este camino a través del 'hijo' es mejor que el mejor camino encontrado hasta ahora para este nodo OR.
                    if total < mejor:
                        # Actualiza el mejor costo para este nodo OR.
                        mejor = total
                        # Reconstruye el camino óptimo a través de este 'hijo' añadiendo el nodo actual al principio del camino óptimo del 'hijo'.
                        # Asumimos que la solución para 'hijo' ya ha sido calculada y está en solucion[hijo][1].
                        camino = [nodo] + solucion[hijo][1]
                # Después de revisar todos los hijos OR, actualiza la solución para este nodo con el mejor costo y camino encontrados.
                solucion[nodo] = (mejor, camino)
                # Retorna el mejor costo encontrado para este nodo OR.
                return mejor
            # Comprueba si el nodo es un nodo AND (sus sucesores están en una lista de conjuntos/diccionarios, donde cada conjunto/diccionario es un sub-problema que debe resolverse).
            else: # AND (grafo[nodo] es una lista de conjuntos/diccionarios, cada uno representa una parte de la conjunción)
                # Inicializa el costo total y el camino para este nodo AND.
                total, camino = 0, [nodo] # El costo para un nodo AND es la suma de los costos de sus sub-problemas.
                # Itera sobre cada conjunto/diccionario de sub-problemas que componen este nodo AND.
                for conjunto in grafo[nodo]: # 'conjunto' representa un sub-problema (o un grupo de alternativas para un sub-problema)
                    # Para cada sub-problema en la conjunción, encontramos la mejor manera de resolverlo.
                    mejor, subcamino = float('inf'), [] # Inicializa el mejor costo y subcamino para este sub-problema.
                    # Itera sobre los nodos dentro de este sub-problema (si un sub-problema es {'X': 5}, subnodo='X', costo_arista=5).
                    # Nota: La estructura del grafo para AND podría ser más variada. Esta implementación parece asumir
                    # que cada 'conjunto' en la lista es un diccionario {subnodo: costo_arista}.
                    for subnodo in conjunto: # 'subnodo' es un nodo que debe resolverse como parte de esta conjunción
                         # Calcula el valor total para resolver este 'subnodo' a través de la arista que lo conecta al nodo actual.
                         # Es el costo de la arista al subnodo (conjunto[subnodo]) más el costo (recursivo) para resolver el subnodo.
                        val = conjunto[subnodo] + costo(subnodo) # Llamada recursiva a costo(subnodo)
                        # Si este camino a través de este 'subnodo' es mejor que el mejor encontrado hasta ahora para este sub-problema.
                        if val < mejor:
                            # Actualiza el mejor costo para este sub-problema.
                            mejor = val
                            # Obtiene el subcamino óptimo para resolver este 'subnodo'.
                            subcamino = solucion[subnodo][1]
                    # Después de revisar todas las opciones para este sub-problema, suma su mejor costo al costo total del nodo AND.
                    total += mejor
                    # Concatena el subcamino óptimo encontrado para este sub-problema al camino total del nodo AND.
                    camino += subcamino # Concatenamos los subcaminos
                # Después de procesar todos los sub-problemas en la conjunción, actualiza la solución para este nodo AND.
                solucion[nodo] = (total, camino)
                # Retorna el costo total encontrado para este nodo AND.
                return total

        # Si el nodo no está definido en el grafo (es un nodo hoja que no es el objetivo),
        # significa que no tiene sucesores y no puede ser resuelto a menos que sea el objetivo.
        # Su costo es infinito.
        solucion[nodo] = (float('inf'), None) # No hay solución desde un nodo hoja no objetivo.
        return float('inf') # Retorna infinito.

    # --- Lógica principal de AO* ---
    # Bucle principal de AO*. Continúa mientras la solución para el nodo de inicio no sea definitiva
    # (aún no está en 'solucion' o su costo es infinito, indicando que aún no se ha encontrado un camino óptimo completo).
    while inicio not in solucion or solucion[inicio][0] == float('inf'):
        # Comienza a trazar el mejor camino parcial desde el inicio.
        nodo = inicio
        # Bucle interno para encontrar un nodo no expandido en el mejor camino parcial actual.
        while True:
            # Si el nodo actual no ha sido expandido, hemos encontrado nuestro nodo para expandir.
            if nodo not in expandido:
                break
            # Si el nodo ha sido expandido, pero no tiene una solución o su camino es None,
            # significa que el camino actual no lleva a una solución completa.
            if nodo not in solucion or not solucion[nodo][1]:
                # Si el camino actual no es viable, la solución desde el inicio es imposible por ahora.
                # Esto podría indicar inalcanzabilidad o que se necesita explorar otra rama.
                # En esta implementación, retornamos fallo.
                return None, None
            # Obtiene el mejor camino conocido desde el nodo actual.
            camino = solucion[nodo][1]
            # Se mueve al siguiente nodo en el mejor camino.
            # Si el camino tiene más de un nodo, toma el segundo elemento. Si solo tiene uno (el nodo actual),
            # significa que hemos llegado al final del camino parcial conocido que aún necesita expansión,
            # o es el nodo objetivo. Establecemos nodo a None para la verificación posterior.
            nodo = camino[1] if len(camino) > 1 else None
            # Si el siguiente nodo es None (llegamos al final del camino parcial y el último nodo ya fue expandido/resuelto),
            # significa que la solución actual no lleva a una expansión adicional, pero no ha llegado al objetivo
            # o se atascó. Esto podría indicar inalcanzabilidad o un problema.
            if nodo is None:
                return None, None

        # Una vez que el bucle interno encuentra un nodo 'nodo' que no ha sido expandido,
        # lo marca como expandido.
        expandido.add(nodo)
        # Llama a la función 'costo' en este nodo expandido.
        # Esto recalcula el costo y el camino desde este nodo hacia arriba en el árbol de solución parcial,
        # propagando cualquier mejora o nuevo camino encontrado.
        costo(nodo) # Recalcula costos desde este nodo hacia arriba

    # Cuando el bucle principal termina, significa que la solución para el nodo de inicio ha sido finalizada
    # y ya no es infinito.
    # Retorna el camino óptimo y el costo óptimo encontrados para el nodo de inicio.
    return solucion[inicio][1], solucion[inicio][0]

# --- Ejemplos de uso ---

# Grafo de ejemplo para A*. Es un grafo dirigido con pesos en las aristas.
# Usa diccionarios anidados: {nodo: {vecino: costo, ...}, ...}
grafo_a = {
    'A': {'B': 1, 'C': 3}, # Desde A, puedes ir a B con costo 1 o a C con costo 3.
    'B': {'D': 2, 'E': 4}, # Desde B, puedes ir a D con costo 2 o a E con costo 4.
    'C': {'F': 2},        # Desde C, puedes ir a F con costo 2.
    'D': {},              # D es un nodo terminal (sin sucesores).
    'E': {'F': 1},        # Desde E, puedes ir a F con costo 1.
    'F': {}               # F es un nodo terminal.
}

# Define una heurística simple que siempre retorna 0.
# Usar una heurística nula convierte A* efectivamente en el algoritmo de Dijkstra,
# que encuentra el camino más corto en grafos ponderados.
def h_simple(n, objetivo): return 0  # Heurística nula

# Llama a la función A* para encontrar un camino de 'A' a 'F' en grafo_a usando la heurística nula.
camino, costo = a_star(grafo_a, 'A', 'F', h_simple)
# Imprime el resultado de A*.
print(f"A*: Camino {camino}, Costo {costo}")

# Grafo de ejemplo para AO*. Este grafo incluye nodos AND y OR.
# La estructura del grafo es diferente:
# - Nodos OR (como 'A', 'C', 'E'): sus sucesores están en un diccionario {vecino: costo}. Se elige el mejor camino.
# - Nodos AND (como 'B'): sus sucesores están en una lista de diccionarios, donde cada diccionario representa un sub-problema que debe resolverse.
#   Por ejemplo, en 'B': [{'D': 2}, {'E': 4}] significa que para resolver 'B', debes resolver el sub-problema que lleva a 'D' (costo 2) Y el sub-problema que lleva a 'E' (costo 4).
grafo_ao = {
    'A': {'B': 1, 'C': 3}, # A es un nodo OR. Para resolver A, resuelve B (costo 1) O resuelve C (costo 3).
    'B': [{'D': 2}, {'E': 4}], # B es un nodo AND. Para resolver B, resuelve D (costo 2) AND resuelve E (costo 4).
    'C': {'F': 2},        # C es un nodo OR. Para resolver C, resuelve F (costo 2).
    'D': {},              # D es un nodo terminal resuelto.
    'E': {'F': 1},        # E es un nodo OR. Para resolver E, resuelve F (costo 1).
    'F': {}               # F es el nodo objetivo resuelto.
}

# Llama a la función AO* para encontrar un plan óptimo desde 'A' a 'F' en grafo_ao usando la heurística nula.
# AO* busca un subgrafo de solución que sea el de menor costo total.
camino_ao, costo_ao = ao_star(grafo_ao, 'A', 'F', h_simple)
# Imprime el resultado de AO*. El "camino" para AO* es más bien el conjunto de nodos que componen el plan óptimo.
print(f"AO*: Camino {camino_ao}, Costo {costo_ao}")