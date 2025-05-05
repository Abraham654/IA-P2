class BacktrackingCSP:
    def __init__(self, variables, dominios, restricciones):
        # variables: nombres del problema
        # dominios: posibles valores por variable
        # restricciones: lista de (tupla_variables, funcion_restriccion)
        self.variables = variables
        self.dominios = dominios
        self.restricciones = restricciones
        self.asignacion = {}

    def es_completa(self):
        # ¿Todas las variables ya están asignadas?
        return len(self.asignacion) == len(self.variables)

    def es_consistente(self, variable, valor):
        # Evalúa si la asignación es válida con las restricciones
        for vars_restr, funcion in self.restricciones:
            if variable in vars_restr:
                temp_asign = {**self.asignacion, variable: valor}
                if all(v in temp_asign for v in vars_restr):
                    # Extrae los argumentos por nombre y evalúa la restricción
                    args = [temp_asign[v] for v in vars_restr]
                    if not funcion(*args):
                        return False
        return True

    def seleccionar_variable_no_asignada(self):
        # Usa heurística MRV: menor dominio restante
        no_asignadas = [v for v in self.variables if v not in self.asignacion]
        return min(no_asignadas, key=lambda v: len(self.dominios[v]))

    def ordenar_valores(self, variable):
        # Ordena valores que menos fallan (heurística de menor restricción)
        return sorted(self.dominios[variable],
            key=lambda val: sum(
                not self.es_consistente(variable, val)
                for vars_r, _ in self.restricciones if variable in vars_r))

    def resolver(self):
        # Inicia el backtracking
        return self._backtrack()

    def _backtrack(self):
        # Algoritmo recursivo principal
        if self.es_completa():
            return self.asignacion

        variable = self.seleccionar_variable_no_asignada()

        for valor in self.ordenar_valores(variable):
            if self.es_consistente(variable, valor):
                self.asignacion[variable] = valor
                resultado = self._backtrack()
                if resultado:
                    return resultado
                del self.asignacion[variable]

        return None

# === Ejemplo: problema de las 4 reinas ===
if __name__ == "__main__":
    variables = ['Q1', 'Q2', 'Q3', 'Q4']
    dominios = {q: [1, 2, 3, 4] for q in variables}  # filas posibles

    # Restricción: sin ataques entre reinas
    def no_ataque(f1, f2, c1, c2):
        return f1 != f2 and abs(f1 - f2) != abs(c1 - c2)

    restricciones = [
        ((f'Q{i}', f'Q{j}'), lambda f1, f2, i=i, j=j: no_ataque(f1, f2, i, j))
        for i in range(1, 5) for j in range(i + 1, 5)
    ]

    csp = BacktrackingCSP(variables, dominios, restricciones)
    solucion = csp.resolver()

    if solucion:
        print("Solución para el problema de las 4 reinas:")
        for reina in sorted(solucion):
            print(f"{reina} en fila {solucion[reina]}")
    else:
        print("No se encontró solución.")
