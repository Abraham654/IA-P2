import itertools  # Para generar combinaciones de valores posibles
from collections import defaultdict  # Diccionario con valor por defecto

# Definimos los valores posibles para cada variable
valores = {
    'Clima': ['Soleado', 'Lluvioso'],      # Variable A
    'Riego': ['Sí', 'No'],                 # Variable B
    'CéspedMojado': ['Sí', 'No']           # Variable C
}

# Definimos las probabilidades condicionales P(CéspedMojado | Clima, Riego)
P_cesped = {
    ('Sí', 'Soleado', 'Sí'): 0.9,
    ('No', 'Soleado', 'Sí'): 0.1,
    ('Sí', 'Soleado', 'No'): 0.2,
    ('No', 'Soleado', 'No'): 0.8,
    ('Sí', 'Lluvioso', 'Sí'): 0.99,
    ('No', 'Lluvioso', 'Sí'): 0.01,
    ('Sí', 'Lluvioso', 'No'): 0.9,
    ('No', 'Lluvioso', 'No'): 0.1
}

# Definimos las probabilidades marginales P(Clima) y P(Riego)
P_clima = {'Soleado': 0.6, 'Lluvioso': 0.4}
P_riego = {'Sí': 0.5, 'No': 0.5}

# Función para calcular P(A, B, C) usando regla de la cadena
def prob_conjunta(clima, riego, cesped):
    p_a = P_clima[clima]
    p_b = P_riego[riego]
    p_c = P_cesped[(cesped, clima, riego)]
    return p_a * p_b * p_c  # P(A)·P(B)·P(C|A,B)

# Calculamos la distribución conjunta completa
conjunta = defaultdict(float)
for clima, riego, cesped in itertools.product(valores['Clima'], valores['Riego'], valores['CéspedMojado']):
    conjunta[(clima, riego, cesped)] = prob_conjunta(clima, riego, cesped)

# Función para calcular distribución condicional P(X | Y = y)
def distribucion_condicional(variable_obj, condicion, conjunta):
    total = 0
    cond_probs = defaultdict(float)
    
    for k, p in conjunta.items():
        escenario = dict(zip(['Clima', 'Riego', 'CéspedMojado'], k))
        if all(escenario[c] == v for c, v in condicion.items()):
            val_obj = escenario[variable_obj]
            cond_probs[val_obj] += p
            total += p
    
    if total > 0:
        for k in cond_probs:
            cond_probs[k] /= total
    return dict(cond_probs)

# Comprobamos si Clima ⊥ Riego | CéspedMojado
# Para cada valor posible de CéspedMojado
print("¿Clima ⊥ Riego | CéspedMojado?")
for cesped in valores['CéspedMojado']:
    p_clima_dado_c = distribucion_condicional('Clima', {'CéspedMojado': cesped}, conjunta)
    p_clima_dado_c_y_r = distribucion_condicional('Clima', {'CéspedMojado': cesped, 'Riego': 'Sí'}, conjunta)
    
    print(f"\nP(Clima | CéspedMojado={cesped}): {p_clima_dado_c}")
    print(f"P(Clima | CéspedMojado={cesped}, Riego=Sí): {p_clima_dado_c_y_r}")

    if all(abs(p_clima_dado_c[k] - p_clima_dado_c_y_r.get(k, 0)) < 0.01 for k in p_clima_dado_c):
        print("→ Clima es condicionalmente independiente de Riego dado CéspedMojado =", cesped)
    else:
        print("→ Clima NO es condicionalmente independiente de Riego dado CéspedMojado =", cesped)
