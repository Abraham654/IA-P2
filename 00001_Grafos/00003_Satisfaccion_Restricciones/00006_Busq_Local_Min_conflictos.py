import random

class MinimosConflictos:
    def __init__(self, variables, dominios, restricciones, max_iter=1000):
        # Inicializa variables del problema
        self.variables = variables
        self.dominios = dominios
        self.restricciones = restricciones
        self.max_iter = max_iter
        self.asignacion = self._inicializar_asignacion()

    def _inicializar_asignacion(self):
        # Asignación aleatoria inicial
        return {v: random.choice(self.dominios[v]) for v in self.variables}

    def _contar_conflictos(self, variable, valor):
        # Cuenta cuántas restricciones se violan si 'variable' toma 'valor'
        conflictos = 0
        temp_asign = {**self.asignacion, variable: valor}
        for vars_restr, funcion in self.restricciones:
            if variable in vars_restr and all(v in temp_asign for v in vars_restr):
                valores = [temp_asign[v] for v in vars_restr]
                if not funcion(*valores):
                    conflictos += 1
        return conflictos

    def _elegir_variable_conflictiva(self):
        # Elige una variable que actualmente causa conflictos
        conflictivas = [v for v in self.variables 
                        if self._contar_conflictos(v, self.asignacion[v]) > 0]
        return random.choice(conflictivas) if conflictivas else None

    def _mejor_valor(self, variable):
        # Retorna el valor con menos conflictos para 'variable'
        return min(self.dominios[variable], 
                   key=lambda val: self._contar_conflictos(variable, val))

    def resolver(self):
        # Bucle principal de mínimos conflictos
        for _ in range(self.max_iter):
            var = self._elegir_variable_conflictiva()
            if var is None:
                return self.asignacion  # Sin conflictos → solución
            self.asignacion[var] = self._mejor_valor(var)
        return None  # No se encontró solución

# ---------- Ejemplo: 8 Reinas ----------
if __name__ == "__main__":
    variables = [f'Q{i}' for i in range(1, 9)]
    dominios = {q: list(range(8)) for q in variables}  # Filas 0–7

    # Verifica que dos reinas no se ataquen
    def no_ataque(qi, qj, row_i, row_j):
        return row_i != row_j and abs(qi - qj) != abs(row_i - row_j)

    # Genera restricciones para cada par de reinas
    restricciones = [
        ((f'Q{i+1}', f'Q{j+1}'), 
         lambda ri, rj, i=i, j=j: no_ataque(i, j, ri, rj))
        for i in range(8) for j in range(i + 1, 8)
    ]

    # Ejecuta el algoritmo
    csp = MinimosConflictos(variables, dominios, restricciones, max_iter=10000)
    solucion = csp.resolver()

    if solucion:
        print("Solución encontrada para las 8 reinas:")
        for reina in sorted(solucion):
            print(f"{reina} en fila {solucion[reina] + 1}")  # Mostrar fila 1-8
    else:
        print("No se encontró solución en el número máximo de iteraciones.")
