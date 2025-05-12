import random
from collections import Counter

# Espacio de estados de una variable binaria
estados = ['Sí', 'No']

# Distribución objetivo (por ejemplo: P(Lluvia))
# Queremos muestrear proporcionalmente a estos valores
distribucion_objetivo = {'Sí': 0.3, 'No': 0.7}

# Inicializamos en un estado aleatorio
estado_actual = random.choice(estados)

# Almacenar las muestras obtenidas
muestras = []

# Número de pasos de la cadena
n_iteraciones = 10000

for _ in range(n_iteraciones):
    # Proponer un nuevo estado (en este caso, otro estado distinto)
    estado_propuesto = 'Sí' if estado_actual == 'No' else 'No'

    # Calcular cociente entre la probabilidad del propuesto y el actual
    p_actual = distribucion_objetivo[estado_actual]
    p_propuesto = distribucion_objetivo[estado_propuesto]
    aceptacion = min(1, p_propuesto / p_actual)  # Regla de aceptación de Metropolis

    # Aceptar el estado propuesto con probabilidad igual al cociente
    if random.random() < aceptacion:
        estado_actual = estado_propuesto  # Aceptamos el cambio

    muestras.append(estado_actual)  # Guardamos la muestra (estado actual)

# Contar cuántas veces se visitó cada estado
conteo = Counter(muestras)

# Normalizar frecuencias para estimar probabilidad
estimacion = {estado: conteo[estado] / n_iteraciones for estado in estados}

# Mostrar resultado
print("Estimación de P(Lluvia) usando MCMC:")
for estado in estados:
    print(f"P(Lluvia = {estado}) ≈ {estimacion[estado]:.4f}")
