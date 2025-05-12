import matplotlib.pyplot as plt  # Para graficar distribuciones
import numpy as np               # Para operaciones numéricas

# Definimos los posibles valores que puede tomar una variable discreta: caras en un dado
valores = np.array([1, 2, 3, 4, 5, 6])  # Espacio de estados de la variable aleatoria

# Asignamos una probabilidad uniforme (equiprobable) para cada valor del dado
probabilidades = np.array([1/6] * 6)  # Distribución de probabilidad discreta

# Verificamos que las probabilidades sumen 1 (normalización)
print(f"Suma de probabilidades: {np.sum(probabilidades)}")  # Debe ser 1.0

# Mostramos la distribución como pares valor:probabilidad
print("Distribución de probabilidad del dado:")
for valor, prob in zip(valores, probabilidades):
    print(f"P({valor}) = {prob:.3f}")

# Calculamos el valor esperado (media) de la variable aleatoria
valor_esperado = np.sum(valores * probabilidades)  # E[X] = Σx·P(x)
print(f"\nValor esperado (media) = {valor_esperado:.2f}")

# Calculamos la varianza: E[X²] - (E[X])²
esperado_cuadrado = np.sum((valores**2) * probabilidades)
varianza = esperado_cuadrado - valor_esperado**2
print(f"Varianza = {varianza:.2f}")

# Graficamos la distribución de probabilidad
plt.bar(valores, probabilidades, color='skyblue', edgecolor='black')
plt.xlabel("Valor del dado")
plt.ylabel("Probabilidad")
plt.title("Distribución de Probabilidad Discreta (Dado Justo)")
plt.grid(axis='y')
plt.xticks(valores)
plt.show()
