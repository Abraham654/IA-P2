class ConflictDirectedBackjumping:
    def __init__(self, variables, dominios, restricciones):
        self.variables = variables
        self.dominios = dominios
        self.restricciones = restricciones
        self.asignacion = {}
        self.conflict_set = {v: set() for v in variables}

    def obtener_vecinos(self, variable):
        vecinos = set()
        for vars_restr, _ in self.restricciones:
            if variable in vars_restr:
                vecinos.update(v for v in vars_restr if v != variable)
        return vecinos

    def es_consistente(self, variable, valor):
        temp_asign = {**self.asignacion, variable: valor}
        for vars_restr, funcion in self.restricciones:
            if all(v in temp_asign for v in vars_restr):
                valores = [temp_asign[v] for v in vars_restr]
                if not funcion(*valores):
                    return False
        return True

    def resolver(self):
        return self._backjump(0)

    def _backjump(self, nivel):
        if len(self.asignacion) == len(self.variables):
            return self.asignacion

        variable = self.variables[nivel]

        for valor in self.dominios[variable]:
            if self.es_consistente(variable, valor):
                self.asignacion[variable] = valor
                resultado = self._backjump(nivel + 1)
                if resultado:
                    return resultado
                del self.asignacion[variable]
            else:
                for v in self.asignacion:
                    self.conflict_set[variable].add(v)

        if nivel > 0:
            salto = max(self.conflict_set[variable]) if self.conflict_set[variable] else nivel - 1
            for v in self.variables[salto + 1:]:
                if v in self.asignacion:
                    del self.asignacion[v]
                self.conflict_set[v].update(self.conflict_set[variable])
            return self._backjump(salto)

        return None

# ---------- Ejemplo: Problema de las 8 reinas ----------
if __name__ == "__main__":
    variables = [f'Q{i}' for i in range(1, 9)]
    dominios = {q: list(range(1, 9)) for q in variables}

    # Solo usamos los valores (no los nombres de las variables)
    def no_ataque(qi, qj):
        i = qi
        j = qj
        pos_i = int(i)
        pos_j = int(j)
        return qi != qj and abs(pos_i - pos_j) != abs(i - j)

    # Usar valores posicionales en la restricción
    restricciones = [
        ((f'Q{i}', f'Q{j}'), lambda qi, qj: qi != qj and abs(i - j) != abs(qi - qj))
        for i in range(1, 9) for j in range(i + 1, 9)
    ]

    csp = ConflictDirectedBackjumping(variables, dominios, restricciones)
    solucion = csp.resolver()

    print("Solución para el problema de las 8 reinas:")
    for reina in sorted(solucion):
        print(f"{reina} en fila {solucion[reina]}")
