import random

# Definir dominios de cada variable
valores = {
    'Lluvia': ['Sí', 'No'],
    'Riego': ['Sí', 'No'],
    'CéspedMojado': ['Sí', 'No']
}

# Padres de cada variable
padres = {
    'Lluvia': [],
    'Riego': [],
    'CéspedMojado': ['Lluvia', 'Riego']
}

# CPTs: Tablas de probabilidad condicional para cada variable
cpts = {
    'Lluvia': {
        ('Sí',): 0.3,
        ('No',): 0.7
    },
    'Riego': {
        ('Sí',): 0.4,
        ('No',): 0.6
    },
    'CéspedMojado': {
        ('Sí', 'Sí', 'Sí'): 0.99,
        ('No', 'Sí', 'Sí'): 0.01,
        ('Sí', 'Sí', 'No'): 0.9,
        ('No', 'Sí', 'No'): 0.1,
        ('Sí', 'No', 'Sí'): 0.8,
        ('No', 'No', 'Sí'): 0.2,
        ('Sí', 'No', 'No'): 0.0,
        ('No', 'No', 'No'): 1.0
    }
}

# Generar una muestra según la red bayesiana
def generar_muestra():
    muestra = {}
    # Muestrear Lluvia
    muestra['Lluvia'] = random.choices(['Sí', 'No'], weights=[0.3, 0.7])[0]
    # Muestrear Riego
    muestra['Riego'] = random.choices(['Sí', 'No'], weights=[0.4, 0.6])[0]
    # Muestrear CéspedMojado en función de Lluvia y Riego
    lluvia = muestra['Lluvia']
    riego = muestra['Riego']
    p_sí = cpts['CéspedMojado'][('Sí', lluvia, riego)]
    muestra['CéspedMojado'] = random.choices(['Sí', 'No'], weights=[p_sí, 1 - p_sí])[0]
    return muestra

# Muestreo directo: contar ocurrencias donde se cumpla la consulta
def muestreo_directo(variable_consulta, valor_objetivo, n_muestras=10000):
    conteo = 0
    for _ in range(n_muestras):
        muestra = generar_muestra()
        if muestra[variable_consulta] == valor_objetivo:
            conteo += 1
    return conteo / n_muestras

# Muestreo por rechazo: filtrar muestras que cumplan la evidencia
def muestreo_por_rechazo(variable_consulta, valor_objetivo, evidencia, n_muestras=10000):
    aceptadas = 0
    coincidencias = 0
    for _ in range(n_muestras):
        muestra = generar_muestra()
        if all(muestra[v] == val for v, val in evidencia.items()):  # Solo aceptar si coincide evidencia
            aceptadas += 1
            if muestra[variable_consulta] == valor_objetivo:
                coincidencias += 1
    if aceptadas == 0:
        return 0.0  # No se pudo estimar si no hubo muestras válidas
    return coincidencias / aceptadas

# Ejecutar ejemplo
if __name__ == "__main__":
    print("Estimación con muestreo directo:")
    prob_lluvia = muestreo_directo('Lluvia', 'Sí')
    print(f"P(Lluvia = Sí): {prob_lluvia:.4f}")

    print("\nEstimación con muestreo por rechazo dado CéspedMojado = Sí:")
    prob_lluvia_dado_mojado = muestreo_por_rechazo('Lluvia', 'Sí', {'CéspedMojado': 'Sí'})
    print(f"P(Lluvia = Sí | CéspedMojado = Sí): {prob_lluvia_dado_mojado:.4f}")
