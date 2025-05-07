import numpy as np
from collections import defaultdict

class PolicySearch:
    def __init__(self, n_estados, n_acciones, gamma=0.95):
        """
        Implementación de búsqueda directa de política para grafos.
        
        Args:
            n_estados: Número de nodos en el grafo
            n_acciones: Número de acciones posibles
            gamma: Factor de descuento para recompensas futuras
        """
        self.politica = np.random.randint(n_acciones, size=n_estados)  # Política aleatoria inicial
        self.V = np.zeros(n_estados)  # Función de valor
        self.n_estados = n_estados
        self.n_acciones = n_acciones
        self.gamma = gamma

    def evaluacion_politica(self, entorno, theta=1e-5):
        """Evaluación iterativa de la política actual"""
        while True:
            delta = 0
            for s in range(self.n_estados):
                v = self.V[s]
                accion = self.politica[s]
                # Calcular nuevo valor para el estado
                self.V[s] = sum(
                    p * (r + self.gamma * self.V[s_next])
                    for s_next, p, r in entorno.resultados_posibles(s, accion)
                )
                delta = max(delta, abs(v - self.V[s]))
            if delta < theta:
                break

    def mejora_politica(self, entorno):
        """Mejora la política basándose en la función de valor actual"""
        politica_estable = True
        for s in range(self.n_estados):
            accion_actual = self.politica[s]
            # Seleccionar acción que maximiza el valor
            valores_acciones = []
            for a in range(self.n_acciones):
                valor = sum(
                    p * (r + self.gamma * self.V[s_next])
                    for s_next, p, r in entorno.resultados_posibles(s, a)
                )
                valores_acciones.append(valor)
            self.politica[s] = np.argmax(valores_acciones)
            if accion_actual != self.politica[s]:
                politica_estable = False
        return politica_estable

    def iteracion_politica(self, entorno):
        """Algoritmo completo de iteración de política"""
        while True:
            self.evaluacion_politica(entorno)
            if self.mejora_politica(entorno):
                break

class GrafoEntorno:
    """Entorno de grafo para pruebas"""
    def __init__(self):
        self.n_estados = 5
        self.n_acciones = 5  # Acciones = mover a nodo 0-4
        self.grafo = {
            0: [(1, 0.8, 2), (2, 0.2, -1)],  # (estado_destino, probabilidad, recompensa)
            1: [(3, 0.7, 1), (4, 0.3, 5)],
            2: [(0, 0.6, -1), (3, 0.4, 3)],
            3: [(4, 1.0, 10)],  # Estado terminal con alta recompensa
            4: [(4, 1.0, 0)]   # Estado terminal absorbente
        }
    
    def resultados_posibles(self, estado, accion):
        """Devuelve (estado_siguiente, probabilidad, recompensa)"""
        if accion in self.grafo.get(estado, []):
            return self.grafo[estado]
        return [(estado, 1.0, -10)]  # Penalización por acción inválida

# Ejemplo de uso
if __name__ == "__main__":
    entorno = GrafoEntorno()
    agente = PolicySearch(entorno.n_estados, entorno.n_acciones)
    
    print("Política inicial aleatoria:")
    print(agente.politica)
    
    print("\nEjecutando iteración de política...")
    agente.iteracion_politica(entorno)
    
    print("\nPolítica óptima encontrada:")
    print(agente.politica)
    
    print("\nValores estimados para cada estado:")
    for estado, valor in enumerate(agente.V):
        print(f"Estado {estado}: {valor:.2f}")