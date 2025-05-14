import math # Importa la librería 'math', que contiene funciones matemáticas como logaritmos.
import random # Importa la librería 'random', que contiene funciones para generar números y hacer selecciones aleatorias.

# Definimos una variable aleatoria: Clima = {Soleado, Nublado, Lluvioso}
# Esta línea define una lista con los posibles estados o valores que puede tomar la variable 'Clima'.
clima_valores = ['Soleado', 'Nublado', 'Lluvioso']

# Distribución de probabilidad: P(Clima)
# Esta línea define un diccionario donde las claves son los estados del clima
# y los valores son las probabilidades asignadas a cada estado.
prob_clima = {
    'Soleado': 0.5, # Probabilidad de que el clima sea 'Soleado'.
    'Nublado': 0.3, # Probabilidad de que el clima sea 'Nublado'.
    'Lluvioso': 0.2 # Probabilidad de que el clima sea 'Lluvioso'.
}

# -------------------- ENTROPÍA --------------------

# Función para calcular la entropía H(X) = -Σ p(x) log2 p(x)
# Define una función llamada 'entropia' que toma un argumento llamado 'distribucion' (que se espera sea un diccionario de probabilidades).
def entropia(distribucion):
    h = 0.0 # Inicializa una variable 'h' (para la entropía) en 0.0 (un número flotante).
    # Itera sobre los valores (las probabilidades) del diccionario 'distribucion'.
    for p in distribucion.values():
        # Comprueba si la probabilidad 'p' es mayor que 0, ya que log2(0) no está definido.
        if p > 0:
            # Aplica la fórmula de la entropía: resta p * log2(p) a 'h'.
            # math.log2(p) calcula el logaritmo base 2 de la probabilidad 'p'.
            h -= p * math.log2(p)  # Fórmula base de la teoría de la información
    return h # Retorna el valor calculado de la entropía.

# Calcular y mostrar la entropía de la variable Clima
# Llama a la función 'entropia' con el diccionario 'prob_clima' y guarda el resultado en 'H_clima'.
H_clima = entropia(prob_clima)
# Imprime el resultado de la entropía formateado a 4 decimales.
# La f-string permite incluir variables dentro de la cadena de texto.
print(f"Entropía H(Clima): {H_clima:.4f} bits")  # Mide la incertidumbre promedio

# -------------------- MUESTREO --------------------

# Simulamos 1000 muestras de Clima para observar su variabilidad
# Usa la función random.choices para seleccionar elementos de una lista con probabilidades dadas.
muestras = random.choices(
    population=list(prob_clima.keys()), # La lista de elementos a elegir (los estados del clima). Convertimos las claves del diccionario a lista.
    weights=list(prob_clima.values()), # La lista de pesos o probabilidades correspondientes a cada elemento. Convertimos los valores del diccionario a lista.
    k=1000 # El número de muestras o selecciones a realizar.
)

# Contamos cuántas veces apareció cada estado
# Crea un diccionario 'conteo' usando una comprensión de diccionario.
# Para cada 'valor' en la lista 'clima_valores', cuenta cuántas veces aparece ese valor en la lista 'muestras'.
conteo = {valor: muestras.count(valor) for valor in clima_valores}

# Estimación de frecuencias observadas
# Imprime un encabezado para la sección de frecuencias observadas.
print("\nFrecuencias observadas:")
# Itera sobre cada estado posible del clima definido en 'clima_valores'.
for valor in clima_valores:
    # Calcula la frecuencia observada dividiendo el conteo de ese valor entre el número total de muestras.
    frec = conteo[valor] / len(muestras)
    # Imprime la frecuencia observada para cada estado, formateada a 3 decimales.
    print(f"P({valor}) ≈ {frec:.3f}")

# -------------------- ACTUALIZACIÓN POR EVIDENCIA --------------------

# Supongamos que observamos 'Nublado' como evidencia
# Esta línea es un comentario que explica el contexto de la siguiente sección: actualizar creencias basándose en una observación.
# Queremos actualizar la creencia: P(Actividad | Clima)
# Otro comentario explicando el objetivo: calcular la probabilidad de una actividad dado un clima específico.

# Definimos una distribución condicional P(Actividad | Clima)
# Define un diccionario anidado que representa la probabilidad condicional de 'Actividad' dado 'Clima'.
# La clave exterior es el estado del clima, y el valor es otro diccionario con las probabilidades de las actividades para ese clima.
# Actividades posibles: {Parque, Cine}
condicional = {
    'Soleado': {'Parque': 0.9, 'Cine': 0.1}, # Si el clima es 'Soleado', P(Parque|Soleado)=0.9, P(Cine|Soleado)=0.1.
    'Nublado': {'Parque': 0.4, 'Cine': 0.6}, # Si el clima es 'Nublado', P(Parque|Nublado)=0.4, P(Cine|Nublado)=0.6.
    'Lluvioso': {'Parque': 0.1, 'Cine': 0.9} # Si el clima es 'Lluvioso', P(Parque|Lluvioso)=0.1, P(Cine|Lluvioso)=0.9.
}

# Calculamos P(Actividad) dado que observamos Clima = 'Nublado'
# Define una variable para almacenar la evidencia observada (el clima que sabemos que ocurrió).
clima_observado = 'Nublado'
# Accede al diccionario 'condicional' usando la clave 'clima_observado' ('Nublado').
# Esto obtiene el diccionario de probabilidades de actividades para el clima 'Nublado'.
p_actividad_dado_clima = condicional[clima_observado]

# Imprime un encabezado indicando para qué clima se están mostrando las probabilidades.
print(f"\nP(Actividad | Clima = {clima_observado}):")
# Itera sobre los pares clave-valor (actividad y su probabilidad) en el diccionario obtenido.
for actividad, prob in p_actividad_dado_clima.items():
    # Imprime cada actividad y su probabilidad condicional, formateada a 2 decimales.
    print(f"{actividad}: {prob:.2f}")