import random # Importa la librería 'random', usada para generar la solución inicial aleatoria para el problema de la mochila.
from collections import deque # Importa 'deque' del módulo 'collections'. 'deque' (double-ended queue) es eficiente para añadir y eliminar elementos de ambos extremos, lo que la hace ideal para implementar la lista tabú de tamaño fijo.

# Define la función que implementa el algoritmo de búsqueda local "Tabu Search" (Búsqueda Tabú).
# Tabu Search es una metaheurística que mejora Hill Climbing al usar una "lista tabú" de movimientos o estados
# recientemente visitados para evitar quedar atrapado en óptimos locales.
# Recibe:
# - problema: Un objeto que define el problema de optimización (debe tener métodos valor() y vecinos()).
# - estado_inicial: El estado desde el cual comienza la búsqueda.
# - max_iter: El número máximo de iteraciones a realizar.
# - tamano_tabu: El tamaño máximo de la lista tabú. Los elementos más antiguos se eliminan automáticamente.
def tabu_search(problema, estado_inicial, max_iter=1000, tamano_tabu=10):
    # Inicializa el estado 'actual' de la búsqueda al estado inicial.
    actual = estado_inicial
    # Inicializa el 'mejor_estado' global encontrado hasta ahora (puede ser diferente del 'actual').
    mejor_estado = actual
    # Calcula el valor del estado inicial y lo almacena como el 'mejor_valor' global encontrado hasta ahora.
    mejor_valor = problema.valor(actual)

    # Inicializa la lista tabú usando un deque con un tamaño máximo fijo ('maxlen').
    # Cuando se añade un nuevo elemento y la lista ya alcanzó su tamaño máximo, el elemento más antiguo se elimina automáticamente del otro extremo.
    # Almacenará los estados (o a veces los movimientos que llevaron a esos estados) que no se pueden visitar temporalmente.
    lista_tabu = deque(maxlen=tamano_tabu) # Lista tabú con tamaño fijo

    # Bucle principal del algoritmo Tabu Search. Se ejecuta hasta 'max_iter' veces.
    for _ in range(max_iter):
        # Genera la lista de estados vecinos del estado 'actual' utilizando el método 'vecinos' del objeto 'problema'.
        vecinos = problema.vecinos(actual)
        # Si no hay vecinos (el estado actual no tiene transiciones), la búsqueda se detiene.
        if not vecinos: break

        # Inicializa variables para encontrar el mejor vecino *no tabú* en esta iteración.
        # mejor_vecino se inicializa a None.
        mejor_vecino = None
        # mejor_valor_vecino se inicializa a menos infinito para encontrar el máximo valor.
        mejor_valor_vecino = -float('inf')

        # Comentario que describe el propósito del siguiente bucle.
        # Selecciona mejor vecino no tabú
        # Itera sobre cada vecino generado.
        for vecino in vecinos:
            # --- Regla Tabú ---
            # Comprueba si el vecino actual NO está en la lista tabú.
            if vecino not in lista_tabu:
                # Si el vecino no es tabú, calcula su valor.
                val = problema.valor(vecino)
                # Compara el valor del vecino actual con el mejor valor encontrado hasta ahora entre los vecinos no tabú.
                if val > mejor_valor_vecino:
                    # Si el valor del vecino actual es mejor, lo registra como el mejor vecino NO tabú.
                    mejor_vecino = vecino
                    # Actualiza el mejor valor encontrado entre los vecinos no tabú.
                    mejor_valor_vecino = val

        # --- Regla de Aspiración Simplificada (implícita) o Manejo de Estancamiento ---
        # Comprueba si no se encontró ningún vecino NO tabú (mejor_vecino sigue siendo None).
        # Esto ocurre si todos los vecinos generados están actualmente en la lista tabú.
        if mejor_vecino is None:
             # Si todos los vecinos son tabú, seleccionamos el mejor vecino *de todos* los vecinos generados,
             # ignorando su estado tabú. Esta es una forma simple de intentar escapar si todos los movimientos posibles
             # son temporalmente prohibidos. Una regla de aspiración completa permitiría un movimiento tabú solo si
             # lleva a un estado mejor que el mejor global encontrado hasta ahora.
             mejor_vecino = max(vecinos, key=problema.valor)
             # Obtiene el valor de este vecino seleccionado (que podría ser tabú).
             mejor_valor_vecino = problema.valor(mejor_vecino)

        # Actualiza el estado 'actual' al mejor vecino seleccionado en esta iteración (sea tabú o no, dependiendo de la lógica anterior).
        actual = mejor_vecino
        # --- Gestión de la Lista Tabú ---
        # Añade el estado 'actual' (el estado al que nos movemos) a la lista tabú.
        # Si la lista ya está llena (tamaño == tamano_tabu), el elemento más antiguo se elimina automáticamente.
        lista_tabu.append(actual) # Agrega a la lista tabú

        # Comprueba si el valor del estado actual es mejor que el mejor valor global encontrado hasta ahora.
        if mejor_valor_vecino > mejor_valor:
            # Si es mejor, actualiza el mejor estado global y su valor.
            mejor_estado = mejor_vecino
            mejor_valor = mejor_valor_vecino

    # Una vez que el bucle principal termina (por alcanzar max_iter o quedarse sin vecinos),
    # retorna el mejor estado global encontrado ('mejor_estado') y su valor ('mejor_valor').
    return mejor_estado, mejor_valor

# Define una clase para modelar el Problema de la Mochila (Knapsack Problem) para usar con Tabu Search.
# Dado un conjunto de ítems, cada uno con un valor y un peso, y una capacidad máxima para la mochila,
# el objetivo es seleccionar un subconjunto de ítems para maximizar el valor total sin exceder la capacidad.
class ProblemaMochila:
    # Método constructor.
    # Recibe la lista de ítems (cada uno como una tupla (valor, peso)) y la capacidad máxima de la mochila.
    def __init__(self, items, capacidad):
        # Almacena la lista de ítems. Se espera formato [(valor1, peso1), (valor2, peso2), ...].
        self.items = items          # (valor, peso)
        # Almacena la capacidad máxima.
        self.capacidad = capacidad

    # Método para calcular el "valor" de una solución dada.
    # Una solución es una lista (o tupla) binaria donde el elemento i es 1 si el ítem i está incluido en la mochila, y 0 si no.
    def valor(self, solucion):
        # Inicializa el valor total y el peso total de la solución.
        val, peso = 0, 0
        # Itera sobre la solución con el índice (i) y el estado (usar: 0 o 1) de cada ítem.
        for i, usar in enumerate(solucion):
            # Si el estado es 1 (el ítem está incluido en la mochila).
            if usar:
                # Suma el valor del ítem al valor total.
                val += self.items[i][0]
                # Suma el peso del ítem al peso total.
                peso += self.items[i][1]
        # --- Función de Evaluación ---
        # Retorna el valor total SI el peso total no excede la capacidad de la mochila.
        # Si el peso excede la capacidad, retorna 0 (o un valor bajo de penalización) para indicar que es una solución inválida.
        return val if peso <= self.capacidad else 0

    # Método para generar los estados vecinos de una solución dada.
    # Para problemas binarios como la mochila, una forma común de generar vecinos es "flipping a bit":
    # crear nuevas soluciones cambiando el estado de un solo ítem (de 0 a 1 o de 1 a 0).
    def vecinos(self, solucion):
        # Inicializa una lista vacía para almacenar los vecinos generados.
        vecinos = []
        # Itera sobre el índice de cada ítem en la solución.
        for i in range(len(solucion)):
            # Crea una copia de la solución actual. Es crucial trabajar con copias para no modificar la solución original.
            copia = solucion.copy()
            # Cambia el estado del ítem en la posición i: si era 0, se vuelve 1; si era 1, se vuelve 0.
            copia[i] = 1 - copia[i] # Flip bit (0 se vuelve 1, 1 se vuelve 0)
            # Añade la nueva solución (el vecino) a la lista de vecinos.
            vecinos.append(copia)
        # Retorna la lista de todos los vecinos generados.
        return vecinos

# Este bloque de código solo se ejecuta cuando el script se corre directamente.
# Contiene un ejemplo de cómo usar el algoritmo Tabu Search con el Problema de la Mochila.
if __name__ == "__main__":
    # Define la lista de ítems, cada uno con su valor y peso.
    items = [(60, 10), (100, 20), (120, 30)] # item1: valor 60, peso 10; item2: valor 100, peso 20; item3: valor 120, peso 30.
    # Define la capacidad máxima de la mochila.
    capacidad = 50
    # Crea una instancia del ProblemaMochila con los ítems y la capacidad.
    problema = ProblemaMochila(items, capacidad)

    # Genera una solución inicial aleatoria como una lista de 0s y 1s, una por cada ítem.
    # random.randint(0, 1) genera un entero aleatorio que es 0 o 1.
    inicial = [random.randint(0, 1) for _ in items]

    # Llama a la función tabu_search para encontrar una mejor solución partiendo de la solución inicial.
    # La función retorna el mejor estado (solución) encontrado y su valor.
    # Se usan los valores por defecto para max_iter (1000) y tamano_tabu (10).
    mejor_sol, mejor_val = tabu_search(problema, inicial)

    # Imprime la solución inicial generada aleatoriamente y su valor.
    print("Solución inicial:", inicial)
    print("Valor inicial:", problema.valor(inicial))

    # Imprime la mejor solución encontrada por el algoritmo Tabu Search y su valor.
    print("\nMejor solución:", mejor_sol)
    print("Valor óptimo:", mejor_val)