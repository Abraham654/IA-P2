import networkx as nx

def policy_iteration(G, discount_factor=0.9, max_iterations=100):
    """
    Aplica el algoritmo de Iteración de Políticas en un grafo MDP.

    :param G: Grafo representando el problema de toma de decisiones
    :param discount_factor: Factor de descuento para futuras recompensas
    :param max_iterations: Número máximo de iteraciones
    :return: Diccionario con la política óptima y los valores de los estados
    """
    states = list(G.nodes)
    policy = {state: max(G.successors(state), default=state, key=lambda s: G[state][s].get('reward', 0)) for state in states}
    values = {state: 0 for state in states}  # Inicializa los valores en 0

    for _ in range(max_iterations):
        new_values = values.copy()
        
        for state in states:
            if G.out_degree(state) == 0:  # Si el estado no tiene transiciones, usa su recompensa
                new_values[state] = G.nodes[state].get("reward", 0)
            else:
                action = policy[state]  # Obtiene la acción de la política actual
                transition_prob = G[state][action].get('prob', 1)  # Probabilidad de transición
                reward = G[state][action].get("reward", 0)  # Recompensa de la acción
                new_values[state] = transition_prob * (reward + discount_factor * values[action])  # Fórmula de actualización
        
        if max(abs(new_values[s] - values[s]) for s in states) < 0.01:  # Convergencia
            break
        
        values = new_values  # Actualiza valores
        policy = {state: max(G.successors(state), default=state, key=lambda s: values[s]) for state in states}  # Actualiza política

    return policy, values

# Creación del grafo con recompensas y probabilidades
G = nx.DiGraph()
G.add_nodes_from([(0, {"reward": None}), (1, {"reward": 10}), (2, {"reward": 5}), 
                  (3, {"reward": 15}), (4, {"reward": 2})])
G.add_edges_from([(0, 1, {"prob": 0.6, "reward": 8}), (0, 2, {"prob": 0.4, "reward": 4}),
                  (2, 3, {"prob": 0.5, "reward": 12}), (2, 4, {"prob": 0.5, "reward": 3})])

# Aplicación de Iteración de Políticas
optimal_policy, optimal_values = policy_iteration(G)

print("Política óptima por estado:")
for state, action in optimal_policy.items():
    print(f"Estado {state} → Acción {action}")

print("\nValores óptimos de los estados:")
for state, value in optimal_values.items():
    print(f"Estado {state}: {value}")