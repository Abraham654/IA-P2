import numpy as np

# Importamos la biblioteca numpy para trabajar con matrices y cálculos numéricos

# Definimos una clase para modelar un Proceso de Markov
class ProcesoMarkov:
    def __init__(self, estados, matriz_transicion):
        # Lista de estados posibles
        self.estados = estados
        # Matriz de transición de probabilidades entre estados
        self.matriz_transicion = np.array(matriz_transicion)
        # Estado actual del sistema, inicializado al primer estado
        self.estado_actual = 0

    def siguiente_estado(self):
        # Obtenemos las probabilidades de transición desde el estado actual
        probabilidades = self.matriz_transicion[self.estado_actual]
        # Elegimos el siguiente estado basado en las probabilidades
        self.estado_actual = np.random.choice(len(self.estados), p=probabilidades)
        # Retornamos el nuevo estado
        return self.estados[self.estado_actual]

    def simular(self, pasos):
        # Lista para almacenar la secuencia de estados simulados
        secuencia = [self.estados[self.estado_actual]]
        # Iteramos por el número de pasos deseados
        for _ in range(pasos):
            # Calculamos el siguiente estado y lo añadimos a la secuencia
            secuencia.append(self.siguiente_estado())
        # Retornamos la secuencia completa de estados
        return secuencia

# Definimos los estados del sistema
estados = ["Soleado", "Nublado", "Lluvioso"]

# Definimos la matriz de transición (probabilidades entre estados)
# Cada fila representa un estado actual, y las columnas las probabilidades de transición
matriz_transicion = [
    [0.8, 0.15, 0.05],  # Probabilidades desde "Soleado"
    [0.2, 0.6, 0.2],    # Probabilidades desde "Nublado"
    [0.25, 0.25, 0.5]   # Probabilidades desde "Lluvioso"
]

# Creamos una instancia del Proceso de Markov con los estados y la matriz de transición
proceso = ProcesoMarkov(estados, matriz_transicion)

# Simulamos el proceso por 10 pasos y mostramos la secuencia de estados
secuencia_simulada = proceso.simular(10)
print("Secuencia simulada de estados:", secuencia_simulada)