import random # Importa la librería 'random', que proporciona funciones para generar números aleatorios y realizar selecciones aleatorias. Se usa aquí para barajar la ruta inicial del TSP.

# Define la función que implementa el algoritmo de búsqueda local "Hill Climbing" (Ascenso de Colina).
# Hill Climbing es un algoritmo iterativo que busca un estado mejor que el actual en su vecindario
# y se mueve a él, deteniéndose cuando no encuentra un vecino mejor (alcanzando un máximo local).
# Recibe:
# - problema: Un objeto que define el problema de optimización. Debe tener los métodos:
#   - valor(estado): Retorna el "valor" o "fitness" (un número) del estado dado. Hill Climbing busca maximizar este valor.
#   - vecinos(estado): Retorna una lista de estados vecinos del estado dado.
# - estado_inicial: El estado desde el cual comienza la búsqueda.
# - max_iter: El número máximo de iteraciones a realizar. Un límite para evitar bucles infinitos si el espacio de búsqueda es complejo o si no se alcanza un máximo local rápidamente.
def hill_climbing(problema, estado_inicial, max_iter=1000):
    # Inicializa el estado actual a ser el estado inicial proporcionado.
    actual = estado_inicial
    # Calcula el valor del estado inicial utilizando el método 'valor' del objeto 'problema'.
    valor_actual = problema.valor(actual)

    # Bucle principal del algoritmo. Se ejecuta hasta 'max_iter' veces.
    # El underscore '_' indica que no nos interesa el valor del contador del bucle.
    for _ in range(max_iter):
        # Genera la lista de estados vecinos del estado 'actual' utilizando el método 'vecinos' del objeto 'problema'.
        vecinos = problema.vecinos(actual)
        # Si no hay vecinos (el estado actual no tiene transiciones a otros estados), la búsqueda se detiene.
        if not vecinos: break # Sin vecinos, se detiene

        # Inicializa variables para rastrear el mejor vecino encontrado en la iteración actual.
        # mejor_vecino se inicializa a None.
        mejor_vecino = None
        # mejor_valor se inicializa a menos infinito. Esto asegura que cualquier valor de un vecino real
        # será mayor, permitiendo encontrar correctamente el primer mejor vecino. Se inicializa así porque buscamos MAXIMIZAR el valor.
        mejor_valor = -float('inf') # Para maximizar

        # Itera sobre cada vecino generado.
        for vecino in vecinos:
            # Calcula el valor del vecino actual utilizando el método 'valor' del objeto 'problema'.
            v = problema.valor(vecino)
            # Compara el valor del vecino actual con el mejor valor encontrado hasta ahora en esta iteración.
            if v > mejor_valor:
                # Si el valor del vecino actual es mejor, lo registra como el mejor vecino encontrado hasta ahora.
                mejor_vecino = vecino
                # Actualiza el mejor valor encontrado hasta ahora.
                mejor_valor = v

        # --- Condición de parada del Hill Climbing ---
        # Después de evaluar todos los vecinos, compara el mejor valor encontrado entre los vecinos
        # con el valor del estado actual.
        if mejor_valor <= valor_actual: break # No mejora, fin
        # Si el mejor vecino NO mejora estrictamente el valor actual (es igual o peor),
        # significa que hemos alcanzado un "máximo local" o una "meseta" donde no hay un paso ascendente.
        # En este punto, el algoritmo se detiene (rompe el bucle).

        # Si se encontró un mejor vecino (es decir, mejor_valor > valor_actual):
        # Actualiza el estado 'actual' al mejor vecino encontrado.
        actual = mejor_vecino
        # Actualiza el 'valor_actual' al valor del mejor vecino.
        valor_actual = mejor_valor

    # Una vez que el bucle termina (ya sea por alcanzar max_iter o por no encontrar un mejor vecino),
    # retorna el último estado 'actual' y su 'valor_actual' (que corresponden al máximo local encontrado o al mejor estado al finalizar las iteraciones).
    return actual, valor_actual

# Define una clase para modelar el Problema del Viajante (TSP) para que sea compatible con el algoritmo Hill Climbing.
# TSP busca encontrar la ruta más corta que visita cada ciudad exactamente una vez y regresa a la ciudad de inicio.
class ProblemaTSP:
    # Método constructor de la clase. Se ejecuta al crear una instancia ProblemaTSP.
    # Recibe la lista de ciudades y un diccionario de distancias entre ciudades.
    def __init__(self, ciudades, distancias):
        # Almacena la lista de ciudades.
        self.ciudades = ciudades
        # Almacena el diccionario de distancias. Se espera que sea {ciudad1: {ciudad2: distancia, ...}, ...}.
        self.distancias = distancias

    # Método para calcular el "valor" de una ruta dada.
    # En TSP, queremos minimizar la distancia total. Como Hill Climbing maximiza,
    # calculamos la distancia total y retornamos su negativo para que maximizar el negativo
    # sea equivalente a minimizar la distancia.
    def valor(self, ruta):
        # Calcula la suma de las distancias entre ciudades consecutivas en la ruta.
        # Itera desde la primera ciudad hasta la penúltima (índices 0 a len(ruta)-2).
        # self.distancias[ruta[i]][ruta[i+1]] accede a la distancia de la ciudad en la posición i a la ciudad en la posición i+1.
        total = sum(self.distancias[ruta[i]][ruta[i+1]] for i in range(len(ruta)-1))
        # Suma la distancia de la última ciudad de la ruta de vuelta a la ciudad de inicio (para completar el ciclo).
        total += self.distancias[ruta[-1]][ruta[0]]  # Vuelta al inicio
        # Retorna el negativo de la distancia total.
        return -total  # Negativo para usarlo como maximización (maximizar -distancia es minimizar distancia)

    # Método para generar los estados vecinos de una ruta dada.
    # Una estrategia común para generar vecinos en TSP es el "intercambio de 2-opt":
    # intercambiar la posición de dos ciudades cualesquiera en la ruta.
    def vecinos(self, ruta):
        # Inicializa una lista vacía para almacenar los vecinos generados.
        vecinos = []
        # Itera sobre todos los pares posibles de índices (i, j) en la ruta, donde i < j.
        for i in range(len(ruta)):
            for j in range(i+1, len(ruta)): # j empieza en i+1 para considerar pares distintos y evitar duplicados.
                # Crea una copia de la ruta actual para no modificar la ruta original.
                vecino = ruta.copy()
                # Intercambia las ciudades en las posiciones i y j.
                vecino[i], vecino[j] = vecino[j], vecino[i]  # Intercambio (operación 2-opt simple)
                # Añade la nueva ruta (el vecino) a la lista de vecinos.
                vecinos.append(vecino)
        # Retorna la lista de todos los vecinos generados por el intercambio de 2-opt.
        return vecinos

# Este bloque de código se ejecuta solo cuando el script se corre directamente.
# Contiene un ejemplo de cómo usar el algoritmo Hill Climbing con el ProblemaTSP.
if __name__ == "__main__":
    # Define la lista de ciudades.
    ciudades = ['A', 'B', 'C', 'D']
    # Define la matriz de distancias entre ciudades como un diccionario de diccionarios.
    # distancias[ciudad_origen][ciudad_destino] da la distancia.
    # Este ejemplo usa una matriz asimétrica (distancia de A a B no es igual a la de B a A).
    distancias = {
        'A': {'A': 0, 'B': 2, 'C': 9, 'D': 10},
        'B': {'A': 1, 'B': 0, 'C': 6, 'D': 4},
        'C': {'A': 15, 'B': 7, 'C': 0, 'D': 8},
        'D': {'A': 6, 'B': 3, 'C': 12, 'D': 0}
    }

    # Crea una instancia del ProblemaTSP con las ciudades y distancias definidas.
    problema = ProblemaTSP(ciudades, distancias)

    # Crea una ruta inicial copiando la lista de ciudades.
    ruta_inicial = ciudades.copy()
    # Baraja aleatoriamente la lista de ciudades para obtener una ruta inicial al azar.
    random.shuffle(ruta_inicial)

    # Llama a la función hill_climbing para encontrar una mejor ruta partiendo de la ruta inicial.
    # La función retorna el mejor estado (ruta) encontrado y su valor (el negativo de la longitud).
    mejor_ruta, mejor_valor = hill_climbing(problema, ruta_inicial)

    # Imprime la ruta inicial generada aleatoriamente.
    print("Ruta inicial:", ruta_inicial)
    # Calcula e imprime la longitud de la ruta inicial (negando el valor para obtener la distancia positiva).
    print("Longitud inicial:", -problema.valor(ruta_inicial))

    # Imprime la mejor ruta encontrada por el algoritmo Hill Climbing.
    print("Mejor ruta:", mejor_ruta)
    # Imprime la longitud de la mejor ruta encontrada (negando el valor retornado por Hill Climbing).
    print("Longitud óptima:", -mejor_valor)