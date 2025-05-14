# Define una clase para representar un CSP y resolverlo usando Búsqueda con Retroceso.
# Esta implementación permite definir restricciones como funciones y utiliza heurísticas para la selección de variables y el ordenamiento de valores.
class BacktrackingCSP:
    # Método constructor de la clase.
    # Recibe:
    # - variables: Una lista de los nombres de las variables del problema (ej: ['Q1', 'Q2', 'Q3', 'Q4']).
    # - dominios: Un diccionario donde las claves son los nombres de las variables y los valores son listas de los posibles valores que cada variable puede tomar (ej: {'Q1': [1, 2, 3, 4], ...}).
    # - restricciones: Una lista de tuplas, donde cada tupla contiene:
    #   1. Una tupla de variables involucradas en la restricción (ej: ('Q1', 'Q2')).
    #   2. Una función de restricción que toma los valores asignados a esas variables como argumentos y retorna True si la restricción se cumple, False si se viola.
    def __init__(self, variables, dominios, restricciones):
        # variables: nombres del problema (ej: 'WA', 'Q1', etc.)
        self.variables = variables # Almacena la lista de variables.
        # dominios: posibles valores por variable (ej: ['rojo', 'verde'], [1, 2, 3])
        self.dominios = dominios # Almacena el diccionario de dominios.
        # restricciones: lista de (tupla_variables, funcion_restriccion)
        self.restricciones = restricciones # Almacena la lista de restricciones.

        # Diccionario para almacenar la asignación parcial actual durante la búsqueda.
        # La clave es el nombre de la variable, el valor es el valor asignado. Inicialmente vacío.
        self.asignacion = {}

    # Método auxiliar para verificar si la asignación actual está completa.
    # La asignación es completa si se ha asignado un valor a cada variable.
    def es_completa(self):
        # ¿Todas las variables ya están asignadas?
        # Compara el número de variables en el diccionario de asignación con el número total de variables.
        return len(self.asignacion) == len(self.variables)

    # Método para verificar si la asignación tentativa (variable = valor) es consistente con la asignación parcial actual.
    # Una asignación es consistente si no viola ninguna de las restricciones relevantes DADA la asignación parcial actual más la nueva asignación.
    # Recibe: la variable a asignar y el valor a probar.
    def es_consistente(self, variable, valor):
        # Evalúa si la asignación es válida con las restricciones
        # Itera sobre todas las restricciones definidas en el CSP.
        for vars_restr, funcion in self.restricciones:
            # Comprueba si la variable que estamos intentando asignar (variable) es una de las variables involucradas en la restricción actual (vars_restr).
            if variable in vars_restr:
                # Crea una copia temporal de la asignación actual y añade la asignación tentativa (variable: valor).
                # {**self.asignacion, variable: valor} es una forma de crear un nuevo diccionario con el contenido de self.asignacion y sobrescribir o añadir 'variable: valor'.
                temp_asign = {**self.asignacion, variable: valor}

                # Comprueba si todas las variables involucradas en esta restricción (vars_restr) ya tienen un valor asignado en la asignación temporal.
                # Esto es necesario para poder evaluar la función de restricción.
                if all(v in temp_asign for v in vars_restr):
                    # Si todas las variables de la restricción están asignadas:
                    # Extrae los valores asignados a las variables de la restricción de la asignación temporal,
                    # en el mismo orden en que aparecen en la tupla vars_restr.
                    # Extrae los argumentos por nombre y evalúa la restricción
                    args = [temp_asign[v] for v in vars_restr]
                    # Llama a la función de restricción con los valores extraídos (*args desempaqueta la lista 'args' como argumentos individuales).
                    # Si la función retorna False, significa que la restricción se viola.
                    if not funcion(*args):
                        # Si la restricción se viola, la asignación tentativa no es consistente.
                        return False
        # Si se verifican todas las restricciones relevantes y ninguna se viola, la asignación tentativa es consistente.
        return True

    # Método para seleccionar la próxima variable no asignada utilizando la heurística MRV (Minimum Remaining Values).
    # MRV selecciona la variable que tiene el menor número de valores restantes en su dominio.
    # Esto ayuda a detectar fallos antes en el árbol de búsqueda.
    def seleccionar_variable_no_asignada(self):
        # Usa heurística MRV: menor dominio restante
        # Crea una lista de variables que aún no están en la asignación.
        no_asignadas = [v for v in self.variables if v not in self.asignacion]
        # Usa la función 'min' en la lista de variables no asignadas.
        # La clave (key) para la comparación es una función lambda que retorna la longitud del dominio de cada variable 'v'.
        # 'min' encontrará la variable 'v' con el menor valor retornado por esta clave (el menor dominio).
        return min(no_asignadas, key=lambda v: len(self.dominios[v]))

    # Método para ordenar los valores en el dominio de una variable seleccionada.
    # Utiliza una heurística (similar a Least Constraining Value - LCV) para probar primero los valores
    # que menos restringen las opciones para las variables no asignadas.
    def ordenar_valores(self, variable):
        # Ordena valores que menos fallan (heurística de menor restricción)
        # Ordena la lista de valores en el dominio de la variable.
        # La clave (key) para la ordenación es una función lambda que evalúa un "costo" para cada valor 'val'.
        # El costo es la suma de las veces que la asignación de este 'val' a 'variable' *no* es consistente
        # con alguna restricción que involucra a 'variable' y que puede ser evaluada con la asignación actual.
        # `sum(not self.es_consistente(variable, val) for vars_r, _ in self.restricciones if variable in vars_r)`
        # Para cada valor 'val', itera sobre todas las restricciones. Si la restricción involucra a 'variable',
        # verifica si 'es_consistente' retorna False para (variable, val) dada la asignación actual.
        # Suma 1 por cada restricción que sería violada *basado en la asignación actual*.
        # Ordenar por este suma minimiza el número de conflictos inmediatos con la asignación parcial.
        # (Nota: La heurística LCV estándar mide el impacto en los dominios de los vecinos no asignados, esta es una variación).
        return sorted(self.dominios[variable],
            key=lambda val: sum(
                not self.es_consistente(variable, val) # Cuenta si la asignación (variable=val) NO es consistente
                for vars_r, _ in self.restricciones if variable in vars_r)) # Para cada restricción que involucra a 'variable'

    # Método de entrada para iniciar el proceso de resolución.
    def resolver(self):
        # Inicia el backtracking llamando al método recursivo principal.
        return self._backtrack()

    # Método recursivo privado que implementa la lógica principal del backtracking.
    def _backtrack(self):
        # Algoritmo recursivo principal
        # --- Caso Base ---
        # Si la asignación actual está completa, hemos encontrado una solución.
        if self.es_completa():
            # Retorna la asignación completa.
            return self.asignacion

        # --- Selección de Variable ---
        # Selecciona la próxima variable no asignada utilizando la heurística MRV.
        variable = self.seleccionar_variable_no_asignada()

        # --- Iteración sobre Valores (Ordenados) ---
        # Itera sobre los valores en el dominio de la variable seleccionada, ordenados por la heurística de ordenamiento de valores.
        for valor in self.ordenar_valores(variable):
            # --- Verificación de Consistencia (Forward Checking implícito en es_consistente) ---
            # Comprueba si asignar este 'valor' a 'variable' es consistente con la asignación actual.
            if self.es_consistente(variable, valor):
                # Si es consistente:
                # Realiza la asignación: añade la variable y su valor a la asignación parcial.
                self.asignacion[variable] = valor
                # --- Llamada Recursiva ---
                # Realiza una llamada recursiva para intentar completar la asignación.
                resultado = self._backtrack()
                # Si la llamada recursiva retorna un resultado (encontró una solución).
                if resultado:
                    # Propaga la solución hacia arriba en la cadena de llamadas.
                    return resultado
                # --- Retroceso (Backtracking) ---
                # Si la llamada recursiva no encontró una solución en esta rama (retornó None),
                # deshace la última asignación (elimina la variable de la asignación parcial).
                del self.asignacion[variable]

        # Si el bucle sobre los valores termina y ninguno llevó a una solución (todas las ramas fallaron),
        # retorna None, indicando que no hay solución posible desde este estado de asignación parcial.
        return None

# === Ejemplo: problema de las 4 reinas ===
# El problema de las N reinas consiste en colocar N reinas en un tablero de ajedrez N×N
# de modo que ninguna reina ataque a otra (no compartan fila, columna ni diagonal).
# Lo modelamos como un CSP:
# Variables: Cada reina Q_i es una variable.
# Dominio: Para una reina en la columna i, el dominio son las posibles filas (1 a N) donde puede estar.
# Restricciones: Para cada par de reinas, no pueden estar en la misma fila ni en la misma diagonal.
if __name__ == "__main__":
    # Define las variables del CSP: las 4 reinas. Asumimos que están en columnas 1, 2, 3, 4.
    variables = ['Q1', 'Q2', 'Q3', 'Q4']

    # Define el dominio para cada variable: cada reina puede estar en cualquiera de las 4 filas.
    dominios = {q: [1, 2, 3, 4] for q in variables} # filas posibles (los valores)

    # Define la función de restricción: comprueba si dos reinas se atacan.
    # Recibe las filas (f1, f2) y columnas (c1, c2) de las dos reinas.
    def no_ataque(f1, f2, c1, c2):
        # Retorna True si NO se atacan:
        # - No están en la misma fila (f1 != f2) AND
        # - No están en la misma diagonal (|f1 - f2| != |c1 - c2|).
        return f1 != f2 and abs(f1 - f2) != abs(c1 - c2)

    # Define la lista de restricciones. Hay una restricción por cada par único de reinas.
    # Genera pares de índices (i, j) para las reinas (de 1 a 4, con i < j para evitar duplicados).
    restricciones = [
        # Para cada par de índices (i, j), crea una tupla:
        # 1. La tupla de variables involucradas: (nombre de la reina i, nombre de la reina j).
        # 2. La función de restricción: una función lambda que toma las filas (f1, f2) asignadas a Q_i y Q_j
        #    y llama a 'no_ataque', pasando las filas y las columnas fijas (i, j).
        #    Los 'i=i, j=j' en la lambda son cruciales para capturar los valores correctos de i y j en cada iteración.
        ((f'Q{i}', f'Q{j}'), lambda f1, f2, i=i, j=j: no_ataque(f1, f2, i, j))
        for i in range(1, 5) for j in range(i + 1, 5) # Genera pares únicos (i, j) con i < j
    ]

    # Crea una instancia del problema CSP para las 4 reinas con las variables, dominios y restricciones definidos.
    csp = BacktrackingCSP(variables, dominios, restricciones)

    # Llama al método 'resolver' para iniciar la búsqueda con retroceso y encontrar una solución.
    solucion = csp.resolver()

    # Comprueba si se encontró una solución (si 'solucion' no es None).
    if solucion:
        # Si se encontró una solución, imprime un encabezado.
        print("Solución para el problema de las 4 reinas:")
        # Imprime la asignación de fila para cada reina, ordenando por el nombre de la reina.
        for reina in sorted(solucion):
            print(f"{reina} en fila {solucion[reina]}")
    else:
        # Si no se encontró solución (el método resolver retornó None), imprime un mensaje.
        print("No se encontró solución.")