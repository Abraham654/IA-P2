# Importamos las bibliotecas necesarias
import numpy as np  # Para cálculos numéricos
import matplotlib.pyplot as plt  # Para graficar

# Definimos una función para generar un proceso estacionario
def generar_proceso_estacionario(media, varianza, n_puntos):
    """
    Genera un proceso estacionario con media y varianza constantes.
    :param media: Media del proceso
    :param varianza: Varianza del proceso
    :param n_puntos: Número de puntos en el proceso
    :return: Serie de tiempo del proceso estacionario
    """
    # Generamos una serie de tiempo con distribución normal
    return np.random.normal(loc=media, scale=np.sqrt(varianza), size=n_puntos)

# Parámetros del proceso estacionario
media = 0  # Media constante
varianza = 1  # Varianza constante
n_puntos = 1000  # Número de puntos en la serie de tiempo

# Generamos el proceso estacionario
proceso = generar_proceso_estacionario(media, varianza, n_puntos)

# Graficamos el proceso estacionario
plt.figure(figsize=(10, 6))  # Configuramos el tamaño de la figura
plt.plot(proceso, label="Proceso Estacionario")  # Graficamos la serie de tiempo
plt.axhline(y=media, color='r', linestyle='--', label="Media")  # Línea de la media
plt.title("Proceso Estacionario")  # Título del gráfico
plt.xlabel("Tiempo")  # Etiqueta del eje x
plt.ylabel("Valor")  # Etiqueta del eje y
plt.legend()  # Mostramos la leyenda
plt.grid()  # Mostramos una cuadrícula
plt.show()  # Mostramos el gráfico

# Verificamos la estacionariedad calculando la media y varianza
media_calculada = np.mean(proceso)  # Calculamos la media de la serie
varianza_calculada = np.var(proceso)  # Calculamos la varianza de la serie

# Imprimimos los resultados
print(f"Media calculada: {media_calculada:.4f}")  # Mostramos la media calculada
print(f"Varianza calculada: {varianza_calculada:.4f}")  # Mostramos la varianza calculada