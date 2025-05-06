import networkx as nx
import numpy as np

class GraphGame:
    def __init__(self, G, payoffs):
        # Grafo dirigido y pagos por nodo (jugador)
        self.G = G
        self.payoffs = payoffs

    def best_response(self, player):
        # Retorna el vecino con mayor pago, si tiene
        neighbors = list(self.G.neighbors(player))
        if not neighbors:
            return None
        return max(neighbors, key=lambda n: self.payoffs.get(n, 0))

    def nash_equilibrium(self):
        # Calcula la mejor jugada para cada jugador
        return {player: self.best_response(player) for player in self.G.nodes}

# -------- Configuración del juego --------
G = nx.DiGraph()
G.add_edges_from([
    (0, 1), (0, 2),
    (1, 2),
    (2, 3),
    (3, 1)
])

payoffs = {0: 3, 1: 5, 2: 2, 3: 4}

game = GraphGame(G, payoffs)

equilibrium = game.nash_equilibrium()
print(f"Equilibrio de Nash: {equilibrium}")
