import heapq  # Para usar cola de prioridad

def busqueda_costo_uniforme(grafo, inicio, objetivo):
    cola = []  # Cola de prioridad: (costo acumulado, nodo)
    heapq.heappush(cola, (0, inicio))

    # Registro de nodos visitados: nodo → (predecesor, costo acumulado)
    visitados = {inicio: (None, 0)}

    while cola:
        costo, actual = heapq.heappop(cola)  # Extrae nodo con menor costo

        if actual == objetivo:
            camino = []
            while actual:
                camino.append(actual)
                actual = visitados[actual][0]
            return (costo, camino[::-1])  # Camino de inicio a objetivo

        for vecino, paso in grafo[actual]:
            nuevo_costo = costo + paso
            # Solo se actualiza si es un camino nuevo o más barato
            if vecino not in visitados or nuevo_costo < visitados[vecino][1]:
                visitados[vecino] = (actual, nuevo_costo)
                heapq.heappush(cola, (nuevo_costo, vecino))

    return None  # No se encontró camino

# Ejemplo de uso
if __name__ == "__main__":
    grafo = {
        'A': [('B', 1), ('C', 4)],
        'B': [('A', 1), ('D', 5), ('E', 2)],
        'C': [('A', 4), ('F', 3)],
        'D': [('B', 5)],
        'E': [('B', 2), ('F', 1)],
        'F': [('C', 3), ('E', 1)]
    }

    inicio, objetivo = 'A', 'F'
    resultado = busqueda_costo_uniforme(grafo, inicio, objetivo)

    if resultado:
        costo, camino = resultado
        print(f"Camino encontrado (costo total: {costo}):", " -> ".join(camino))
    else:
        print(f"No se encontró camino desde {inicio} hasta {objetivo}")
