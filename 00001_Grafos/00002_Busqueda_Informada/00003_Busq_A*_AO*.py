def ao_star(grafo, inicio, objetivo, heuristica):
    solucion = {}          # Guarda (costo, camino) por nodo
    expandido = set()      # Nodos ya explorados

    def costo(nodo):
        if nodo in solucion:
            return solucion[nodo][0]  # Si ya se calculó, se reutiliza

        if nodo in grafo:
            if isinstance(grafo[nodo], dict):  # Nodo OR: escoger la mejor opción
                mejor_costo = float('inf')
                mejor_camino = None
                for hijo, c_arco in grafo[nodo].items():
                    c_total = c_arco + costo(hijo)
                    if c_total < mejor_costo:
                        mejor_costo = c_total
                        mejor_camino = [nodo] + solucion[hijo][1]
                solucion[nodo] = (mejor_costo, mejor_camino)
                return mejor_costo

            else:  # Nodo AND: se deben considerar todos los subconjuntos
                c_total = 0
                camino_total = [nodo]
                for conjunto in grafo[nodo]:
                    mejor = float('inf')
                    camino_mejor = []
                    for subnodo in conjunto:
                        temp = conjunto[subnodo] + costo(subnodo)
                        if temp < mejor:
                            mejor = temp
                            camino_mejor = solucion[subnodo][1]
                    c_total += mejor
                    camino_total += camino_mejor
                solucion[nodo] = (c_total, camino_total)
                return c_total

        # Nodo hoja: si es el objetivo, costo 0; si no, no viable
        if nodo == objetivo:
            solucion[nodo] = (0, [nodo])
            return 0
        solucion[nodo] = (float('inf'), None)
        return float('inf')

    solucion[objetivo] = (0, [objetivo])  # Se parte del objetivo

    while inicio not in solucion or solucion[inicio][0] == float('inf'):
        nodo = inicio
        while True:
            if nodo not in expandido:
                break
            if nodo not in solucion or not solucion[nodo][1]:
                return None, None
            camino = solucion[nodo][1]
            nodo = camino[1] if len(camino) > 1 else None
            if nodo is None:
                return None, None

        expandido.add(nodo)
        costo(nodo)  # Recalcula costos

    return solucion[inicio][1], solucion[inicio][0]  # Camino y costo total
