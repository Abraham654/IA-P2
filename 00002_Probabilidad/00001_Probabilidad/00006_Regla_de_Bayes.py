# Importamos defaultdict para manejar diccionarios con valores por defecto
from collections import defaultdict

# Definimos los valores posibles de las variables
valores = {
    'Enfermedad': ['Sí', 'No'],         # Variable hipotética: si una persona tiene enfermedad
    'Test': ['Positivo', 'Negativo']    # Resultado de un test diagnóstico
}

# Probabilidad previa de tener la enfermedad (P(Enfermedad))
P_enfermedad = {
    'Sí': 0.01,     # 1% de probabilidad de estar enfermo
    'No': 0.99      # 99% de no tener la enfermedad
}

# Probabilidades condicionales del test dado la enfermedad: P(Test | Enfermedad)
P_test_dado_enfermedad = {
    ('Positivo', 'Sí'): 0.9,    # Sensibilidad: 90% de detectar si tiene la enfermedad
    ('Negativo', 'Sí'): 0.1,
    ('Positivo', 'No'): 0.05,   # Falsos positivos: 5% de los sanos dan positivo
    ('Negativo', 'No'): 0.95
}

# Función para aplicar la Regla de Bayes: P(Enfermedad | Test)
def bayes_invertido(evidencia):
    numeradores = {}
    for enf in valores['Enfermedad']:
        # P(Enfermedad) * P(Test | Enfermedad)
        p_prior = P_enfermedad[enf]
        p_likelihood = P_test_dado_enfermedad[(evidencia, enf)]
        numeradores[enf] = p_prior * p_likelihood
    
    # Normalizamos los numeradores para obtener P(Enfermedad | Test)
    total = sum(numeradores.values())
    posteriors = {k: v / total for k, v in numeradores.items()}
    return posteriors

# Ejecutamos la inferencia para Test = Positivo
print("Aplicando Regla de Bayes para un resultado Positivo en el test:")
resultado = bayes_invertido('Positivo')

# Mostramos los resultados
for enf, prob in resultado.items():
    print(f"P(Enfermedad = {enf} | Test = Positivo) = {prob:.4f}")
