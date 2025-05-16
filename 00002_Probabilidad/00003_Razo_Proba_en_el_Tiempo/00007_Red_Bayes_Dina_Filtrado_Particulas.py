# Importamos las librerías necesarias
import numpy as np  # Para operaciones numéricas
import random       # Para muestreo aleatorio

# Definimos el número de partículas
NUM_PARTICULAS = 1000

# Definimos el espacio de estados posibles (ejemplo: 0 = falso, 1 = verdadero)
ESTADOS = [0, 1]

# Definimos la función de transición de estado P(X_t | X_{t-1})
def transicion_estado(estado_anterior):
    # Ejemplo: 80% de permanecer igual, 20% de cambiar
    if random.random() < 0.8:
        return estado_anterior
    else:
        return 1 - estado_anterior

# Definimos la función de verosimilitud P(evidencia | estado)
def verosimilitud(evidencia, estado):
    # Ejemplo: sensor tiene 90% de precisión
    if evidencia == estado:
        return 0.9
    else:
        return 0.1

# Inicializamos las partículas aleatoriamente
particulas = [random.choice(ESTADOS) for _ in range(NUM_PARTICULAS)]

# Definimos una secuencia de evidencias observadas (ejemplo)
evidencias = [1, 0, 1, 1, 0]

# Iteramos sobre cada evidencia (cada paso de tiempo)
for t, evidencia in enumerate(evidencias):
    # Paso 1: Predicción - propagamos cada partícula según el modelo de transición
    particulas = [transicion_estado(p) for p in particulas]

    # Paso 2: Pesado - calculamos el peso de cada partícula según la evidencia observada
    pesos = [verosimilitud(evidencia, p) for p in particulas]

    # Normalizamos los pesos para que sumen 1
    suma_pesos = sum(w for w in pesos)
    pesos = [w / suma_pesos for w in pesos]

    # Paso 3: Remuestreo - seleccionamos nuevas partículas según los pesos
    indices = np.random.choice(range(NUM_PARTICULAS), size=NUM_PARTICULAS, p=pesos)
    particulas = [particulas[i] for i in indices]

    # Estimamos la creencia actual (probabilidad de cada estado)
    prob_0 = particulas.count(0) / NUM_PARTICULAS
    prob_1 = particulas.count(1) / NUM_PARTICULAS

    # Mostramos la estimación en este paso de tiempo
    print(f"Tiempo {t+1}: P(estado=0)={prob_0:.2f}, P(estado=1)={prob_1:.2f}")

# Fin del filtrado de partículas para una Red Bayesiana Dinámica