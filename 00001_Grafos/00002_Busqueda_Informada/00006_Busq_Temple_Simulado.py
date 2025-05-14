import random # Importa la librería 'random', usada para generar números aleatorios (para seleccionar vecinos al azar) y para la parte probabilística del criterio de aceptación.
import math # Importa la librería 'math', usada para la función exponencial 'math.exp' en el cálculo de la probabilidad de aceptación de peores estados.

# Define la función que implementa el algoritmo de Recocido Simulado (Simulated Annealing).
# Este algoritmo es una metaheurística probabilística inspirada en el proceso de enfriamiento de metales (recocido).
# Permite movimientos ocasionales a peores estados para escapar de óptimos locales, con una probabilidad que disminuye a medida que "baja la temperatura".
# Recibe:
# - problema: Un objeto que define el problema de optimización. Debe tener los métodos:
#   - valor(estado): Retorna el "valor" o "fitness" del estado (para maximizar).
#   - vecino_aleatorio(estado): Retorna UN vecino seleccionado al azar del estado dado.
# - estado_inicial: El estado desde el cual comienza la búsqueda.
# - temp_inicial: La temperatura inicial del proceso de simulación. Alta al principio para permitir más exploración.
# - enfriamiento: Un factor (entre 0 y 1) por el cual se multiplica la temperatura en cada paso. Controla qué tan rápido baja la temperatura.
# - iter_por_temp: El número de intentos de movimiento (iteraciones) que se realizan a cada temperatura.
# - temp_final: La temperatura mínima a la que se detiene el proceso de simulación.
def simulated_annealing(problema, estado_inicial, temp_inicial=1000, enfriamiento=0.95, iter_por_temp=100, temp_final=0.1):
    # Inicializa el estado 'actual' al estado inicial.
    actual = estado_inicial
    # Inicializa el 'mejor_estado' global encontrado hasta ahora al estado inicial.
    mejor_estado = actual
    # Calcula el valor del estado inicial y lo almacena como el 'mejor_valor' global encontrado hasta ahora.
    mejor_valor = problema.valor(actual)
    # Inicializa la temperatura actual al valor de la temperatura inicial.
    temp = temp_inicial

    # Bucle principal del algoritmo. Continúa mientras la temperatura actual sea mayor que la temperatura final.
    # Esto simula el proceso de enfriamiento.
    while temp > temp_final:
        # Bucle interno. Se ejecuta 'iter_por_temp' veces para intentar movimientos a la temperatura actual.
        for _ in range(iter_por_temp):
            # Genera UN vecino seleccionado al azar del estado 'actual' utilizando el método 'vecino_aleatorio'.
            vecino = problema.vecino_aleatorio(actual)
            # Calcula el cambio en el valor (fitness) si nos movemos del estado actual al vecino.
            # Un delta positivo significa que el vecino es mejor; un delta negativo significa que es peor.
            delta = problema.valor(vecino) - problema.valor(actual)

            # --- Criterio de Aceptación de Metropolis ---
            # Decide si aceptar o no el movimiento al vecino.
            # 1. Si el vecino es mejor que el estado actual (delta > 0), siempre se acepta el movimiento.
            # 2. Si el vecino es peor o igual que el estado actual (delta <= 0), se acepta con una probabilidad.
            #    La probabilidad es e^(delta / temp).
            #    math.exp(delta / temp) calcula e elevado a (delta / temp).
            #    Si delta es negativo, delta / temp es negativo, y e^(negativo) es un número entre 0 y 1.
            #    random.random() genera un número aleatorio entre 0.0 y 1.0.
            #    Si el número aleatorio es menor que la probabilidad calculada, el movimiento a un estado peor es aceptado.
            if delta > 0 or random.random() < math.exp(delta / temp):
                # Si el movimiento es aceptado (ya sea porque es una mejora o por probabilidad), actualiza el estado 'actual' al vecino.
                actual = vecino

            # Después de considerar el movimiento (y actualizar 'actual' si fue aceptado),
            # comprueba si el valor del estado 'actual' es mejor que el mejor valor global encontrado hasta ahora.
            if problema.valor(actual) > mejor_valor:
                # Si es mejor, actualiza el mejor estado global y su valor.
                mejor_estado = actual
                mejor_valor = problema.valor(actual)

        # --- Esquema de Enfriamiento ---
        # Al finalizar el bucle interno (después de iter_por_temp intentos de movimiento),
        # reduce la temperatura multiplicándola por el factor de enfriamiento.
        temp *= enfriamiento # Reduce la temperatura

    # Una vez que el bucle principal termina (la temperatura ha descendido por debajo de temp_final),
    # retorna el mejor estado global encontrado ('mejor_estado') y su valor ('mejor_valor').
    return mejor_estado, mejor_valor

# Clase para modelar el Problema del Viajante (TSP), adaptada para Simulated Annealing.
# A diferencia de la versión para Hill Climbing, solo necesita generar UN vecino aleatorio por llamada.
class ProblemaTSP:
    # Método constructor. Almacena ciudades y distancias.
    def __init__(self, ciudades, distancias):
        self.ciudades = ciudades
        self.distancias = distancias # Diccionario de diccionarios: {ciudad1: {ciudad2: distancia, ...}, ...}

    # Método para calcular el "valor" de una ruta. Similar a la versión de Hill Climbing,
    # calcula la distancia total del ciclo y retorna su negativo para que la maximización funcione como minimización de distancia.
    def valor(self, ruta):
        # Suma distancias entre ciudades consecutivas.
        total = sum(self.distancias[ruta[i]][ruta[i+1]] for i in range(len(ruta)-1))
        # Suma la distancia de vuelta al inicio.
        total += self.distancias[ruta[-1]][ruta[0]] # Regresa al inicio
        # Retorna el negativo de la distancia total.
        return -total # Negativo para maximizar

    # Método para generar UN estado vecino aleatorio de una ruta.
    # Implementa el intercambio de 2-opt seleccionando dos puntos al azar y intercambiando ciudades.
    def vecino_aleatorio(self, ruta):
        # Crea una copia de la ruta actual.
        vecino = ruta.copy()
        # Selecciona dos índices distintos al azar de la longitud de la ruta.
        i, j = random.sample(range(len(ruta)), 2)
        # Intercambia las ciudades en las posiciones i y j.
        vecino[i], vecino[j] = vecino[j], vecino[i] # Swap (intercambio)
        # Retorna el vecino generado aleatoriamente.
        return vecino

# Este bloque de código se ejecuta solo cuando el script se corre directamente.
# Contiene un ejemplo de cómo usar el algoritmo Simulated Annealing con el ProblemaTSP.
if __name__ == "__main__":
    # Define la lista de ciudades.
    ciudades = ['A', 'B', 'C', 'D']
    # Define la matriz de distancias simétrica (distancia A a B es igual a B a A).
    distancias = {
        'A': {'B': 2, 'C': 9, 'D': 10},
        'B': {'A': 2, 'C': 6, 'D': 4},
        'C': {'A': 9, 'B': 6, 'D': 8},
        'D': {'A': 10, 'B': 4, 'C': 8}
    }

    # Crea una instancia del ProblemaTSP.
    problema = ProblemaTSP(ciudades, distancias)

    # Crea una ruta inicial aleatoria barajando las ciudades.
    ruta_inicial = ciudades.copy()
    random.shuffle(ruta_inicial)

    # Llama a la función simulated_annealing para encontrar una mejor ruta partiendo de la ruta inicial.
    # Utiliza los parámetros por defecto para la temperatura y enfriamiento.
    mejor_ruta, mejor_valor = simulated_annealing(problema, ruta_inicial)

    # Imprime la ruta inicial y su longitud. Nota: se usa -problema.valor(...) para mostrar la distancia positiva.
    print("Ruta inicial:", ruta_inicial, f"(Distancia: {-problema.valor(ruta_inicial)})")
    # Imprime la mejor ruta encontrada por Simulated Annealing y su longitud (usando el valor final encontrado).
    print("Mejor ruta:", mejor_ruta, f"(Distancia: {-mejor_valor})")