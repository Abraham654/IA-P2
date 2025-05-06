import networkx as nx

def utility_function(G, node, risk_aversion=1.0):
    # Obtiene el pago del nodo, si es None, lo convierte en 0
    payoff = G.nodes[node].get('payoff')
    if payoff is None:
        payoff = 0

    # Calcula utilidad del nodo considerando aversión al riesgo
    utility = payoff ** (1 / risk_aversion)

    # Lista de (pago, probabilidad) de vecinos
    neighbor_payoffs = [
        (G.nodes[n].get('payoff', 0), G[node][n].get('prob', 1))
        for n in G.neighbors(node)
    ]

    if not neighbor_payoffs:  # Si no tiene vecinos, devuelve su propia utilidad
        return utility

    # Utilidad esperada de vecinos
    expected_utility = sum(
        p ** (1 / risk_aversion) * prob
        for p, prob in neighbor_payoffs
        if p is not None  # evita fallas si algún vecino también tiene payoff=None
    )

    return max(utility, expected_utility)  # Retorna el mayor valor entre utilidad propia y esperada

# ----------- Grafo con pagos y probabilidades -----------
G = nx.Graph()
G.add_nodes_from([
    (0, {"payoff": None}), (1, {"payoff": 10}),
    (2, {"payoff": 5}), (3, {"payoff": 15}),
    (4, {"payoff": 2})
])
G.add_edges_from([
    (0, 1, {"prob": 0.6}), (0, 2, {"prob": 0.4}),
    (2, 3, {"prob": 0.5}), (2, 4, {"prob": 0.5})
])

# ----------- Cálculo de utilidad del nodo raíz -----------
utility_value = utility_function(G, 0, risk_aversion=2.0)
print(f"Utilidad esperada del nodo raíz: {utility_value}")
