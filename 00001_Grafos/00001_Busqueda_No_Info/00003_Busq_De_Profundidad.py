def busqueda_profundidad(grafo, inicio, objetivo):
    pila = [(inicio, [inicio])]   # Pila: [(nodo actual, camino hasta él)]
    visitados = set()             # Conjunto para evitar ciclos

    while pila:
        actual, camino = pila.pop()  # Tomamos el último nodo insertado

        if actual == objetivo:
            return camino

        if actual not in visitados:
            visitados.add(actual)

            # Agregamos vecinos no visitados (orden inverso para mantener recorrido)
            for vecino in reversed(grafo[actual]):
                if vecino not in visitados:
                    pila.append((vecino, camino + [vecino]))

    return None  # Si no se encuentra camino
def busqueda_profundidad_recursiva(grafo, inicio, objetivo, visitados=None, camino=None):
    if visitados is None:
        visitados = set()
    if camino is None:
        camino = []

    visitados.add(inicio)
    camino = camino + [inicio]

    if inicio == objetivo:
        return camino

    for vecino in grafo[inicio]:
        if vecino not in visitados:
            resultado = busqueda_profundidad_recursiva(grafo, vecino, objetivo, visitados, camino)
            if resultado:
                return resultado

    return None
if __name__ == "__main__":
    grafo = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }

    inicio, objetivo = 'A', 'F'

    print("Versión iterativa:")
    camino = busqueda_profundidad(grafo, inicio, objetivo)
    print(" -> ".join(camino) if camino else "No se encontró camino")

    print("\nVersión recursiva:")
    camino_rec = busqueda_profundidad_recursiva(grafo, inicio, objetivo)
    print(" -> ".join(camino_rec) if camino_rec else "No se encontró camino")
