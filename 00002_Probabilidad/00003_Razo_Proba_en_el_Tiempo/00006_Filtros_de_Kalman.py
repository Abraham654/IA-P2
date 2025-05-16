# Importamos las librerías necesarias
import numpy as np  # Para operaciones numéricas y matrices

class KalmanFilter:
    def __init__(self, A, B, H, Q, R, x0, P0):
        # Matriz de transición de estado
        self.A = A
        # Matriz de control
        self.B = B
        # Matriz de observación
        self.H = H
        # Covarianza del ruido de proceso
        self.Q = Q
        # Covarianza del ruido de medición
        self.R = R
        # Estado inicial estimado
        self.x = x0
        # Covarianza inicial del estado
        self.P = P0

    def predict(self, u):
        # Predicción del estado siguiente usando el modelo
        self.x = self.A @ self.x + self.B @ u
        # Predicción de la covarianza del estado
        self.P = self.A @ self.P @ self.A.T + self.Q

    def update(self, z):
        # Cálculo de la ganancia de Kalman
        S = self.H @ self.P @ self.H.T + self.R  # Covarianza de la innovación
        K = self.P @ self.H.T @ np.linalg.inv(S)  # Ganancia de Kalman
        # Actualización del estado estimado con la medición
        y = z - self.H @ self.x  # Innovación o residuo
        self.x = self.x + K @ y
        # Actualización de la covarianza del estado
        I = np.eye(self.P.shape[0])  # Matriz identidad
        self.P = (I - K @ self.H) @ self.P

    def current_state(self):
        # Devuelve el estado estimado actual
        return self.x

# Ejemplo de uso del filtro de Kalman para estimar la posición de un objeto en 1D

# Definimos las matrices del modelo
A = np.array([[1]])       # El estado solo depende del anterior (posición constante)
B = np.array([[0]])       # No hay control externo
H = np.array([[1]])       # Observamos directamente la posición
Q = np.array([[0.01]])    # Ruido de proceso pequeño
R = np.array([[0.1]])     # Ruido de medición mayor
x0 = np.array([[0]])      # Estado inicial (posición 0)
P0 = np.array([[1]])      # Incertidumbre inicial

# Creamos el filtro de Kalman
kf = KalmanFilter(A, B, H, Q, R, x0, P0)

# Simulamos algunas mediciones ruidosas
mediciones = [0.05, -0.02, 0.04, 0.1, 0.08]

for z in mediciones:
    kf.predict(u=np.array([[0]]))  # No hay control
    kf.update(z=np.array([[z]]))   # Actualizamos con la medición
    print("Estado estimado:", kf.current_state().flatten()[0])  # Mostramos la estimación