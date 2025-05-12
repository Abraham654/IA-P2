from itertools import product
from collections import defaultdict

# Variables y dominios
variables = {
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
        ('Sí', 'Sí', 'No'): 0.01,
        ('Sí', 'No', 'Sí'): 0.9,
        ('Sí', 'No', 'No'): 0.1,
        ('No', 'Sí', 'Sí'): 0.8,
        ('No', 'Sí', 'No'): 0.2,
        ('No', 'No', 'Sí'): 0.0,
        ('No', 'No', 'No'): 1.0
    }
}

# Construir factor para una variable y sus padres
def construir_factor(var):
    scope = [var] + padres[var]  # variables involucradas
    tabla = {}
    for entrada, prob in cpts[var].items():
        tabla[entrada] = prob
    return {'vars': scope, 'tabla': tabla}

# Aplicar evidencia (fijar valores conocidos)
def restringir_factor(factor, evidencia):
    nuevas_vars = [v for v in factor['vars'] if v not in evidencia]
    nueva_tabla = {}
    for key, prob in factor['tabla'].items():
        asign = dict(zip(factor['vars'], key))
        if all(asign.get(ev) == val for ev, val in evidencia.items()):
            nueva_clave = tuple(asign[v] for v in nuevas_vars)
            nueva_tabla[nueva_clave] = prob
    return {'vars': nuevas_vars, 'tabla': nueva_tabla}

# Multiplicar dos factores (join)
def multiplicar_factores(f1, f2):
    todas_vars = list(dict.fromkeys(f1['vars'] + f2['vars']))  # evitar duplicados
    tabla = {}
    for fila in product(*[variables[v] for v in todas_vars]):
        asign = dict(zip(todas_vars, fila))
        try:
            k1 = tuple(asign[v] for v in f1['vars'])
            k2 = tuple(asign[v] for v in f2['vars'])
            tabla[tuple(asign[v] for v in todas_vars)] = f1['tabla'][k1] * f2['tabla'][k2]
        except KeyError:
            continue
    return {'vars': todas_vars, 'tabla': tabla}

# Eliminar una variable (suma sobre ella)
def eliminar_variable(factor, var):
    nuevas_vars = [v for v in factor['vars'] if v != var]
    nueva_tabla = defaultdict(float)
    for fila, prob in factor['tabla'].items():
        asign = dict(zip(factor['vars'], fila))
        clave = tuple(asign[v] for v in nuevas_vars)
        nueva_tabla[clave] += prob
    return {'vars': nuevas_vars, 'tabla': dict(nueva_tabla)}

# Algoritmo principal de inferencia por eliminación de variables
def inferencia(query, evidencia):
    factores = [construir_factor(v) for v in variables]

    # Aplicar evidencia a todos los factores
    for ev in evidencia:
        factores = [restringir_factor(f, {ev: evidencia[ev]}) for f in factores]

    # Variables a eliminar (no query ni evidencia)
    eliminar = [v for v in variables if v != query and v not in evidencia]

    for var in eliminar:
        involucrados = [f for f in factores if var in f['vars']]
        no_involucrados = [f for f in factores if var not in f['vars']]
        if involucrados:
            combinado = involucrados[0]
            for f in involucrados[1:]:
                combinado = multiplicar_factores(combinado, f)
            nuevo = eliminar_variable(combinado, var)
            factores = no_involucrados + [nuevo]

    # Multiplicar factores restantes
    resultado = factores[0]
    for f in factores[1:]:
        resultado = multiplicar_factores(resultado, f)

    # Normalizar
    total = sum(resultado['tabla'].values())
    normalizado = {k: v / total for k, v in resultado['tabla'].items()}
    return normalizado

# Ejecución: calcular P(Lluvia | CéspedMojado = Sí)
if __name__ == "__main__":
    resultado = inferencia('Lluvia', {'CéspedMojado': 'Sí'})
    print("P(Lluvia | CéspedMojado = Sí):")
    for k, v in resultado.items():
        print(f"{k[0]}: {v:.4f}")
