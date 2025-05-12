import random

# Definir los valores posibles de cada variable
valores = {
    'Lluvia': ['Sí', 'No'],
    'Riego': ['Sí', 'No'],
    'CéspedMojado': ['Sí', 'No']
}

# Padres de cada nodo en la red bayesiana
padres = {
    'Lluvia': [],
    'Riego': [],
    'CéspedMojado': ['Lluvia', 'Riego']
}

# Tablas de probabilidad condicional (CPTs)
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

# Genera una muestra con ponderación de verosimilitud
def generar_muestra_ponderada(evidencia):
    muestra = {}
    peso = 1.0  # Inicializar el peso a 1
    for var in ['Lluvia', 'Riego', 'CéspedMojado']:  # Orden de muestreo
        if var in evidencia:
            # Si es variable observada, usar la probabilidad directamente como peso
            padres_vals = tuple(muestra[p] for p in padres[var])
            prob = cpts[var].get((evidencia[var],) + padres_vals, 0.0)
            muestra[var] = evidencia[var]
            peso *= prob  # Multiplicamos el peso acumulado
        else:
            # Si no es observada, muestrear normalmente
            if padres[var]:
                padres_vals = tuple(muestra[p] for p in padres[var])
                prob_true = cpts[var].get(('Sí',) + padres_vals, 0.0)
            else:
                prob_true = cpts[var].get(('Sí',), 0.0)
            muestra[var] = random.choices(['Sí', 'No'], weights=[prob_true, 1 - prob_true])[0]
    return muestra, peso

# Estimar P(consulta | evidencia) usando ponderación
def ponderacion_verosimilitud(consulta_var, consulta_val, evidencia, n=10000):
    numerador = 0.0
    denominador = 0.0
    for _ in range(n):
        muestra, peso = generar_muestra_ponderada(evidencia)
        if muestra[consulta_var] == consulta_val:
            numerador += peso
        denominador += peso
    if denominador == 0:
        return 0.0
    return numerador / denominador

# Ejecutar ejemplo
if __name__ == "__main__":
    evidencia = {'CéspedMojado': 'Sí'}  # Observamos que el césped está mojado
    prob_lluvia = ponderacion_verosimilitud('Lluvia', 'Sí', evidencia)
    print(f"P(Lluvia = Sí | CéspedMojado = Sí) ≈ {prob_lluvia:.4f}")
