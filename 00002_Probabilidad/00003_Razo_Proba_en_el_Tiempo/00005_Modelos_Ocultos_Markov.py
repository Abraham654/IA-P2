# Importamos las bibliotecas necesarias
import numpy as np  # Para trabajar con matrices y operaciones matemáticas
import random  # Para generar números aleatorios

# Definimos los estados ocultos del modelo
states = ['Soleado', 'Lluvioso']  # Estados posibles del clima
n_states = len(states)  # Número de estados

# Definimos las observaciones posibles
observations = ['Caminar', 'Comprar', 'Limpiar']  # Actividades observadas
n_observations = len(observations)  # Número de observaciones

# Definimos la matriz de transición de estados (probabilidades de pasar de un estado a otro)
transition_matrix = np.array([
    [0.8, 0.2],  # Probabilidades de transición desde "Soleado"
    [0.4, 0.6]   # Probabilidades de transición desde "Lluvioso"
])

# Definimos la matriz de emisión (probabilidades de observar una actividad dado un estado)
emission_matrix = np.array([
    [0.6, 0.3, 0.1],  # Probabilidades de observaciones desde "Soleado"
    [0.1, 0.4, 0.5]   # Probabilidades de observaciones desde "Lluvioso"
])

# Definimos la distribución inicial de estados (probabilidades iniciales de cada estado)
initial_distribution = np.array([0.7, 0.3])  # Probabilidad de iniciar en "Soleado" o "Lluvioso"

# Función para generar una secuencia de estados y observaciones
def generate_sequence(length):
    sequence_states = []  # Lista para almacenar los estados generados
    sequence_observations = []  # Lista para almacenar las observaciones generadas

    # Seleccionamos el primer estado basado en la distribución inicial
    current_state = np.random.choice(states, p=initial_distribution)
    sequence_states.append(current_state)  # Agregamos el estado inicial a la secuencia

    # Generamos la secuencia de estados y observaciones
    for _ in range(length):
        # Generamos una observación basada en el estado actual
        state_index = states.index(current_state)  # Índice del estado actual
        observation = np.random.choice(observations, p=emission_matrix[state_index])
        sequence_observations.append(observation)  # Agregamos la observación a la secuencia

        # Generamos el siguiente estado basado en la matriz de transición
        current_state = np.random.choice(states, p=transition_matrix[state_index])
        sequence_states.append(current_state)  # Agregamos el nuevo estado a la secuencia

    return sequence_states, sequence_observations  # Retornamos las secuencias generadas

# Función para calcular la probabilidad de una secuencia de observaciones usando el algoritmo Forward
def forward_algorithm(obs_sequence):
    T = len(obs_sequence)  # Longitud de la secuencia de observaciones
    alpha = np.zeros((T, n_states))  # Matriz para almacenar las probabilidades forward

    # Paso de inicialización
    for i in range(n_states):
        alpha[0, i] = initial_distribution[i] * emission_matrix[i, observations.index(obs_sequence[0])]

    # Paso de inducción
    for t in range(1, T):
        for j in range(n_states):
            alpha[t, j] = sum(alpha[t-1, i] * transition_matrix[i, j] for i in range(n_states)) * \
                          emission_matrix[j, observations.index(obs_sequence[t])]

    # Paso de terminación
    return sum(alpha[T-1, :])  # Retornamos la probabilidad total de la secuencia

# Generamos una secuencia de ejemplo
sequence_length = 5  # Longitud de la secuencia
states_seq, obs_seq = generate_sequence(sequence_length)

# Mostramos las secuencias generadas
print("Secuencia de estados:", states_seq)
print("Secuencia de observaciones:", obs_seq)

# Calculamos la probabilidad de la secuencia de observaciones
probability = forward_algorithm(obs_seq)
print("Probabilidad de la secuencia de observaciones:", probability)