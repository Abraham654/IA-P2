import math
import random

# Definimos una variable aleatoria: Clima = {Soleado, Nublado, Lluvioso}
clima_valores = ['Soleado', 'Nublado', 'Lluvioso']

# Distribución de probabilidad: P(Clima)
prob_clima = {
    'Soleado': 0.5,
    'Nublado': 0.3,
    'Lluvioso': 0.2
}

# -------------------- ENTROPÍA --------------------

# Función para calcular la entropía H(X) = -Σ p(x) log2 p(x)
def entropia(distribucion):
    h = 0.0
    for p in distribucion.values():
        if p > 0:
            h -= p * math.log2(p)  # Fórmula base de la teoría de la información
    return h

# Calcular y mostrar la entropía de la variable Clima
H_clima = entropia(prob_clima)
print(f"Entropía H(Clima): {H_clima:.4f} bits")  # Mide la incertidumbre promedio

# -------------------- MUESTREO --------------------

# Simulamos 1000 muestras de Clima para observar su variabilidad
muestras = random.choices(
    population=list(prob_clima.keys()),
    weights=list(prob_clima.values()),
    k=1000  # número de muestras
)

# Contamos cuántas veces apareció cada estado
conteo = {valor: muestras.count(valor) for valor in clima_valores}

# Estimación de frecuencias observadas
print("\nFrecuencias observadas:")
for valor in clima_valores:
    frec = conteo[valor] / len(muestras)
    print(f"P({valor}) ≈ {frec:.3f}")

# -------------------- ACTUALIZACIÓN POR EVIDENCIA --------------------

# Supongamos que observamos 'Nublado' como evidencia
# Queremos actualizar la creencia: P(Actividad | Clima)

# Definimos una distribución condicional P(Actividad | Clima)
# Actividades posibles: {Parque, Cine}
condicional = {
    'Soleado': {'Parque': 0.9, 'Cine': 0.1},
    'Nublado': {'Parque': 0.4, 'Cine': 0.6},
    'Lluvioso': {'Parque': 0.1, 'Cine': 0.9}
}

# Calculamos P(Actividad) dado que observamos Clima = 'Nublado'
clima_observado = 'Nublado'
p_actividad_dado_clima = condicional[clima_observado]

print(f"\nP(Actividad | Clima = {clima_observado}):")
for actividad, prob in p_actividad_dado_clima.items():
    print(f"{actividad}: {prob:.2f}")
