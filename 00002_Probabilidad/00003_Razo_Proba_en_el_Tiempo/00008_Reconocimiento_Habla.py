# Importamos las librerías necesarias
import numpy as np  # Para operaciones numéricas
import matplotlib.pyplot as plt  # Para graficar resultados

# Definimos los posibles estados ocultos (palabras o fonemas)
states = ['silencio', 'hola', 'adios']

# Definimos las posibles observaciones (características acústicas discretizadas)
observations = ['bajo', 'medio', 'alto']

# Definimos la matriz de transición de estados (probabilidad de pasar de un estado a otro)
transition_prob = np.array([
    [0.7, 0.2, 0.1],  # De silencio a otros estados
    [0.1, 0.8, 0.1],  # De hola a otros estados
    [0.2, 0.2, 0.6]   # De adios a otros estados
])

# Definimos la matriz de emisión (probabilidad de observar una característica dado un estado)
emission_prob = np.array([
    [0.8, 0.15, 0.05],  # Silencio
    [0.1, 0.7, 0.2],    # Hola
    [0.05, 0.2, 0.75]   # Adios
])

# Definimos la distribución inicial de estados
initial_prob = np.array([0.6, 0.2, 0.2])

# Secuencia de observaciones simuladas (por ejemplo, características acústicas extraídas)
obs_sequence = ['bajo', 'medio', 'alto', 'alto', 'medio']

# Convertimos las observaciones a índices
obs_idx = [observations.index(obs) for obs in obs_sequence]

# Inicializamos la matriz de creencias (forward algorithm)
T = len(obs_sequence)  # Longitud de la secuencia
N = len(states)        # Número de estados
alpha = np.zeros((T, N))  # Matriz para almacenar las probabilidades

# Paso de inicialización: calculamos la probabilidad inicial para cada estado
for s in range(N):
    alpha[0, s] = initial_prob[s] * emission_prob[s, obs_idx[0]]

# Paso de recursión: actualizamos las creencias para cada tiempo y estado
for t in range(1, T):
    for s in range(N):
        # Suma de probabilidades de llegar al estado s desde todos los estados anteriores
        alpha[t, s] = np.sum(alpha[t-1, :] * transition_prob[:, s]) * emission_prob[s, obs_idx[t]]

# Normalizamos las probabilidades en cada paso de tiempo
alpha = alpha / alpha.sum(axis=1, keepdims=True)

# Mostramos la probabilidad de cada estado en cada tiempo
for t in range(T):
    print(f"Tiempo {t+1}:")
    for s in range(N):
        print(f"  P({states[s]} | observaciones) = {alpha[t, s]:.3f}")

# Graficamos la evolución de las creencias en el tiempo
plt.figure(figsize=(8, 4))
for s in range(N):
    plt.plot(range(1, T+1), alpha[:, s], label=states[s])
plt.xlabel('Tiempo')
plt.ylabel('Probabilidad')
plt.title('Evolución de la creencia sobre los estados ocultos')
plt.legend()
plt.show()