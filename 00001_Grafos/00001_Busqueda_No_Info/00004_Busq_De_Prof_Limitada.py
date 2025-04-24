def busqueda_profundidad_limitada(grafo, inicio, objetivo, limite):
    pila = [(inicio, [inicio], 0)]  # (nodo, camino, profundidad)
    visitados = set()

    while pila:
        actual, camino, profundidad = pila.pop()

        if actual == objetivo:
            return camino

        if actual not in visitados and profundidad < limite:
            visitados.add(actual)

            # Añade vecinos a la pila con profundidad aumentada
            for vecino in reversed(grafo[actual]):
                if vecino not in visitados:
                    pila.append((vecino, camino + [vecino], profundidad + 1))

    return None  # No se encontró el objetivo en el límite dado
def dls_recursiva(grafo, nodo, objetivo, limite, visitados=None, camino=None):
    if visitados is None:
        visitados = set()
    if camino is None:
        camino = []

    visitados.add(nodo)
    camino = camino + [nodo]

    if nodo == objetivo:
        return camino

    if limite <= 0:
        return None  # Se alcanza el límite de profundidad

    for vecino in grafo[nodo]:
        if vecino not in visitados:
            resultado = dls_recursiva(grafo, vecino, objetivo, limite - 1, visitados, camino)
            if resultado:
                return resultado

    return None  # Si ningún camino fue válido
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
    limite = 3

    print("Versión iterativa:")
    camino = busqueda_profundidad_limitada(grafo, inicio, objetivo, limite)
    print(" -> ".join(camino) if camino else f"No se encontró camino con límite {limite}")

    print("\nVersión recursiva:")
    camino_rec = dls_recursiva(grafo, inicio, objetivo, limite)
    print(" -> ".join(camino_rec) if camino_rec else f"No se encontró camino con límite {limite}")
