import heapq  # Importa la librería 'heapq', que proporciona una implementación del algoritmo de cola de prioridad (heap).

# Define la función principal que implementa el algoritmo de Búsqueda de Costo Uniforme.
# Recibe tres argumentos:
# - grafo: Un diccionario que representa el grafo. Las claves son los nodos.
#          Los valores son listas de tuplas (vecino, costo_del_paso).
# - inicio: El nodo desde el cual comenzar la búsqueda.
# - objetivo: El nodo que se desea encontrar.
def busqueda_costo_uniforme(grafo, inicio, objetivo):
    # Inicializa la cola de prioridad. En UCS, esta cola almacena tuplas (costo_acumulado, nodo).
    # heapq siempre mantiene el elemento con el menor costo (el primer elemento de la tupla) en la parte superior.
    cola = []  # Cola de prioridad: (costo acumulado, nodo)

    # Añade el nodo inicial a la cola de prioridad. El costo acumulado al inicio es 0.
    # heapq.heappush(cola, item) inserta un item en el heap (la lista 'cola').
    heapq.heappush(cola, (0, inicio))

    # Inicializa un diccionario para rastrear los nodos visitados y la información relevante para reconstruir el camino y comparar costos.
    # La clave es el nodo visitado. El valor es una tupla (predecesor, costo_acumulado_para_llegar_a_este_nodo).
    # El nodo inicial se marca con un predecesor None y un costo acumulado de 0.
    visitados = {inicio: (None, 0)} # Registro de nodos visitados: nodo → (predecesor, costo acumulado)

    # Inicia el bucle principal del algoritmo. Continúa mientras haya nodos en la cola de prioridad.
    while cola:
        # Extrae el nodo con el menor costo acumulado de la cola de prioridad.
        # heapq.heappop(cola) extrae y devuelve el elemento más pequeño del heap (en este caso, la tupla con el menor primer elemento).
        costo, actual = heapq.heappop(cola)  # Extrae nodo con menor costo

        # Comprueba si el nodo actual extraído es el objetivo que estamos buscando.
        if actual == objetivo:
            # Si el nodo actual es el objetivo, hemos encontrado el camino de menor costo.
            # Inicializamos una lista vacía para almacenar el camino.
            camino = []
            # Iniciamos un bucle para reconstruir el camino hacia atrás desde el objetivo hasta el inicio
            # usando el diccionario 'visitados'.
            while actual: # El bucle continúa mientras 'actual' no sea None (llegamos al nodo inicial).
                # Añade el nodo actual al principio del camino (o al final temporalmente).
                camino.append(actual)
                # Se mueve al nodo padre (predecesor) del nodo actual, que está almacenado como el primer elemento
                # de la tupla en visitados[actual].
                actual = visitados[actual][0]
            # Retorna una tupla que contiene el costo total del camino (que es el 'costo' al extraer el objetivo)
            # y el camino invertido (para que vaya de inicio a objetivo) usando slicing [::-1].
            return (costo, camino[::-1])  # Retorna el costo total y el camino de inicio a objetivo

        # Si el nodo actual no es el objetivo, exploramos sus vecinos para encontrar nuevos caminos.
        # Itera sobre cada vecino del nodo 'actual' y el costo del paso para llegar a ese vecino, según la definición del 'grafo'.
        for vecino, paso in grafo[actual]:
            # Calcula el nuevo costo acumulado para llegar al vecino a través del nodo actual.
            nuevo_costo = costo + paso

            # Implementa la lógica clave de UCS y Dijkstra:
            # Solo consideramos este nuevo camino al vecino si:
            # 1. El vecino no ha sido visitado antes, O
            # 2. El vecino ya fue visitado, pero este nuevo camino ofrece un costo acumulado menor que el que teníamos registrado anteriormente.
            if vecino not in visitados or nuevo_costo < visitados[vecino][1]:
                # Si la condición anterior se cumple:
                # Actualiza la información del vecino en el diccionario 'visitados' con el nodo actual como su predecesor
                # y el 'nuevo_costo' como su costo acumulado.
                visitados[vecino] = (actual, nuevo_costo)
                # Añade el vecino a la cola de prioridad con su 'nuevo_costo' acumulado.
                # heapq se encargará de mantener la cola ordenada por este costo.
                heapq.heappush(cola, (nuevo_costo, vecino))

    # Si el bucle 'while cola:' termina y no se ha encontrado el objetivo (nunca se ejecutó el 'return'),
    # significa que el objetivo no es alcanzable desde el nodo de inicio.
    return None  # No se encontró camino

# Este bloque de código solo se ejecuta cuando el script se corre directamente (no cuando es importado como módulo).
# Es una práctica común para incluir ejemplos de uso o pruebas.
if __name__ == "__main__":
    # Define la estructura del grafo con costos asociados a las aristas.
    # Las claves son los nodos y los valores son listas de tuplas (vecino, costo).
    grafo = {
        'A': [('B', 1), ('C', 4)], # De A a B cuesta 1, de A a C cuesta 4.
        'B': [('A', 1), ('D', 5), ('E', 2)], # De B a A cuesta 1, etc.
        'C': [('A', 4), ('F', 3)],
        'D': [('B', 5)],
        'E': [('B', 2), ('F', 1)],
        'F': [('C', 3), ('E', 1)]
    }

    # Define el nodo de inicio y el nodo objetivo.
    inicio, objetivo = 'A', 'F'
    # Llama a la función de búsqueda de costo uniforme con el grafo, inicio y objetivo definidos.
    # El resultado (una tupla con costo y camino, o None) se guarda en 'resultado'.
    resultado = busqueda_costo_uniforme(grafo, inicio, objetivo)

    # Comprueba si se encontró un resultado (si 'resultado' no es None).
    if resultado:
        # Si se encontró, desempaqueta la tupla 'resultado' en 'costo' y 'camino'.
        costo, camino = resultado
        # Imprime el camino encontrado y su costo total, formateando la salida.
        print(f"Camino encontrado (costo total: {costo}):", " -> ".join(camino))
    else:
        # Si 'resultado' es None (no se encontró el camino), imprime un mensaje indicándolo.
        print(f"No se encontró camino desde {inicio} hasta {objetivo}")