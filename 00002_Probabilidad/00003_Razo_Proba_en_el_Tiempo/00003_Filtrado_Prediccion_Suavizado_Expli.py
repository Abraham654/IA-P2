import numpy as np
from collections import defaultdict

# Estados ocultos posibles (ej: clima)
estados = ['Soleado', 'Lluvioso']

# Observaciones posibles (ej: si alguien lleva paraguas)
observaciones = ['Sí', 'No']

# Probabilidad inicial P(estado_0)
P_inicial = {'Soleado': 0.6, 'Lluvioso': 0.4}

# Matriz de transición P(estado_t | estado_t-1)
P_transicion = {
    'Soleado': {'Soleado': 0.7, 'Lluvioso': 0.3},
    'Lluvioso': {'Soleado': 0.4, 'Lluvioso': 0.6}
}

# Matriz de observación P(observación | estado)
P_emision = {
    'Soleado': {'Sí': 0.1, 'No': 0.9},
    'Lluvioso': {'Sí': 0.8, 'No': 0.2}
}

# Evidencia observada en el tiempo (observaciones reales)
evidencia = ['Sí', 'Sí', 'No', 'Sí']  # Secuencia observada

# FILTRADO: calcula creencia sobre el estado actual dado las observaciones pasadas
def filtrado(observaciones):
    belief = P_inicial.copy()  # Empezamos con P(estado_0)
    for obs in observaciones:
        # Predicción: P(estado_t) = sum(P(estado_t-1) * transiciones)
        nueva_belief = {}
        for estado_actual in estados:
            prob = sum(
                belief[estado_prev] * P_transicion[estado_prev][estado_actual]
                for estado_prev in estados
            )
            # Multiplicamos por la probabilidad de la observación actual
            nueva_belief[estado_actual] = P_emision[estado_actual][obs] * prob
        # Normalizar
        total = sum(nueva_belief.values())
        for estado in estados:
            nueva_belief[estado] /= total
        belief = nueva_belief  # Actualizamos creencia
    return belief

# PREDICCIÓN: estima la probabilidad del siguiente estado
def prediccion(belief_actual, pasos=1):
    for _ in range(pasos):
        nueva_belief = {}
        for estado_actual in estados:
            nueva_belief[estado_actual] = sum(
                belief_actual[estado_prev] * P_transicion[estado_prev][estado_actual]
                for estado_prev in estados
            )
        belief_actual = nueva_belief
    return belief_actual

# SUAVIZADO: calcula creencia pasada usando información futura (P(estado_k | evidencias completas))
def suavizado(observaciones):
    n = len(observaciones)
    alpha = [{} for _ in range(n)]
    beta = [{} for _ in range(n)]

    # FORWARD: calcular alpha (igual al filtrado)
    alpha[0] = {
        estado: P_inicial[estado] * P_emision[estado][observaciones[0]]
        for estado in estados
    }
    normalizar = sum(alpha[0].values())
    for estado in estados:
        alpha[0][estado] /= normalizar

    for t in range(1, n):
        for estado in estados:
            alpha[t][estado] = P_emision[estado][observaciones[t]] * sum(
                alpha[t-1][prev] * P_transicion[prev][estado]
                for prev in estados
            )
        normalizar = sum(alpha[t].values())
        for estado in estados:
            alpha[t][estado] /= normalizar

    # BACKWARD: calcular beta (probabilidad futura)
    for estado in estados:
        beta[n-1][estado] = 1.0  # Última observación

    for t in reversed(range(n - 1)):
        for estado in estados:
            beta[t][estado] = sum(
                P_transicion[estado][sig] *
                P_emision[sig][observaciones[t+1]] *
                beta[t+1][sig]
                for sig in estados
            )
        normalizar = sum(beta[t].values())
        for estado in estados:
            beta[t][estado] /= normalizar

    # Combinar alpha y beta
    resultado = []
    for t in range(n):
        prob = {}
        for estado in estados:
            prob[estado] = alpha[t][estado] * beta[t][estado]
        total = sum(prob.values())
        for estado in estados:
            prob[estado] /= total
        resultado.append(prob)
    return resultado

# EXPLICACIÓN: devuelve la secuencia de estados más probable (Viterbi)
def explicacion(observaciones):
    V = [{}]
    path = {}

    # Inicializar
    for estado in estados:
        V[0][estado] = P_inicial[estado] * P_emision[estado][observaciones[0]]
        path[estado] = [estado]

    # Dinámica
    for t in range(1, len(observaciones)):
        nuevo_path = {}
        V.append({})
        for estado in estados:
            (prob_max, estado_prev) = max(
                [(V[t-1][s] * P_transicion[s][estado] * P_emision[estado][observaciones[t]], s)
                 for s in estados]
            )
            V[t][estado] = prob_max
            nuevo_path[estado] = path[estado_prev] + [estado]
        path = nuevo_path

    # Elegir la secuencia con mayor probabilidad final
    n = len(observaciones) - 1
    (prob, estado_final) = max((V[n][estado], estado) for estado in estados)
    return path[estado_final], prob

# Ejecutar funciones
print("=== FILTRADO (última creencia) ===")
print(filtrado(evidencia))

print("\n=== PREDICCIÓN (1 paso futuro) ===")
print(prediccion(filtrado(evidencia), pasos=1))

print("\n=== SUAVIZADO (todos los pasos) ===")
for t, prob in enumerate(suavizado(evidencia)):
    print(f"Tiempo {t}: {prob}")

print("\n=== EXPLICACIÓN (secuencia más probable) ===")
secuencia, prob = explicacion(evidencia)
print(f"Secuencia: {secuencia} | Prob: {prob:.4f}")
