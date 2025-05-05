class ForwardCheckingCSP:
    def __init__(self, variables, dominios, restricciones):
        # Inicializa variables, copia editable de dominios y restricciones
        self.variables = variables
        self.dominios = {v: list(dominios[v]) for v in variables}
        self.restricciones = restricciones
        self.asignacion = {}

    def es_completa(self):
        # Verifica si todas las variables están asignadas
        return len(self.asignacion) == len(self.variables)

    def es_consistente(self, variable, valor):
        # Verifica que un valor no viole ninguna restricción
        temp_asign = {**self.asignacion, variable: valor}
        for vars_r, funcion in self.restricciones:
            if all(v in temp_asign for v in vars_r):
                if not funcion(**{v: temp_asign[v] for v in vars_r}):
                    return False
        return True

    def forward_check(self, variable, valor):
        # Elimina valores inconsistentes en vecinos (forward checking)
        dominios_temp = {v: list(self.dominios[v]) for v in self.variables}
        for vecino in self.obtener_vecinos(variable):
            if vecino not in self.asignacion:
                for val in list(self.dominios[vecino]):
                    if not self.es_consistente(vecino, val):
                        self.dominios[vecino].remove(val)
                        if not self.dominios[vecino]:
                            return False  # Dominio vacío
        return True

    def obtener_vecinos(self, variable):
        # Devuelve variables relacionadas por restricciones
        vecinos = set()
        for vars_r, _ in self.restricciones:
            if variable in vars_r:
                vecinos.update(v for v in vars_r if v != variable)
        return vecinos

    def seleccionar_variable(self):
        # Heurística MRV: elige variable con menor dominio posible
        no_asignadas = [v for v in self.variables if v not in self.asignacion]
        return min(no_asignadas, key=lambda v: len(self.dominios[v]))

    def resolver(self):
        # Inicia el proceso de backtracking
        return self._backtrack()

    def _backtrack(self):
        if self.es_completa():
            return self.asignacion

        var = self.seleccionar_variable()

        for val in list(self.dominios[var]):
            if self.es_consistente(var, val):
                self.asignacion[var] = val
                dominios_previos = {v: list(self.dominios[v]) for v in self.variables}

                if self.forward_check(var, val):
                    resultado = self._backtrack()
                    if resultado is not None:
                        return resultado

                # Revertir asignación y dominios
                self.asignacion.pop(var)
                self.dominios = dominios_previos

        return None

# --- Ejemplo: Coloreado de mapas ---
if __name__ == "__main__":
    variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
    dominios = {v: ['rojo', 'verde', 'azul'] for v in variables}

    # Comparación entre dos colores
    def diferente_color(**kwargs):
        vals = list(kwargs.values())
        return vals[0] != vals[1]

    restricciones = [
        (('WA', 'NT'), diferente_color),
        (('WA', 'SA'), diferente_color),
        (('NT', 'SA'), diferente_color),
        (('NT', 'Q'), diferente_color),
        (('SA', 'Q'), diferente_color),
        (('SA', 'NSW'), diferente_color),
        (('SA', 'V'), diferente_color),
        (('Q', 'NSW'), diferente_color),
        (('NSW', 'V'), diferente_color)
    ]

    csp = ForwardCheckingCSP(variables, dominios, restricciones)
    solucion = csp.resolver()

    print("Solución encontrada:")
    if solucion:
        for region, color in sorted(solucion.items()):
            print(f"{region}: {color}")
    else:
        print("No se encontró solución.")
