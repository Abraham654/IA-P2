from itertools import product
from collections import defaultdict

# Red bayesiana simple: variables con sus valores posibles
variables = {
    'Lluvia': ['Sí', 'No'],
    'Riego': ['Sí', 'No'],
    'CéspedMojado': ['Sí', 'No']
}

# Estructura de dependencia: padres de cada nodo
padres = {
    'Lluvia': [],
    'Riego': [],
    'CéspedMojado': ['Lluvia', 'Riego']
}

# Tablas de probabilidad condicional (CPTs)
# P(Lluvia)
cpt_lluvia = {('Sí',): 0.3, ('No',): 0.7}
# P(Riego)
cpt_riego = {('Sí',): 0.4, ('No',): 0.6}
# P(CéspedMojado | Lluvia, Riego)
cpt_cesped = {
    ('Sí', 'Sí', 'Sí'): 0.99,
    ('Sí', 'Sí', 'No'): 0.01,
    ('Sí', 'No', 'Sí'): 0.9,
    ('Sí', 'No', 'No'): 0.1,
    ('No', 'Sí', 'Sí'): 0.8,
    ('No', 'Sí', 'No'): 0.2,
    ('No', 'No', 'Sí'): 0.0,
    ('No', 'No', 'No'): 1.0
}

# Función para obtener la probabilidad de un nodo dado un escenario
def probabilidad(nodo, valor, escenario):
    if nodo == 'Lluvia':
        return cpt_lluvia[(valor,)]
    elif nodo == 'Riego':
        return cpt_riego[(valor,)]
    elif nodo == 'CéspedMojado':
        llu, rie = escenario['Lluvia'], escenario['Riego']
        return cpt_cesped[(llu, rie, valor)]

# Función de inferencia por enumeración
def inferencia_por_enumeracion(variable_objetivo, evidencia):
    # Guardar las distribuciones de probabilidad para cada valor del objetivo
    distribucion = defaultdict(float)
    
    # Variables ocultas = todas menos evidencia y objetivo
    ocultas = [v for v in variables if v not in evidencia and v != variable_objetivo]
    
    # Recorrer todos los valores posibles del objetivo
    for valor_obj in variables[variable_objetivo]:
        total = 0.0
        # Construir escenario base con evidencia + valor del objetivo
        base = dict(evidencia)
        base[variable_objetivo] = valor_obj
        
        # Enumerar todas las combinaciones de las variables ocultas
        for combinacion in product(*[variables[v] for v in ocultas]):
            escenario = dict(base)
            escenario.update(dict(zip(ocultas, combinacion)))
            
            # Calcular P(escenario completo)
            p = 1.0
            for var in variables:
                p *= probabilidad(var, escenario[var], escenario)
            total += p
        
        distribucion[valor_obj] = total
    
    # Normalizar los resultados para obtener una distribución válida
    suma = sum(distribucion.values())
    return {k: v / suma for k, v in distribucion.items()}

# Ejecutar inferencia: ¿Cuál es la probabilidad de Lluvia dado que CéspedMojado=Sí?
resultado = inferencia_por_enumeracion('Lluvia', {'CéspedMojado': 'Sí'})

# Mostrar resultados
print("P(Lluvia | CéspedMojado=Sí):")
for val, prob in resultado.items():
    print(f"{val}: {prob:.4f}")
