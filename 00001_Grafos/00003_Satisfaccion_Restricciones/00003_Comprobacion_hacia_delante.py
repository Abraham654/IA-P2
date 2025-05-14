# Define una clase para representar un CSP y resolverlo usando Búsqueda con Retroceso y Forward Checking.
# El Forward Checking es una técnica de propagación de restricciones que, al asignar un valor a una variable,
# elimina los valores inconsistentes de los dominios de las variables vecinas no asignadas.
class ForwardCheckingCSP:
    # Método constructor de la clase.
    # Recibe variables, dominios y restricciones.
    def __init__(self, variables, dominios, restricciones):
        # Inicializa variables, copia editable de dominios y restricciones
        self.variables = variables # Almacena la lista de variables.

        # Crea una copia *profunda* de los dominios iniciales.
        # Es crucial tener dominios editables porque Forward Checking los modificará (poda valores).
        # Usamos list(dominios[v]) para crear una nueva lista para cada dominio.
        self.dominios = {v: list(dominios[v]) for v in variables}

        self.restricciones = restricciones # Almacena la lista de restricciones (formato similar al ejemplo anterior).

        # Diccionario para almacenar la asignación parcial actual durante la búsqueda.
        self.asignacion = {}

    # Método auxiliar para verificar si la asignación actual está completa.
    # Es completa cuando todas las variables tienen un valor asignado.
    def es_completa(self):
        # Verifica si todas las variables están asignadas
        return len(self.asignacion) == len(self.variables)

    # Método para verificar si un valor 'valor' para una 'variable' es consistente con las restricciones.
    # Esta versión parece diseñada para verificar si una restricción particular es satisfecha cuando todas sus variables están asignadas
    # en una asignación temporal (que incluye la asignación 'variable: valor').
    def es_consistente(self, variable, valor): # Note: El nombre del método puede ser un poco confuso en el contexto de FC; se usa para evaluar restricciones completas.
        # Verifica que un valor no viole ninguna restricción
        # Crea una asignación temporal combinando la asignación actual con la asignación tentativa de 'variable: valor'.
        temp_asign = {**self.asignacion, variable: valor}

        # Itera sobre todas las restricciones definidas.
        for vars_r, funcion in self.restricciones:
            # Comprueba si todas las variables involucradas en esta restricción (vars_r) están presentes en la asignación temporal.
            # Esto significa que la restricción puede ser evaluada con los valores de temp_asign.
            if all(v in temp_asign for v in vars_r):
                # Si todas las variables de la restricción están asignadas en temp_asign:
                # Llama a la función de restricción, pasando los valores de esas variables desde temp_asign
                # como argumentos de palabra clave (**{v: temp_asign[v] for v in vars_r} convierte la lista de variables en argumentos de palabra clave).
                # Si la función retorna False, la restricción se viola.
                if not funcion(**{v: temp_asign[v] for v in vars_r}):
                    # Si la restricción se viola, la asignación tentativa no es consistente.
                    return False
        # Si se verifican todas las restricciones relevantes y ninguna se viola en temp_asign, la asignación es consistente.
        return True # Nota: La consistencia aquí se evalúa en el contexto de temp_asign, no solo self.asignacion.

    # Método principal para el Forward Checking.
    # Al asignar 'valor' a 'variable', este método poda (elimina) los valores inconsistentes
    # de los dominios de las variables vecinas *no asignadas*.
    # Recibe: la variable a la que se asignó un valor y el valor asignado.
    # Retorna: True si no se encontró ningún dominio vacío después de la poda, False si algún dominio se quedó vacío.
    def forward_check(self, variable, valor):
        # Elimina valores inconsistentes en vecinos (forward checking)

        # Crea una copia de los dominios actuales ANTES de podar.
        # Esta copia se guarda en el método _backtrack para poder restaurarla si la rama falla.
        # La copia local dominios_temp aquí no se usa para restauración en este método, pero la lógica de copia es relevante.
        # dominios_temp = {v: list(self.dominios[v]) for v in self.variables} # Esta línea no es funcionalmente necesaria en este método.

        # Itera sobre las variables vecinas de la variable a la que acabamos de asignar un valor.
        # obtener_vecinos() encuentra variables conectadas por restricciones.
        for vecino in self.obtener_vecinos(variable):
            # El Forward Checking solo se aplica a variables VECINAS que aún NO han sido asignadas.
            if vecino not in self.asignacion:
                # Itera sobre una *copia* de la lista de valores en el dominio del vecino.
                # Hacemos una copia (list(...)) porque podríamos eliminar valores mientras iteramos.
                for val in list(self.dominios[vecino]):
                    # Comprueba si asignar este 'val' al 'vecino' sería consistente dada la asignación parcial actual MÁS la nueva asignación de 'variable: valor'.
                    # Esta llamada a 'es_consistente' usará internamente {**self.asignacion, variable: valor} para formar temp_asign y evaluar restricciones.
                    if not self.es_consistente(vecino, val):
                        # Si la asignación (vecino = val) no es consistente con el estado actual (asignacion + (variable=valor)):
                        # Elimina este 'val' del dominio del vecino. Esto es la poda.
                        self.dominios[vecino].remove(val)
                        # Después de eliminar un valor, comprueba si el dominio del vecino se ha quedado vacío.
                        if not self.dominios[vecino]:
                            # Si el dominio del vecino está vacío, significa que la asignación actual (variable=valor) lleva a una contradicción.
                            # Retorna False para indicar un fallo en esta rama de búsqueda.
                            return False # Dominio vacío, fallo

        # Si se itera sobre todos los vecinos no asignados y se podan sus dominios sin encontrar ningún dominio vacío,
        # significa que la asignación de 'variable=valor' es consistente localmente con los vecinos y la poda fue exitosa.
        # Retorna True.
        return True

    # Método auxiliar para encontrar las variables que están relacionadas por una restricción con una variable dada.
    # Recibe: una variable.
    # Retorna: un conjunto de variables vecinas.
    def obtener_vecinos(self, variable):
        # Devuelve variables relacionadas por restricciones
        vecinos = set() # Usamos un conjunto para evitar duplicados.
        # Itera sobre todas las restricciones.
        for vars_r, _ in self.restricciones:
            # Si la variable dada está involucrada en esta restricción:
            if variable in vars_r:
                # Añade a 'vecinos' todas las variables de la restricción que no sean la variable dada.
                vecinos.update(v for v in vars_r if v != variable)
        # Retorna el conjunto de vecinos.
        return vecinos

    # Método para seleccionar la próxima variable no asignada utilizando la heurística MRV (Minimum Remaining Values).
    # Prioriza la variable con el dominio más pequeño, ya que es la que tiene más probabilidades de causar un fallo temprano si no hay solución.
    def seleccionar_variable(self):
        # Heurística MRV: elige variable con menor dominio posible
        # Crea una lista de variables que aún no están en la asignación.
        no_asignadas = [v for v in self.variables if v not in self.asignacion]
        # Usa 'min' con una clave lambda que retorna la longitud del dominio actual (posiblemente reducido por FC) de la variable.
        return min(no_asignadas, key=lambda v: len(self.dominios[v]))

    # Método de entrada para iniciar el proceso de resolución del CSP.
    def resolver(self):
        # Inicia el backtracking llamando al método recursivo principal.
        return self._backtrack()

    # Método recursivo principal que implementa la Búsqueda con Retroceso mejorada con Forward Checking.
    def _backtrack(self):
        # --- Caso Base ---
        # Si la asignación actual está completa, se ha encontrado una solución.
        if self.es_completa():
            return self.asignacion # Retorna la asignación completa.

        # --- Selección de Variable ---
        # Selecciona la próxima variable a asignar utilizando la heurística MRV.
        var = self.seleccionar_variable()

        # --- Iteración sobre Valores y Forward Checking ---
        # Itera sobre los valores en el dominio *actual* (posiblemente reducido por FC) de la variable seleccionada.
        # Hacemos una copia (list(...)) porque el Forward Checking en llamadas recursivas posteriores podría modificar este dominio.
        for val in list(self.dominios[var]):
            # Opcional: una verificación de consistencia básica. Si es_consistente verifica contra la asignación actual, esta línea es útil.
            # Si es_consistente verifica contra la asignación temporal + (var=val), esta línea es redundante con el check dentro de forward_check.
            # Suponiendo que verifica contra la asignación actual:
            if self.es_consistente(var, val):
                 # Si la asignación básica es consistente:
                # Realiza la asignación tentativa.
                self.asignacion[var] = val

                # --- Paso de Forward Checking y Guardado de Dominios ---
                # Guarda una copia de los dominios *antes* de realizar el Forward Checking para esta asignación.
                # Esto es necesario para restaurar los dominios si esta rama falla.
                dominios_previos = {v: list(self.dominios[v]) for v in self.variables}

                # Realiza el Forward Checking: poda los dominios de los vecinos no asignados.
                # Si self.forward_check(var, val) retorna True, significa que la poda no encontró ningún dominio vacío.
                if self.forward_check(var, val):
                    # Si el Forward Checking tuvo éxito:
                    # Realiza la llamada recursiva para intentar completar la asignación con los dominios podados.
                    resultado = self._backtrack()
                    # Si la llamada recursiva retorna un resultado (no es None), significa que se encontró una solución en esta rama.
                    if resultado is not None:
                         # Propaga la solución hacia arriba.
                         return resultado

                # --- Retroceso y Restauración de Dominios ---
                # Si el Forward Checking falló (retornó False) O la llamada recursiva no encontró una solución:
                # Deshace la última asignación.
                self.asignacion.pop(var)
                # Restaura los dominios a su estado antes de que se realizara el Forward Checking para esta asignación.
                # Esto deshace la poda realizada en forward_check(var, val).
                self.dominios = dominios_previos

        # Si el bucle sobre los valores termina y ninguno llevó a una solución, retorna None.
        return None

# --- Ejemplo: Coloreado de mapas ---
# Problema del coloreado del mapa de Australia, similar al ejemplo anterior, pero resuelto con Forward Checking.
if __name__ == "__main__":
    # Define las variables (regiones) y sus dominios (colores).
    variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
    dominios = {v: ['rojo', 'verde', 'azul'] for v in variables}

    # Define la función de restricción para vecinos: deben tener colores diferentes.
    # Usa **kwargs para aceptar los valores de las variables por su nombre, lo cual encaja con 'es_consistente'.
    def diferente_color(**kwargs):
        # Convierte los valores de los argumentos de palabra clave en una lista.
        vals = list(kwargs.values())
        # Comprueba si el primer valor es diferente del segundo.
        return vals[0] != vals[1]

    # Define la lista de restricciones. Cada restricción es una tupla: (variables involucradas, función de restricción).
    # Las variables involucradas son pares de regiones adyacentes.
    restricciones = [
        (('WA', 'NT'), diferente_color), # WA y NT deben tener colores diferentes.
        (('WA', 'SA'), diferente_color), # WA y SA deben tener colores diferentes.
        (('NT', 'SA'), diferente_color),
        (('NT', 'Q'), diferente_color),
        (('SA', 'Q'), diferente_color),
        (('SA', 'NSW'), diferente_color),
        (('SA', 'V'), diferente_color),
        (('Q', 'NSW'), diferente_color),
        (('NSW', 'V'), diferente_color)
        # Tasmania ('T') no tiene restricciones con otras variables en este ejemplo.
    ]

    # Crea una instancia del problema CSP con Forward Checking.
    csp = ForwardCheckingCSP(variables, dominios, restricciones)

    # Llama al método 'resolver' para iniciar el proceso de backtracking con forward checking.
    solucion = csp.resolver()

    # Imprime el resultado.
    print("Solución encontrada:")
    # Si se encontró una solución, itera sobre la asignación (ordenada por nombre de región) e imprime cada asignación.
    if solucion:
        for region, color in sorted(solucion.items()):
            print(f"{region}: {color}")
    else:
        # Si no se encontró solución, imprime un mensaje.
        print("No se encontró solución.")