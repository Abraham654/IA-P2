import random # Importa la librería 'random', fundamental para operaciones probabilísticas como selección, cruce y mutación en algoritmos genéticos, así como para crear individuos iniciales al azar.
import heapq # Importa la librería 'heapq', utilizada para implementar una cola de prioridad (min-heap). Se usa aquí para seleccionar eficientemente los k mejores individuos en el paso de reemplazo (elitismo simplificado).
from copy import deepcopy # Importa 'deepcopy' del módulo 'copy'. Se usa para crear copias completamente independientes de individuos (especialmente en el cruce) para evitar que las modificaciones en los hijos afecten a los padres originales.

# Define la función principal que implementa el Algoritmo Genético (Genetic Algorithm).
# Los algoritmos genéticos son algoritmos de búsqueda evolutiva inspirados en la selección natural.
# Trabajan con una población de soluciones candidatas y las mejoran a lo largo de generaciones mediante selección, cruce y mutación.
# Recibe:
# - problema: Un objeto que define el problema a resolver. Debe tener los métodos:
#   - crear_individuo(): Genera un individuo aleatorio válido (una solución candidata).
#   - fitness(individuo): Calcula el valor (aptitud) de un individuo. El algoritmo busca maximizar esta aptitud.
#   - cruzar(padre1, padre2): Combina dos individuos para crear uno o más descendientes.
#   - mutar(individuo): Aplica pequeños cambios aleatorios a un individuo.
# - tam_poblacion: El número de individuos en la población en cada generación.
# - max_generaciones: El número máximo de generaciones que se ejecutarán.
# - prob_cruce: La probabilidad de que dos padres se crucen (en lugar de pasar sin cambios a la siguiente generación).
# - prob_mutacion: La probabilidad de que un hijo mute.
def algoritmo_genetico(problema, tam_poblacion=50, max_generaciones=100, prob_cruce=0.8, prob_mutacion=0.1):
    # --- Inicialización ---
    # Crea la población inicial generando 'tam_poblacion' individuos aleatorios válidos usando el método 'crear_individuo' del problema.
    poblacion = [problema.crear_individuo() for _ in range(tam_poblacion)]

    # --- Ciclo Evolutivo por Generaciones ---
    # Bucle principal que representa la evolución a lo largo de múltiples generaciones.
    for _ in range(max_generaciones):
        # --- Evaluación ---
        # Calcula el fitness (aptitud) de cada individuo en la población actual.
        # Crea una lista de tuplas (fitness, individuo). El fitness es el primer elemento para facilitar la selección basada en fitness.
        evaluaciones = [(problema.fitness(ind), ind) for ind in poblacion]

        # --- Selección ---
        # Comentario que describe el método de selección utilizado: Torneo Binario.
        # En el torneo binario, se seleccionan aleatoriamente 2 individuos y el que tiene mayor fitness gana y pasa a ser un padre.
        # Se repite hasta seleccionar 'tam_poblacion' padres. Esto introduce un sesgo a favor de los individuos más aptos.
        padres = []
        # Bucle para seleccionar 'tam_poblacion' padres.
        for _ in range(tam_poblacion):
            # Selecciona 2 individuos aleatoriamente (sin reemplazo) de la lista de evaluaciones.
            a, b = random.sample(evaluaciones, 2)
            # Compara el fitness de los dos individuos seleccionados (a[0] > b[0]).
            # Añade el individuo con mayor fitness (la tupla (fitness, individuo)) a la lista de padres.
            padres.append(a if a[0] > b[0] else b)

        # --- Cruce (Recombinación) y Mutación ---
        # Inicializa una lista vacía para la nueva generación de individuos (los hijos).
        nueva_poblacion = []
        # Itera sobre la lista de padres, tomando pares de padres (i, i+1) para el cruce.
        # El paso es 2 porque procesamos padres en pares.
        for i in range(0, tam_poblacion, 2):
            # Selecciona el primer padre del par. Obtenemos el individuo (elemento [1] de la tupla (fitness, individuo)).
            p1 = padres[i][1]
            # Selecciona el segundo padre del par.
            # Si tam_poblacion es impar y estamos en el último elemento (i+1 sería fuera del rango),
            # usamos el primer padre (padres[0][1]) como segundo padre para asegurar que siempre haya un par.
            p2 = padres[i+1][1] if i+1 < tam_poblacion else padres[0][1]

            # --- Operador de Cruce ---
            # Genera un número aleatorio entre 0.0 y 1.0.
            # Si el número aleatorio es menor que la probabilidad de cruce definida, se realiza el cruce.
            if random.random() < prob_cruce:
                # Llama al método 'cruzar' del problema con copias profundas de los padres.
                # 'deepcopy' es importante si el individuo es una estructura mutable (como una lista de listas),
                # para que las modificaciones en los hijos (dentro de 'cruzar') no afecten a los padres originales en la lista 'padres'.
                # El método 'cruzar' retorna una tupla de dos hijos (hijo1, hijo2).
                hijo1, hijo2 = problema.cruzar(deepcopy(p1), deepcopy(p2))
            else:
                # Si el número aleatorio es mayor o igual a la probabilidad de cruce, los padres pasan directamente (copiados) a la siguiente generación como hijos.
                hijo1, hijo2 = deepcopy(p1), deepcopy(p2) # No hay cruce, los hijos son copias de los padres

            # --- Operador de Mutación ---
            # Genera un número aleatorio para decidir si mutar al hijo1.
            if random.random() < prob_mutacion:
                # Si el número aleatorio es menor que la probabilidad de mutación, llama al método 'mutar' en hijo1.
                # Se asume que 'mutar' modifica el individuo in-place y lo retorna.
                hijo1 = problema.mutar(hijo1)
            # Genera un número aleatorio para decidir si mutar al hijo2.
            if random.random() < prob_mutacion:
                # Si el número aleatorio es menor que la probabilidad de mutación, llama al método 'mutar' en hijo2.
                hijo2 = problema.mutar(hijo2)

            # Añade los hijos generados a la lista de la nueva población.
            nueva_poblacion.extend([hijo1, hijo2])

        # --- Reemplazo (Elitismo Simplificado) ---
        # Comentario que describe el método de reemplazo.
        # En esta implementación, la nueva población reemplaza a la antigua.
        # Para mantener el tamaño de la población y aplicar una forma de elitismo,
        # seleccionamos los 'tam_poblacion' individuos con mayor fitness de la 'nueva_poblacion'.
        # Calcula el fitness de los individuos en la 'nueva_poblacion'.
        evaluaciones = [(problema.fitness(ind), ind) for ind in nueva_poblacion]
        # Selecciona los 'tam_poblacion' individuos con mayor fitness de las evaluaciones de la nueva población.
        # heapq.nlargest(k, iterable) retorna los k elementos más grandes (las tuplas con mayor fitness).
        # Usamos una comprensión de lista para extraer solo los individuos (elemento [1] de la tupla) y formar la nueva 'poblacion'.
        poblacion = [ind for (_, ind) in heapq.nlargest(tam_poblacion, evaluaciones)]

    # --- Finalización ---
    # Después de completar todas las generaciones, encuentra el individuo con el fitness más alto en la población final.
    # Crea una lista de tuplas (fitness, individuo) para la población final.
    # Usa la función 'max' con 'key' para encontrar la tupla con el fitness más alto.
    mejor = max([(problema.fitness(ind), ind) for ind in poblacion])
    # Retorna el mejor individuo encontrado (elemento [1] de la tupla 'mejor') y su fitness (elemento [0]).
    return mejor[1], mejor[0]

# Define una clase para modelar el Problema del Viajante (TSP), adaptada para el Algoritmo Genético.
# Un individuo (solución candidata) es una permutación del orden en que se visitan las ciudades.
class ProblemaTSP:
    # Método constructor. Almacena la lista de ciudades y la matriz/diccionario de distancias.
    def __init__(self, ciudades, distancias):
        self.ciudades = ciudades
        self.distancias = distancias # Diccionario de diccionarios {ciudad1: {ciudad2: distancia, ...}, ...}

    # Método para crear un individuo aleatorio válido.
    # En TSP, un individuo válido es una permutación de todas las ciudades.
    def crear_individuo(self):
        # Crea una copia de la lista de ciudades.
        ind = self.ciudades.copy()
        # Baraja la copia para obtener una permutación aleatoria.
        random.shuffle(ind)
        # Retorna la permutación aleatoria como un individuo inicial.
        return ind

    # Método para calcular el fitness (aptitud) de un individuo (una ruta/permutación).
    # La aptitud es inversamente proporcional a la distancia total de la ruta.
    def fitness(self, ind):
        # Calcula la suma de las distancias entre ciudades consecutivas en la ruta, incluyendo el regreso al inicio.
        # Itera sobre los índices de la ruta. (i+1) % len(ind) asegura que la última ciudad se conecte con la primera.
        # Accede a la distancia entre la ciudad en ind[i] y la ciudad en ind[(i+1) % len(ind)].
        total = sum(self.distancias[ind[i]][ind[(i+1) % len(ind)]] for i in range(len(ind)))
        # Retorna el negativo de la distancia total. Maximizar este valor negativo es equivalente a minimizar la distancia total.
        return -total # Negativo para maximizar (minimizar distancia)

    # Método para realizar la operación de cruce (recombinación) entre dos padres (permutaciones).
    # Implementa una versión del cruce ordenado (Order Crossover, OX1).
    # Recibe dos individuos padre, p1 y p2 (se espera que ya sean copias profundas si son mutables).
    # Retorna dos individuos hijos, h1 y h2.
    def cruzar(self, p1, p2):
        size = len(p1) # Obtiene el tamaño del individuo (número de ciudades).
        # Selecciona dos puntos de corte aleatorios distintos para el cruce. Los ordena para que a < b.
        a, b = sorted(random.sample(range(size), 2))

        # Inicializa los hijos h1 y h2.
        # h1 toma el segmento entre los puntos de corte [a:b] de p1.
        h1 = p1[a:b]
        # h2 toma el segmento entre los puntos de corte [a:b] de p2.
        h2 = p2[a:b]

        # Completa el resto de h1 y h2 tomando ciudades de los otros padres, manteniendo el orden original y evitando duplicados.
        # Itera sobre los padres en el orden [p2, p1]. Esto es para llenar h1 con elementos de p2 (fuera del segmento) y h2 con elementos de p1 (fuera del segmento).
        for x in [p2, p1]:
            # Itera sobre cada ciudad en el padre 'x'.
            for ciudad in x:
                # Si la ciudad no está ya en el hijo h1 y h1 aún no tiene el tamaño completo:
                if ciudad not in h1 and len(h1) < size:
                    # Añade la ciudad al final de h1.
                    h1.append(ciudad)
                # Si la ciudad no está ya en el hijo h2 y h2 aún no tiene el tamaño completo:
                if ciudad not in h2 and len(h2) < size:
                    # Añade la ciudad al final de h2.
                    h2.append(ciudad)

        # Retorna los dos individuos hijos resultantes del cruce.
        return h1, h2

    # Método para realizar la operación de mutación en un individuo (una permutación).
    # Implementa la mutación por intercambio simple (swap mutation): intercambia la posición de dos elementos aleatorios.
    # Recibe un individuo 'ind' (se espera que sea una copia si es mutable).
    # Retorna el individuo mutado.
    def mutar(self, ind):
        # Selecciona dos índices distintos al azar dentro del rango de la longitud del individuo.
        i, j = random.sample(range(len(ind)), 2)
        # Intercambia los elementos (ciudades) en las posiciones i y j dentro del individuo.
        ind[i], ind[j] = ind[j], ind[i] # Realiza el intercambio (mutación)
        # Retorna el individuo después de la mutación.
        return ind

# Este bloque de código solo se ejecuta cuando el script se corre directamente.
# Contiene un ejemplo de cómo usar el Algoritmo Genético con el Problema del Viajante.
if __name__ == "__main__":
    # Define la lista de ciudades.
    ciudades = ['A', 'B', 'C', 'D']
    # Define la matriz de distancias como un diccionario de diccionarios.
    # Este ejemplo usa una matriz simétrica (distancia A a B es igual a B a A).
    distancias = {
        'A': {'A': 0, 'B': 2, 'C': 9, 'D': 10},
        'B': {'A': 2, 'B': 0, 'C': 6, 'D': 4},
        'C': {'A': 9, 'B': 6, 'C': 0, 'D': 8},
        'D': {'A': 10, 'B': 4, 'C': 8, 'D': 0}
    }

    # Crea una instancia del ProblemaTSP con las ciudades y distancias.
    problema = ProblemaTSP(ciudades, distancias)

    # Llama a la función algoritmo_genetico para encontrar una buena ruta para el TSP.
    # Se usan los parámetros por defecto para el tamaño de población, generaciones, etc.
    # Retorna el mejor individuo (ruta) encontrado en la población final y su fitness (el negativo de la distancia).
    mejor_ruta, mejor_val = algoritmo_genetico(problema)

    # Imprime la mejor ruta encontrada por el Algoritmo Genético.
    print("Mejor ruta:", mejor_ruta)
    # Imprime la distancia total de la mejor ruta (negando el valor de fitness para obtener la distancia positiva).
    print("Distancia total:", -mejor_val)