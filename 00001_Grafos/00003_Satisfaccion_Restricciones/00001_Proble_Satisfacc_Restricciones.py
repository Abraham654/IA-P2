import itertools

class CSP:
    def __init__(self, variables, dominios, restricciones):
        self.variables = variables
        self.dominios = dominios
        self.restricciones = restricciones
        # Vecinos conectados directamente por restricciones
        self.vecinos = {v: [u for u in variables if (u, v) in restricciones or (v, u) in restricciones] for v in variables}

    def consistente(self, var, val, asignacion):
        for vecino in self.vecinos[var]:
            if vecino in asignacion:
                par = (val, asignacion[vecino])
                if par not in self.restricciones.get((var, vecino), []) and par not in self.restricciones.get((vecino, var), [(b, a) for (a, b) in self.restricciones.get((var, vecino), [])]):
                    return False
        return True

    def backtracking_search(self, asignacion={}):
        if len(asignacion) == len(self.variables):
            return asignacion

        var = next(v for v in self.variables if v not in asignacion)
        for val in self.dominios[var]:
            if self.consistente(var, val, asignacion):
                asignacion[var] = val
                resultado = self.backtracking_search(asignacion)
                if resultado: return resultado
                del asignacion[var]
        return None

    def ac3(self):
        cola = list(itertools.product(self.variables, repeat=2))
        while cola:
            xi, xj = cola.pop()
            if self.revisar_dominio(xi, xj):
                if not self.dominios[xi]: return False
                for xk in self.vecinos[xi]:
                    if xk != xj:
                        cola.append((xk, xi))
        return True

    def revisar_dominio(self, xi, xj):
        revisado = False
        for x in self.dominios[xi][:]:
            if not any((x, y) in self.restricciones.get((xi, xj), []) for y in self.dominios[xj]):
                self.dominios[xi].remove(x)
                revisado = True
        return revisado

# Ejemplo: Coloreado de mapa de Australia
if __name__ == "__main__":
    variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
    colores = ['rojo', 'verde', 'azul']
    dominios = {v: colores[:] for v in variables}

    restricciones = {}
    adyacentes = [
        ('WA', 'NT'), ('WA', 'SA'), ('NT', 'SA'), ('NT', 'Q'),
        ('SA', 'Q'), ('SA', 'NSW'), ('SA', 'V'), ('Q', 'NSW'), ('NSW', 'V')
    ]
    for (a, b) in adyacentes:
        restricciones[(a, b)] = [(x, y) for x in colores for y in colores if x != y]
        restricciones[(b, a)] = [(y, x) for x, y in restricciones[(a, b)]]  # Asegura simetría

    problema = CSP(variables, dominios, restricciones)
    problema.ac3()
    solucion = problema.backtracking_search()

    if solucion:
        print("Solución encontrada:")
        for region, color in solucion.items():
            print(f"{region}: {color}")
    else:
        print("No se encontró una solución válida.")
