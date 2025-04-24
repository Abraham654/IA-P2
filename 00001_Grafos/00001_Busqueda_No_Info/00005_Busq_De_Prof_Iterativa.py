def busqueda_profundidad_iterativa(grafo, inicio, objetivo):
    def dls(nodo, objetivo, limite):
        if nodo == objetivo:
            return [nodo]
        if limite == 0:
            return None
        for vecino in grafo[nodo]:
            resultado = dls(vecino, objetivo, limite - 1)
            if resultado:
                return [nodo] + resultado
        return None

    profundidad = 0  # Límite inicial
    while True:
        resultado = dls(inicio, objetivo, profundidad)  # DFS limitada
        if resultado:
            return resultado
        profundidad += 1  # Aumenta el límite para intentar más profundo

def iddfs_completo(grafo, inicio, objetivo):
    profundidad = 0
    while True:
        visitados = set()
        pila = [(inicio, [inicio], 0)]  # (nodo, camino actual, nivel)
        encontrado = None

        while pila:
            nodo, camino, nivel = pila.pop()
            if nodo == objetivo:
                encontrado = camino
                break
            if nivel < profundidad and nodo not in visitados:
                visitados.add(nodo)
                for vecino in reversed(grafo[nodo]):
                    if vecino not in visitados:
                        pila.append((vecino, camino + [vecino], nivel + 1))

        if encontrado:
            return encontrado
        if not pila:
            break  # No quedan caminos por explorar
        profundidad += 1

    return None

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

    inicio, objetivo = 'A', 'F'

    print("Versión básica:")
    camino = busqueda_profundidad_iterativa(grafo, inicio, objetivo)
    print(" -> ".join(camino) if camino else "Camino no encontrado")

    print("\nVersión completa con seguimiento de visitados:")
    camino_completo = iddfs_completo(grafo, inicio, objetivo)
    print(" -> ".join(camino_completo) if camino_completo else "Camino no encontrado")
