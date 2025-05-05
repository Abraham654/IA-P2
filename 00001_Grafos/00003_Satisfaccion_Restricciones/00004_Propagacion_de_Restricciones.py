from collections import deque

class ConstraintPropagationCSP:
    def __init__(self, variables, dominios, restricciones):
        # Inicializa variables, copia de dominios y restricciones bidireccionales
        self.variables = variables
        self.dominios = {v: list(dominios[v]) for v in variables}
        self.restricciones = self._hacer_bidireccionales(restricciones)
        self.arcos = self._construir_arcos()

    def _hacer_bidireccionales(self, restricciones):
        # Duplica restricciones en ambas direcciones
        bidireccionales = {}
        for (a, b), func in restricciones.items():
            bidireccionales[(a, b)] = func
            bidireccionales[(b, a)] = lambda x, y: func(y, x)
        return bidireccionales

    def _construir_arcos(self):
        # Genera lista de todos los arcos (xi, xj)
        return deque((xi, xj) for xi, xj in self.restricciones)

    def _revisar(self, xi, xj):
        # Revisa y elimina valores en xi que no satisfacen la restricción con xj
        revisado = False
        for x in list(self.dominios[xi]):
            if not any(self.restricciones[(xi, xj)](x, y) for y in self.dominios[xj]):
                self.dominios[xi].remove(x)
                revisado = True
        return revisado

    def ac3(self):
        # Algoritmo AC-3: mantiene consistencia entre arcos
        cola = deque(self.arcos)
        while cola:
            xi, xj = cola.popleft()
            if self._revisar(xi, xj):
                if not self.dominios[xi]:
                    return False  # No hay solución
                for xk in self._vecinos(xi):
                    if xk != xj:
                        cola.append((xk, xi))
        return True

    def _vecinos(self, variable):
        # Devuelve vecinos conectados por restricciones
        return {xj for (xi, xj) in self.restricciones if xi == variable}

    def resolver(self):
        # Aplica AC-3 y luego backtracking si es necesario
        if not self.ac3():
            return None
        return self._backtrack({})

    def _backtrack(self, asignacion):
        # Algoritmo de búsqueda con backtracking
        if len(asignacion) == len(self.variables):
            return asignacion
        var = self._seleccionar_variable(asignacion)
        for val in self.dominios[var]:
            if self._es_consistente(var, val, asignacion):
                asignacion[var] = val
                resultado = self._backtrack(asignacion)
                if resultado:
                    return resultado
                del asignacion[var]
        return None

    def _seleccionar_variable(self, asignacion):
        # Selecciona variable no asignada con menor dominio (MRV)
        no_asignadas = [v for v in self.variables if v not in asignacion]
        return min(no_asignadas, key=lambda v: len(self.dominios[v]))

    def _es_consistente(self, var, val, asignacion):
        # Revisa si val para var es consistente con la asignación actual
        for (vi, vj), restr in self.restricciones.items():
            if var == vi and vj in asignacion:
                if not restr(val, asignacion[vj]):
                    return False
            elif var == vj and vi in asignacion:
                if not restr(asignacion[vi], val):
                    return False
        return True

# ---------- Ejemplo: Coloreado de mapas ----------
if __name__ == "__main__":
    variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
    colores = ['rojo', 'verde', 'azul']
    dominios = {v: list(colores) for v in variables}

    def diferente_color(c1, c2):
        return c1 != c2

    restricciones = {
        ('WA', 'NT'): diferente_color,
        ('WA', 'SA'): diferente_color,
        ('NT', 'SA'): diferente_color,
        ('NT', 'Q'): diferente_color,
        ('SA', 'Q'): diferente_color,
        ('SA', 'NSW'): diferente_color,
        ('SA', 'V'): diferente_color,
        ('Q', 'NSW'): diferente_color,
        ('NSW', 'V'): diferente_color
    }

    csp = ConstraintPropagationCSP(variables, dominios, restricciones)
    solucion = csp.resolver()

    print("Solución encontrada:")
    if solucion:
        for region, color in solucion.items():
            print(f"{region}: {color}")
    else:
        print("No se encontró solución.")
