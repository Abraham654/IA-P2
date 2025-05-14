import random # Importa la librería 'random', usada para generar números aleatorios. Se utiliza aquí para generar estados iniciales aleatorios y para generar vecinos aleatorios en el problema de ejemplo (ProblemaFuncion).
import heapq # Importa la librería 'heapq', que proporciona funciones para implementar colas de prioridad (heaps). Se usa aquí para seleccionar eficientemente los k mejores estados y vecinos.

# Define la función que implementa el algoritmo de Búsqueda de Haz Local (Local Beam Search).
# Este algoritmo es una variante de búsqueda local que mantiene un "haz" (beam) de k estados en lugar de solo uno.
# En cada paso, genera todos los vecinos de todos los estados en el haz, evalúa a todos estos vecinos y selecciona los k mejores para formar el nuevo haz.
# Recibe:
# - problema: Un objeto que define el problema. Debe tener los métodos:
#   - valor(estado): Retorna el valor del estado (para maximizar).
#   - generar_vecinos(estado): Retorna una lista de estados vecinos del estado dado.
# - estados_iniciales: Una lista de k estados desde los cuales comienza la búsqueda.
# - k: El tamaño del haz (el número de estados que se mantienen en cada iteración).
# - max_iter: El número máximo de iteraciones a realizar.
def local_beam_search(problema, estados_iniciales, k=5, max_iter=1000):
    # Crea el haz inicial. Es una lista de tuplas donde cada tupla contiene el valor del estado y el estado mismo: (valor, estado).
    # Esto es necesario porque heapq ordena por el primer elemento de la tupla (el valor).
    haz = [(problema.valor(e), e) for e in estados_iniciales]

    # Convierte la lista 'haz' en una estructura de heap in-place. Aunque nlargest puede trabajar con cualquier iterable,
    # heapify lo prepara, aunque no es estrictamente necesario antes de nlargest.
    heapq.heapify(haz) # Ordenar por valor (prepara la lista como un heap)

    # Selecciona los k estados con los valores más altos (los k mejores) del haz inicial.
    # heapq.nlargest(k, iterable) retorna una lista de los k elementos más grandes del iterable.
    # Esto asegura que el haz inicial contenga los k mejores de la lista de estados_iniciales.
    haz = heapq.nlargest(k, haz) # Quedarse con los k mejores (el haz inicial)

    # Bucle principal del algoritmo. Se ejecuta hasta 'max_iter' veces.
    for _ in range(max_iter):
        # Inicializa una lista vacía para almacenar TODOS los vecinos generados a partir de todos los estados en el haz actual.
        vecinos = []
        # Itera sobre cada tupla (valor, estado) en el haz actual.
        # Ignoramos el valor (_) ya que solo necesitamos el estado para generar vecinos.
        for _, estado in haz:
            # Itera sobre cada vecino generado para el estado actual del haz.
            for v in problema.generar_vecinos(estado):
                # Para cada vecino 'v', calcula su valor y lo añade a la lista 'vecinos' como una tupla (valor, vecino).
                vecinos.append((problema.valor(v), v))

        # Si no se generó ningún vecino (por ejemplo, si generar_vecinos retornó una lista vacía para todos los estados),
        # la búsqueda se detiene.
        if not vecinos: break # Si no hay vecinos, se detiene

        # Selecciona los k mejores vecinos de la lista completa de todos los vecinos generados.
        # Estos k mejores vecinos formarán el haz para la siguiente iteración.
        nuevo_haz = heapq.nlargest(k, vecinos)

        # --- Condición de parada ---
        # Comprueba si el valor del mejor estado en el nuevo haz (nuevo_haz[0][0])
        # es igual al valor del mejor estado en el haz actual (haz[0][0]).
        # heapq.nlargest retorna la lista ordenada de mayor a menor, por lo que el mejor valor está en el primer elemento [0][0].
        if nuevo_haz[0][0] == haz[0][0]: break # Si no mejora (el mejor valor no aumenta), se detiene

        # Si el mejor valor mejoró (o se mantuvo igual pero hay otros estados mejores en el haz),
        # actualiza el haz actual para que sea el nuevo haz de los k mejores vecinos.
        haz = nuevo_haz # Actualiza el haz para la próxima iteración

    # Una vez que el bucle termina, retorna el mejor estado encontrado y su valor.
    # El mejor estado está en el primer elemento del haz final (haz[0]), y el estado es el segundo elemento de la tupla [1],
    # mientras que el valor es el primer elemento de la tupla [0].
    return haz[0][1], haz[0][0] # Mejor estado (haz[0][1]) y su valor (haz[0][0])

# Define una clase de ejemplo para un problema de optimización de funciones continuas.
# El "estado" es un número (valor de x) y el "valor" es el resultado de evaluar una función f(x).
# El objetivo es maximizar f(x).
class ProblemaFuncion:
    # Método constructor. Almacena la función objetivo que se desea maximizar.
    def __init__(self, funcion):
        self.funcion = funcion # La función a evaluar, f(x).

    # Método para calcular el "valor" de un estado (un valor de x).
    # Simplemente evalúa la función objetivo en el estado dado.
    def valor(self, x):
        return self.funcion(x) # Evalúa f(x)

    # Método para generar estados vecinos de un estado dado (un valor de x).
    # Para un problema continuo, los vecinos se generan añadiendo una pequeña perturbación aleatoria.
    def generar_vecinos(self, x, paso=0.1):
        # Genera una lista de 10 vecinos.
        # Cada vecino es el estado original 'x' más un número aleatorio uniforme entre -paso y +paso.
        return [x + random.uniform(-paso, paso) for _ in range(10)] # Genera 10 vecinos perturbando x

# Este bloque de código solo se ejecuta cuando el script se corre directamente.
# Contiene un ejemplo de cómo usar el algoritmo Local Beam Search para maximizar una función.
if __name__ == "__main__":
    # Define la función objetivo que queremos maximizar: f(x) = -x^2 + 1.2*x.
    # Esta es una parábola que abre hacia abajo, su máximo está en el vértice (derivada = 0: -2x + 1.2 = 0 => x = 0.6).
    def funcion_obj(x): return -x**2 + 1.2*x # Máximo cerca de x ≈ 0.6

    # Crea una instancia del ProblemaFuncion con la función objetivo.
    problema = ProblemaFuncion(funcion_obj)

    # Define el tamaño del haz (k).
    k = 3
    # Genera una lista de k estados iniciales aleatorios, cada uno es un número flotante entre -10 y 10.
    estados = [random.uniform(-10, 10) for _ in range(k)]

    # Llama a la función local_beam_search con el problema, los estados iniciales y el tamaño del haz k.
    # Retorna el mejor estado (valor de x) encontrado en el haz final y su valor de función f(x).
    mejor_x, mejor_valor = local_beam_search(problema, estados, k=k)

    # Imprime los estados iniciales utilizados.
    print("Estados iniciales:", estados)
    # Imprime el mejor estado (valor de x) y su valor de función (f(x)) encontrados por el algoritmo, formateados a 4 decimales.
    print(f"Mejor solución: x = {mejor_x:.4f}, f(x) = {mejor_valor:.4f}")