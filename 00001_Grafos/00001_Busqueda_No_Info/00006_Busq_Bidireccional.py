from collections import deque  # Cola eficiente para recorrido BFS

def busqueda_bidireccional(grafo, inicio, objetivo):
    if inicio == objetivo:
        return [inicio]  # Caso trivial

    # Inicializa colas y visitados para ambas direcciones
    cola_inicio = deque([inicio])
    visitado_inicio = {inicio: None}
    cola_objetivo = deque([objetivo])
    visitado_objetivo = {objetivo: None}
    nodo_interseccion = None

    while cola_inicio and cola_objetivo:
        # Expandir desde el inicio
        actual_i = cola_inicio.popleft()
        if actual_i in visitado_objetivo:
            nodo_interseccion = actual_i
            break
        for vecino in grafo[actual_i]:
            if vecino not in visitado_inicio:
                visitado_inicio[vecino] = actual_i
                cola_inicio.append(vecino)

        # Expandir desde el objetivo
        actual_o = cola_objetivo.popleft()
        if actual_o in visitado_inicio:
            nodo_interseccion = actual_o
            break
        for vecino in grafo[actual_o]:
            if vecino not in visitado_objetivo:
                visitado_objetivo[vecino] = actual_o
                cola_objetivo.append(vecino)

    if nodo_interseccion:
        # Reconstrucción desde inicio a intersección
        camino = []
        nodo = nodo_interseccion
        while nodo is not None:
            camino.append(nodo)
            nodo = visitado_inicio[nodo]
        camino.reverse()  # Orden correcto: inicio → intersección

        # Completar desde intersección a objetivo (sin repetir nodo_interseccion)
        nodo = visitado_objetivo[nodo_interseccion]
        while nodo is not None:
            camino.append(nodo)
            nodo = visitado_objetivo[nodo]

        return camino

    return None  # Si no hay conexión entre los nodos

# Ejemplo de uso
if __name__ == "__main__":
    grafo = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }

    inicio = 'A'
    objetivo = 'F'
    camino = busqueda_bidireccional(grafo, inicio, objetivo)
    print(f"Camino encontrado: {camino}" if camino else "No se encontró camino")
