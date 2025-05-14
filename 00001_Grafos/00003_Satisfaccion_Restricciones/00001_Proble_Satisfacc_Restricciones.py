import itertools # Importa la librería 'itertools', que proporciona herramientas para trabajar con iteradores. Se usa aquí para generar combinaciones de variables (arcos) para el algoritmo AC-3.

# Define una clase para representar un Problema de Satisfacción de Restricciones (CSP - Constraint Satisfaction Problem).
# Un CSP consta de un conjunto de variables, cada una con un dominio de posibles valores, y un conjunto de restricciones
# que especifican qué combinaciones de valores para subconjuntos de variables son permitidas.
class CSP:
    # Método constructor de la clase.
    # Recibe:
    # - variables: Una lista de todas las variables en el CSP.
    # - dominios: Un diccionario donde las claves son las variables y los valores son listas de sus dominios (posibles valores).
    # - restricciones: Un diccionario que define las restricciones entre pares de variables. La clave es una tupla (variable1, variable2), y el valor es una lista de tuplas (valor1, valor2) que son las combinaciones *permitidas* para ese par de variables.
    def __init__(self, variables, dominios, restricciones):
        self.variables = variables # Almacena la lista de variables.
        self.dominios = dominios # Almacena el diccionario de dominios.
        self.restricciones = restricciones # Almacena el diccionario de restricciones permitidas.

        # Pre-calcula los vecinos para cada variable. Los vecinos son otras variables que están directamente conectadas por al menos una restricción.
        # Esto facilita encontrar rápidamente las variables relevantes al verificar la consistencia.
        # Para cada variable 'v', crea una lista de variables 'u' si existe una restricción entre 'u' y 'v' en cualquier dirección.
        self.vecinos = {v: [u for u in variables if (u, v) in restricciones or (v, u) in restricciones] for v in variables}

    # Método para verificar si asignar un 'val' a una 'var' es consistente con la 'asignacion' parcial actual.
    # Una asignación es consistente si no viola ninguna restricción con las variables que ya están asignadas.
    # Recibe:
    # - var: La variable a la que se está intentando asignar un valor.
    # - val: El valor que se está intentando asignar a 'var'.
    # - asignacion: Un diccionario que representa la asignación parcial actual (variables ya asignadas y sus valores).
    def consistente(self, var, val, asignacion):
        # Itera sobre los vecinos de la variable 'var'.
        for vecino in self.vecinos[var]:
            # Si el vecino ya está asignado en la asignación parcial.
            if vecino in asignacion:
                # Crea el par de valores (valor de la variable actual, valor del vecino asignado).
                par = (val, asignacion[vecino])
                # --- Verificación de Restricción ---
                # Comprueba si este par de valores viola la restricción entre 'var' y 'vecino'.
                # La restricción está definida por la lista de pares *permitidos*.
                # Si el par (val, asignacion[vecino]) NO está en la lista de restricciones permitidas para (var, vecino)
                # Y (para asegurar la simetría si no todas las restricciones están explícitas en ambos sentidos)
                # si el par reverso (asignacion[vecino], val) NO está en la lista de restricciones permitidas para (vecino, var)
                # (la segunda parte con get y list comprehension es para manejar casos donde la restricción (vecino, var) no está explícitamente definida pero la de (var, vecino) sí, asumiendo simetría).
                # Si la condición es verdadera, significa que el par *no está permitido* y viola la restricción.
                if par not in self.restricciones.get((var, vecino), []) and par not in self.restricciones.get((vecino, var), [(b, a) for (a, b) in self.restricciones.get((var, vecino), [])]):
                    # Si se encuentra una violación de restricción, la asignación no es consistente.
                    return False
        # Si se verifica con todos los vecinos asignados y no se encuentra ninguna violación, la asignación es consistente.
        return True

    # Implementa el algoritmo de búsqueda con retroceso (Backtracking Search).
    # Es una forma recursiva de búsqueda que intenta construir una solución asignando valores a las variables una por una.
    # Si una asignación es inconsistente, "retrocede" (deshace la asignación) y prueba otro valor o rama.
    # Recibe: asignacion (el estado actual de la asignación parcial, por defecto vacío al inicio).
    def backtracking_search(self, asignacion={}):
        # --- Caso Base ---
        # Si el número de variables en la asignación actual es igual al número total de variables,
        # significa que se ha encontrado una asignación completa (una solución).
        if len(asignacion) == len(self.variables):
            # Retorna la asignación completa (la solución).
            return asignacion

        # --- Selección de Variable (Simple) ---
        # Selecciona la próxima variable no asignada. En esta implementación, simplemente toma la primera variable
        # que no está en el diccionario de asignación.
        var = next(v for v in self.variables if v not in asignacion)

        # --- Iteración sobre el Dominio y Recursión ---
        # Itera sobre cada posible valor en el dominio de la variable seleccionada.
        for val in self.dominios[var]:
            # Comprueba si asignar este 'val' a 'var' es consistente con la asignación parcial actual.
            if self.consistente(var, val, asignacion):
                # Si es consistente:
                # Realiza la asignación tentativa: asigna 'val' a 'var' en la asignación parcial.
                asignacion[var] = val
                # Realiza una llamada recursiva para intentar resolver el resto del CSP con esta nueva asignación.
                resultado = self.backtracking_search(asignacion)
                # Si la llamada recursiva retorna un resultado (es decir, encontró una solución en esa rama).
                if resultado:
                    # Retorna la solución encontrada hacia arriba en la pila de llamadas.
                    return resultado
                # --- Retroceso (Backtracking) ---
                # Si la llamada recursiva no encontró una solución en esta rama (retornó None),
                # deshace la última asignación para probar otro valor para 'var'.
                del asignacion[var]

        # Si el bucle termina (se han probado todos los valores para 'var' y ninguno llevó a una solución consistente),
        # retorna None, indicando que no hay solución posible a partir de la asignación parcial actual en esta rama.
        return None

    # Implementa el algoritmo AC-3 (Arc Consistency Algorithm 3).
    # AC-3 es un algoritmo de propagación de restricciones que reduce los dominios de las variables
    # eliminando valores que no son consistentes con alguna restricción binaria.
    # Garantiza la consistencia de arcos.
    def ac3(self):
        # --- Inicialización de la Cola ---
        # Crea una cola de arcos para revisar. Inicialmente, la cola contiene todos los arcos posibles (pares ordenados de variables).
        # itertools.product(iterable, repeat=2) genera todas las combinaciones con repetición de longitud 2 del iterable.
        cola = list(itertools.product(self.variables, repeat=2))

        # --- Proceso de Revisión Iterativo ---
        # Bucle principal de AC-3. Continúa mientras haya arcos en la cola para revisar.
        while cola:
            # Saca un arco (variable_i, variable_j) de la cola.
            xi, xj = cola.pop() # Usamos pop() para simplicidad, deque sería más eficiente para una cola pura.

            # Llama al método auxiliar 'revisar_dominio' para intentar reducir el dominio de xi basado en xj.
            if self.revisar_dominio(xi, xj):
                # Si 'revisar_dominio' retornó True (el dominio de xi se redujo):
                # Comprueba si el dominio de xi ha quedado vacío. Si es así, el CSP no tiene solución.
                if not self.dominios[xi]:
                    # Retorna False para indicar que el CSP es inconsistente.
                    return False
                # Si el dominio de xi se redujo pero no quedó vacío:
                # Añade todos los arcos (variable_k, variable_i) a la cola, donde xk es un vecino de xi.
                # Esto se hace porque la reducción del dominio de xi puede hacer que algunos valores
                # en los dominios de sus vecinos (xk) dejen de ser consistentes con xi.
                for xk in self.vecinos[xi]:
                    # Asegura que no añadamos el arco (xj, xi) de vuelta inmediatamente (ya se procesará o ya fue procesado).
                    if xk != xj:
                        # Añade el arco (vecino_de_xi, xi) a la cola para su revisión.
                        cola.append((xk, xi))

        # Si el bucle termina (la cola está vacía) sin encontrar un dominio vacío,
        # significa que se ha alcanzado la consistencia de arcos.
        # Retorna True para indicar que el CSP es arc-consistente (aunque no necesariamente resuelto).
        return True

    # Método auxiliar para el algoritmo AC-3. Revisa y reduce el dominio de 'xi' basado en la restricción con 'xj'.
    # Para cada valor en el dominio de 'xi', comprueba si existe al menos un valor en el dominio de 'xj'
    # que sea consistente con él según la restricción entre xi y xj. Si un valor en el dominio de xi no tiene
    # ningún valor consistente en el dominio de xj, ese valor se elimina del dominio de xi.
    # Recibe: las dos variables del arco (xi, xj).
    # Retorna: True si el dominio de xi fue modificado, False en caso contrario.
    def revisar_dominio(self, xi, xj):
        # Inicializa un flag para indicar si el dominio de xi ha sido revisado (modificado).
        revisado = False
        # Itera sobre los valores en el dominio de xi. Hacemos una copia [:] porque podríamos modificar la lista mientras iteramos.
        for x in self.dominios[xi][:]:
            # Comprueba si NO existe NINGÚN valor 'y' en el dominio de xj (self.dominios[xj])
            # tal que el par (x, y) esté permitido por la restricción entre xi y xj.
            # self.restricciones.get((xi, xj), []) obtiene la lista de pares permitidos; si no hay restricción explícita, se asume que todos los pares son permitidos (lista vacía de NO permitidos).
            # La negación 'not any(...)' verifica si *ningún* 'y' funciona.
            if not any((x, y) in self.restricciones.get((xi, xj), []) for y in self.dominios[xj]):
                # Si NO hay ningún valor 'y' en el dominio de xj consistente con 'x', entonces 'x' es inconsistente con el arco (xi, xj).
                # Elimina el valor 'x' del dominio de xi.
                self.dominios[xi].remove(x)
                # Establece el flag 'revisado' a True para indicar que se realizó una modificación.
                revisado = True
        # Retorna el flag 'revisado', indicando si el dominio de xi fue reducido.
        return revisado

# Este bloque de código solo se ejecuta cuando el script se corre directamente.
# Contiene un ejemplo de un CSP: el problema del coloreado del mapa de Australia.
# Variables: las regiones de Australia. Dominio: {rojo, verde, azul}. Restricción: regiones adyacentes deben tener colores diferentes.
if __name__ == "__main__":
    # Define las variables del CSP: las regiones de Australia.
    variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T'] # Australia Occidental, Territorio del Norte, Australia del Sur, Queensland, Nueva Gales del Sur, Victoria, Tasmania.

    # Define el dominio de valores para cada variable: los colores disponibles.
    colores = ['rojo', 'verde', 'azul']

    # Inicializa el diccionario de dominios: cada variable inicialmente puede tener cualquiera de los colores.
    # colores[:] crea una copia de la lista de colores para cada variable, asegurando que cada dominio sea independiente.
    dominios = {v: colores[:] for v in variables}

    # Inicializa un diccionario vacío para almacenar las restricciones.
    restricciones = {}

    # Define las pares de regiones adyacentes. Las regiones adyacentes no pueden tener el mismo color.
    adyacentes = [
        ('WA', 'NT'), ('WA', 'SA'), ('NT', 'SA'), ('NT', 'Q'),
        ('SA', 'Q'), ('SA', 'NSW'), ('SA', 'V'), ('Q', 'NSW'), ('NSW', 'V')
    ]
    # Tasmania ('T') no es adyacente a ninguna otra región continental.

    # --- Definición de Restricciones ---
    # Itera sobre cada par de regiones adyacentes definidas.
    for (a, b) in adyacentes:
        # Define la restricción para el par (a, b): la lista de pares de colores *permitidos*.
        # Son todas las combinaciones de colores (x, y) donde x es diferente de y.
        restricciones[(a, b)] = [(x, y) for x in colores for y in colores if x != y]
        # Asegura que la restricción sea simétrica añadiendo también el par (b, a) con los pares de colores invertidos.
        restricciones[(b, a)] = [(y, x) for x, y in restricciones[(a, b)]] # Asegura simetría en la definición de restricciones

    # Crea una instancia del Problema CSP con las variables, dominios iniciales y restricciones definidas.
    problema = CSP(variables, dominios, restricciones)

    # --- Aplicación de Propagación de Restricciones ---
    # Llama al método AC-3 para hacer el CSP arc-consistente antes de intentar resolverlo.
    # AC-3 puede reducir los dominios de las variables, potencialmente haciendo la búsqueda más eficiente o detectando inconsistencias tempranamente.
    problema.ac3() # Aplica AC-3 para reducir los dominios si es posible

    # --- Búsqueda de Solución ---
    # Llama al método backtracking_search para encontrar una solución al CSP.
    # La búsqueda se realiza sobre los dominios (posiblemente reducidos) después de AC-3.
    solucion = problema.backtracking_search()

    # --- Presentación de Resultados ---
    # Comprueba si se encontró una solución (si 'solucion' no es None).
    if solucion:
        # Si se encontró una solución, imprime un encabezado.
        print("Solución encontrada:")
        # Itera sobre los pares (región, color) en el diccionario de la solución e imprime la asignación para cada región.
        for region, color in solucion.items():
            print(f"{region}: {color}")
    else:
        # Si 'solucion' es None, significa que no se encontró una asignación válida.
        print("No se encontró una solución válida.")