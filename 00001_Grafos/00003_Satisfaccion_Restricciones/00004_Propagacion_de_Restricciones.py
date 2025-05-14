from collections import deque # Importa la clase deque, una cola doblemente terminada eficiente para añadir y eliminar elementos de ambos extremos. Se usa aquí para la cola de arcos en el algoritmo AC-3.

# Define una clase para representar un CSP con énfasis en la propagación de restricciones usando AC-3.
# Resuelve el CSP aplicando AC-3 primero para reducir dominios, y luego usando Backtracking Search.
class ConstraintPropagationCSP:
    # Método constructor de la clase.
    # Recibe variables, dominios iniciales y restricciones.
    def __init__(self, variables, dominios, restricciones):
        # Inicializa variables, copia de dominios y restricciones bidireccionales
        self.variables = variables # Almacena la lista de variables.

        # Crea una copia editable de los dominios iniciales. Los dominios serán modificados (podados) por AC-3.
        self.dominios = {v: list(dominios[v]) for v in variables}

        # Almacena las restricciones. Llama a _hacer_bidireccionales para asegurar que cada restricción binaria
        # esté representada en ambas direcciones ((A, B) y (B, A)) en el diccionario interno.
        # El formato de restricciones de entrada se espera que sea { (v1, v2): funcion_restr, ...}.
        self.restricciones = self._hacer_bidireccionales(restricciones)

        # Construye la cola inicial de arcos para el algoritmo AC-3 a partir de las claves del diccionario de restricciones bidireccionales.
        self.arcos = self._construir_arcos()

    # Método auxiliar para asegurar que todas las restricciones binarias estén definidas en ambas direcciones.
    # Esto es necesario para AC-3, que revisa arcos (xi, xj) y (xj, xi).
    # Recibe un diccionario de restricciones (posiblemente unidireccionales).
    # Retorna un nuevo diccionario con restricciones bidireccionales.
    def _hacer_bidireccionales(self, restricciones):
        # Duplica restricciones en ambas direcciones
        bidireccionales = {} # Diccionario para almacenar las restricciones bidireccionales.
        # Itera sobre cada par (tupla_variables, función_restricción) en el diccionario de restricciones de entrada.
        for (a, b), func in restricciones.items():
            # Añade la restricción original (a, b) -> func al diccionario bidireccional.
            bidireccionales[(a, b)] = func
            # Añade la restricción inversa (b, a) -> lambda.
            # La función lambda toma dos argumentos (x, y) y llama a la función original 'func' con los argumentos invertidos (y, x).
            # Esto asegura que la función de restricción funcione correctamente independientemente del orden de las variables en el arco.
            bidireccionales[(b, a)] = lambda x, y: func(y, x)
        # Retorna el diccionario de restricciones bidireccionales.
        return bidireccionales

    # Método auxiliar para construir la cola inicial de arcos para AC-3.
    # La cola de arcos contiene todas las restricciones binarias definidas en el grafo, en ambas direcciones.
    # Retorna un deque (cola) de tuplas (variable_i, variable_j).
    def _construir_arcos(self):
        # Genera lista de todos los arcos (xi, xj)
        # Crea un deque que contiene todas las claves (las tuplas de variables, que representan arcos) del diccionario de restricciones bidireccionales.
        return deque(self.restricciones.keys())

    # Método auxiliar central para el algoritmo AC-3. Revisa un arco (xi, xj).
    # Intenta eliminar valores del dominio de 'xi' que no son consistentes con algún valor en el dominio de 'xj' según la restricción entre ellos.
    # Recibe: las dos variables del arco (xi, xj).
    # Retorna: True si el dominio de xi fue reducido, False en caso contrario.
    def _revisar(self, xi, xj):
        # Revisa y elimina valores en xi que no satisfacen la restricción con xj
        revisado = False # Flag para rastrear si se realizaron eliminaciones en el dominio de xi.
        # Itera sobre una *copia* del dominio de xi. Es importante copiar porque podríamos eliminar elementos.
        for x in list(self.dominios[xi]):
            # Comprueba si NO existe NINGÚN valor 'y' en el dominio de xj (self.dominios[xj])
            # tal que la función de restricción entre xi y xj (self.restricciones[(xi, xj)]) retorne True cuando se llama con (x, y).
            # 'any(...)' retorna True si al menos un 'y' satisface la condición; 'not any(...)' es True si *ningún* 'y' lo hace.
            if not any(self.restricciones[(xi, xj)](x, y) for y in self.dominios[xj]):
                # Si no se encuentra ningún valor 'y' consistente en el dominio de xj para el valor 'x' de xi:
                # Elimina el valor 'x' del dominio de xi. Esto es la poda de dominio.
                self.dominios[xi].remove(x)
                # Establece el flag 'revisado' a True para indicar que se modificó el dominio de xi.
                revisado = True
        # Retorna 'revisado', indicando si el dominio de xi fue modificado.
        return revisado

    # Implementa el algoritmo AC-3 (Arc Consistency Algorithm 3).
    # Procesa la cola de arcos, revisando cada arco. Si la revisión de un arco (xi, xj)
    # reduce el dominio de xi, añade todos los arcos (xk, xi) (donde xk es un vecino de xi) de nuevo a la cola.
    def ac3(self):
        # Algoritmo AC-3: mantiene consistencia entre arcos
        # Inicializa la cola de arcos con todos los arcos bidireccionales construidos previamente.
        cola = deque(self.arcos)

        # Bucle principal de AC-3. Continúa mientras la cola de arcos no esté vacía.
        while cola:
            # Extrae el primer arco (variable_i, variable_j) de la cola (FIFO).
            xi, xj = cola.popleft()

            # Revisa el arco (xi, xj) llamando al método _revisar.
            if self._revisar(xi, xj):
                # Si _revisar retorna True (el dominio de xi se redujo):
                # Comprueba si el dominio de xi se ha quedado vacío. Si es así, el CSP no tiene solución.
                if not self.dominios[xi]:
                    # Retorna False inmediatamente para indicar que el CSP es inconsistente.
                    return False # No hay solución posible

                # Si el dominio de xi se redujo pero no quedó vacío:
                # Añade a la cola todos los arcos (xk, xi) donde xk es un vecino de xi.
                # Esto es necesario porque la reducción del dominio de xi puede afectar la consistencia de estos arcos.
                for xk in self._vecinos(xi):
                    # Asegura que no añadamos el arco (xj, xi) de vuelta a menos que sea estrictamente necesario (aunque la regla estándar de AC-3 a menudo añade todos los vecinos, la condición xk != xj es común para evitar ciclos triviales inmediatos).
                    if xk != xj:
                        # Añade el arco (vecino_de_xi, xi) a la cola para su revisión.
                        cola.append((xk, xi))

        # Si el bucle termina (la cola está vacía) sin encontrar un dominio vacío,
        # significa que se ha alcanzado la consistencia de arcos.
        # Retorna True para indicar que el CSP es arc-consistente (no necesariamente resuelto, pero con dominios podados).
        return True

    # Método auxiliar para obtener las variables que son vecinas (conectadas por una restricción) de una variable dada.
    # Recibe: una variable.
    # Retorna: un conjunto de variables vecinas.
    def _vecinos(self, variable):
        # Devuelve vecinos conectados por restricciones
        # Busca en las claves del diccionario de restricciones bidireccionales (que son tuplas (xi, xj)).
        # Si la primera variable en la tupla (xi) coincide con la variable dada, añade la segunda variable (xj) al conjunto.
        # Usamos un conjunto para asegurar que cada vecino aparezca solo una vez.
        return {xj for (xi, xj) in self.restricciones if xi == variable}

    # Método principal para resolver el CSP.
    # Primero aplica el algoritmo AC-3 para podar los dominios, y luego inicia la búsqueda con retroceso.
    def resolver(self):
        # Aplica AC-3 y luego backtracking si es necesario
        # Llama a AC-3. Si retorna False, el CSP no tiene solución.
        if not self.ac3():
            # Si AC-3 determina que no hay solución, retorna None.
            return None
        # Si AC-3 retorna True (el CSP es arc-consistente), inicia la búsqueda con retroceso.
        # Llama al método recursivo _backtrack con un diccionario de asignación inicial vacío.
        return self._backtrack({})

    # Método recursivo principal que implementa la Búsqueda con Retroceso (Backtracking Search).
    # Trabaja con los dominios que ya han sido posiblemente reducidos por AC-3.
    # Recibe: el diccionario de asignación parcial actual (este diccionario se pasa y modifica recursivamente).
    def _backtrack(self, asignacion):
        # Algoritmo de búsqueda con backtracking
        # --- Caso Base ---
        # Si la longitud de la asignación es igual al número total de variables, se ha encontrado una solución completa.
        if len(asignacion) == len(self.variables):
            return asignacion # Retorna la asignación (la solución).

        # --- Selección de Variable (MRV) ---
        # Selecciona la próxima variable no asignada utilizando la heurística MRV (mínimo dominio restante).
        # _seleccionar_variable necesita saber qué variables ya están asignadas para encontrar las no asignadas.
        var = self._seleccionar_variable(asignacion)

        # --- Iteración sobre Valores ---
        # Itera sobre los valores en el dominio actual (posiblemente podado por AC-3) de la variable seleccionada.
        # No es necesario copiar el dominio aquí, ya que _backtrack no modifica self.dominios directamente (AC-3 lo hizo antes).
        for val in self.dominios[var]:
            # --- Verificación de Consistencia ---
            # Comprueba si asignar este 'val' a 'var' es consistente con la asignación parcial actual.
            # _es_consistente verifica si esta nueva asignación viola alguna restricción con las variables ya asignadas.
            if self._es_consistente(var, val, asignacion):
                # Si es consistente:
                # Realiza la asignación tentativa: añade la variable y su valor al diccionario de asignación.
                # Como 'asignacion' es un diccionario, modificarlo aquí afectará a la copia pasada recursivamente.
                asignacion[var] = val
                # --- Llamada Recursiva ---
                # Realiza una llamada recursiva a _backtrack con la asignación actualizada.
                resultado = self._backtrack(asignacion)
                # Si la llamada recursiva retorna un resultado (no es None), significa que se encontró una solución en esa rama.
                if resultado:
                    return resultado # Propaga la solución hacia arriba.
                # --- Retroceso (Backtracking) ---
                # Si la llamada recursiva no encontró una solución (retornó None),
                # deshace la última asignación para probar otro valor para 'var'.
                del asignacion[var]

        # Si el bucle sobre los valores termina y ninguno llevó a una solución, retorna None.
        return None # No se encontró solución en esta rama.

    # Método auxiliar para seleccionar la próxima variable no asignada utilizando la heurística MRV.
    # Recibe: el diccionario de asignación parcial actual.
    # Retorna: la variable no asignada con el dominio más pequeño.
    def _seleccionar_variable(self, asignacion):
        # Selecciona variable no asignada con menor dominio (MRV)
        # Crea una lista de variables que aún no están en la asignación actual.
        no_asignadas = [v for v in self.variables if v not in asignacion]
        # Encuentra la variable en 'no_asignadas' cuyo dominio (en self.dominios) tiene la menor longitud.
        return min(no_asignadas, key=lambda v: len(self.dominios[v]))

    # Método auxiliar para verificar si asignar 'val' a 'var' es consistente con la 'asignacion' parcial actual.
    # Comprueba si la asignación (var = val) viola alguna restricción binaria con las variables que ya están asignadas.
    # Recibe: la variable, el valor a probar, y la asignación parcial actual.
    # Retorna: True si es consistente, False si se viola alguna restricción con un vecino asignado.
    def _es_consistente(self, var, val, asignacion):
        # Revisa si val para var es consistente con la asignación actual
        # Itera sobre cada restricción binaria definida en el diccionario bidireccional.
        for (vi, vj), restr in self.restricciones.items():
            # Caso 1: La variable a asignar es la primera variable en la restricción (var == vi).
            # Comprueba si la segunda variable en la restricción (vj) ya está asignada.
            if var == vi and vj in asignacion:
                # Si vj está asignada, evalúa la función de restricción con el valor tentativo para 'var' (val)
                # y el valor asignado para 'vj' (asignacion[vj]). Si la función retorna False, se viola la restricción.
                if not restr(val, asignacion[vj]):
                    return False # Inconsistente.
            # Caso 2: La variable a asignar es la segunda variable en la restricción (var == vj).
            # Comprueba si la primera variable en la restricción (vi) ya está asignada.
            elif var == vj and vi in asignacion:
                # Si vi está asignada, evalúa la función de restricción con el valor asignado para 'vi' (asignacion[vi])
                # y el valor tentativo para 'var' (val). Si la función retorna False, se viola la restricción.
                if not restr(asignacion[vi], val):
                    return False # Inconsistente.
        # Si ninguna restricción relevante con vecinos asignados es violada, la asignación tentativa es consistente.
        return True

# ---------- Ejemplo: Coloreado de mapas ----------
# Problema del coloreado del mapa de Australia, resuelto con AC-3 + Backtracking.
if __name__ == "__main__":
    # Define las variables (regiones) y sus dominios (colores).
    variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
    dominios = {v: list(['rojo', 'verde', 'azul']) for v in variables} # Usamos list() para asegurar copias mutables.

    # Define la función de restricción para vecinos: deben tener colores diferentes.
    # Esta función toma dos argumentos, c1 y c2.
    def diferente_color(c1, c2):
        return c1 != c2

    # Define el diccionario de restricciones. La clave es una tupla (variable1, variable2), el valor es la función de restricción.
    # Solo necesitamos definir la restricción una vez por par de variables (la clase la hará bidireccional).
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
        # Tasmania 'T' no tiene restricciones en este ejemplo.
    }

    # Crea una instancia del problema CSP, que aplicará AC-3 en la inicialización y luego Backtracking.
    csp = ConstraintPropagationCSP(variables, dominios, restricciones)

    # Llama al método 'resolver' para iniciar el proceso (AC-3 seguido de Backtracking si AC-3 no falla).
    solucion = csp.resolver()

    # Imprime el resultado.
    print("Solución encontrada:")
    # Si se encontró una solución, itera sobre la asignación (no se garantiza orden aquí, pero se imprime).
    # Si deseas ordenar, podrías usar sorted(solucion.items()).
    if solucion:
        for region, color in solucion.items():
            print(f"{region}: {color}")
    else:
        # Si no se encontró solución (por AC-3 o Backtracking), imprime un mensaje.
        print("No se encontró solución.")