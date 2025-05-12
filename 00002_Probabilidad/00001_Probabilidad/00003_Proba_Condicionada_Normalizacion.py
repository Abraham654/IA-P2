# Supongamos el escenario médico: variable "Enfermedad" y prueba "Resultado"
# Queremos calcular P(Enfermedad | Resultado=Positivo)

# Definimos la probabilidad a priori de Enfermedad
p_enfermedad = 0.1              # P(Enfermedad)
p_no_enfermedad = 0.9           # P(NoEnfermedad)

# Definimos las probabilidades condicionales de la prueba
p_positivo_dado_enfermedad = 0.95    # P(Positivo | Enfermedad)
p_positivo_dado_no = 0.05            # P(Positivo | NoEnfermedad)

# Usamos la regla de la probabilidad total para obtener P(Positivo)
p_positivo = (p_positivo_dado_enfermedad * p_enfermedad) + (p_positivo_dado_no * p_no_enfermedad)

# Usamos Bayes para obtener la probabilidad condicionada (posterior)
# P(Enfermedad | Positivo) = (P(Positivo | Enfermedad) * P(Enfermedad)) / P(Positivo)
p_enfermedad_dado_positivo = (p_positivo_dado_enfermedad * p_enfermedad) / p_positivo

# También obtenemos la probabilidad del complemento
p_no_enfermedad_dado_positivo = (p_positivo_dado_no * p_no_enfermedad) / p_positivo

# Mostramos los resultados antes y después de normalizar (de hecho, ya están normalizados)
print("Probabilidades condicionadas (ya normalizadas):")
print(f"P(Enfermedad | Positivo) = {p_enfermedad_dado_positivo:.4f}")
print(f"P(NoEnfermedad | Positivo) = {p_no_enfermedad_dado_positivo:.4f}")

# Verificamos que la suma de las probabilidades condicionadas es 1
suma = p_enfermedad_dado_positivo + p_no_enfermedad_dado_positivo
print(f"Suma de probabilidades = {suma:.4f}")  # Debe ser 1.0000 (normalización correcta)

# Si se tuvieran probabilidades sin normalizar, las normalizamos manualmente:
# Supongamos valores arbitrarios no normalizados:
no_norm = {
    'Enfermedad': 0.75,
    'NoEnfermedad': 0.25
}

# Calculamos el total para normalizar
total = sum(no_norm.values())

# Normalizamos manualmente
normalizado = {k: v / total for k, v in no_norm.items()}

print("\nEjemplo de normalización manual:")
for estado, prob in normalizado.items():
    print(f"P({estado}) = {prob:.4f}")
