import random

# Definimos una variable aleatoria: Diagnóstico = {Enfermo, Sano}
valores_diagnostico = ['Enfermo', 'Sano']

# Asignamos la probabilidad a priori: P(Enfermo) = 0.1, P(Sano) = 0.9
# Estas probabilidades representan conocimiento previo antes de cualquier evidencia
prob_apriori = {
    'Enfermo': 0.1,
    'Sano': 0.9
}

# Mostramos la distribución a priori
print("Distribución a priori P(Diagnóstico):")
for estado, prob in prob_apriori.items():
    print(f"{estado}: {prob:.2f}")

# Simulamos 1000 muestras basadas en la distribución a priori
muestras = random.choices(
    population=list(prob_apriori.keys()),  # posibles valores
    weights=list(prob_apriori.values()),   # probabilidades asociadas
    k=1000                                 # número de muestras
)

# Contamos la frecuencia observada de cada estado
conteo = {estado: muestras.count(estado) for estado in valores_diagnostico}

# Mostramos frecuencias observadas
print("\nFrecuencias observadas (aproximación experimental):")
for estado in valores_diagnostico:
    frecuencia = conteo[estado] / len(muestras)  # estimación relativa
    print(f"{estado}: {frecuencia:.3f}")

# Aplicamos la regla de probabilidad total
# Supongamos que P(Positivo | Enfermo) = 0.95, P(Positivo | Sano) = 0.05
# Calculamos P(Positivo) = Σ P(Positivo | Diagnóstico) * P(Diagnóstico)
prob_condicional = {
    'Enfermo': 0.95,
    'Sano': 0.05
}

# Probabilidad total de un resultado positivo antes de observar evidencia
p_positivo = sum(prob_condicional[estado] * prob_apriori[estado] for estado in valores_diagnostico)

print(f"\nP(Resultado positivo) (por probabilidad total): {p_positivo:.4f}")
