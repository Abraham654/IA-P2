import networkx as nx

def value_iteration(G, discount_factor=0.9, tolerance=0.01, max_iterations=100):
    # Implementa Value Iteration para encontrar los valores óptimos de los nodos (estados) en el grafo.
    # Los valores se actualizan iterativamente usando la ecuación de Bellman (adaptada a la estructura del grafo).

    # Inicializa los valores de todos los nodos. Usa la recompensa del nodo si existe, sino 0.
    values = {node: float(G.nodes[node].get("reward", 0)) for node in G.nodes}
    iteration = 0 # Contador de iteraciones

    # Bucle principal de Value Iteration
    while iteration < max_iterations:
        new_values = values.copy() # Copia los valores para la actualización simultánea
        max_change = 0 # Rastrea el cambio máximo en los valores en esta iteración

        # Itera sobre cada nodo (estado) para calcular su nuevo valor
        for node in G.nodes:
            # Si el nodo es un estado terminal (no tiene aristas de salida), su valor es solo su recompensa inmediata.
            if G.out_degree(node) == 0:
                 new_values[node] = float(G.nodes[node].get("reward", 0))
                 continue # No hay transiciones futuras, pasa al siguiente nodo

            # Para nodos no terminales, calcula el mejor valor esperado considerando las transiciones salientes.
            # La lógica aquí sigue V(s) = max_s' [P(s'|s) * (R(s') + gamma * V(s'))] basada en la estructura original,
            # donde maximizamos sobre las posibles transiciones de un solo paso representadas por las aristas salientes.
            best_value_from_transitions = float('-inf') # Inicializa con un valor muy bajo para encontrar el máximo esperado

            # Itera sobre todas las aristas que salen de 'node'. Cada arista representa una posible transición.
            # (u, v, data) -> u es el nodo actual, v es el vecino, data es el diccionario de atributos de la arista.
            for _, neighbor, edge_data in G.out_edges(node, data=True):
                # Obtiene la probabilidad de esta transición de la arista, por defecto 1.0 si no se especifica.
                transition_prob = edge_data.get('prob', 1.0)

                # Calcula el valor esperado si tomamos esta transición:
                # probabilidad de la transición * (recompensa en el nodo destino + factor de descuento * valor actual del nodo destino)
                expected_value_via_transition = transition_prob * (float(G.nodes[neighbor].get("reward", 0)) + discount_factor * values[neighbor])

                # Actualiza el mejor valor esperado si esta transición ofrece un valor mayor
                best_value_from_transitions = max(best_value_from_transitions, expected_value_via_transition)

            # El nuevo valor del nodo es el máximo valor esperado encontrado entre todas sus transiciones salientes.
            new_values[node] = best_value_from_transitions

            # Calcula la diferencia absoluta entre el nuevo valor y el valor anterior para este nodo.
            max_change = max(max_change, abs(new_values[node] - values[node]))

        # Actualiza los valores de los nodos para la próxima iteración
        values = new_values
        iteration += 1

        # Verifica si el cambio máximo en los valores es menor que la tolerancia (criterio de convergencia)
        if max_change < tolerance:
            break # Los valores han convergido, sale del bucle

    return values # Retorna el diccionario con los valores óptimos encontrados para cada nodo

# --- Uso del código ---
# Crea un grafo dirigido para modelar un problema de decisión simple.
G = nx.DiGraph()

# Agrega nodos (estados) al grafo. Cada nodo puede tener un atributo 'reward'.
# Si 'reward' no está presente o es None, se tratará como 0 por defecto en la función.
G.add_nodes_from([
    (0, {"reward": 0}),    # Nodo 0: Estado inicial o intermedio sin recompensa inmediata significativa.
    (1, {"reward": 10}),   # Nodo 1: Estado terminal con una recompensa positiva.
    (2, {"reward": 5}),    # Nodo 2: Estado intermedio con una pequeña recompensa.
    (3, {"reward": 15}),   # Nodo 3: Estado terminal con una recompensa más alta.
    (4, {"reward": 2})     # Nodo 4: Estado terminal con una pequeña recompensa.
])

# Agrega aristas (transiciones) entre los nodos. Cada arista puede tener un atributo 'prob'.
# Si 'prob' no está presente, se tratará como 1.0 (transición determinística) por defecto.
G.add_edges_from([
    (0, 1, {"prob": 0.6}), # Transición del Nodo 0 al Nodo 1 con probabilidad 0.6.
    (0, 2, {"prob": 0.4}), # Transición del Nodo 0 al Nodo 2 con probabilidad 0.4.
    (2, 3, {"prob": 0.5}), # Transición del Nodo 2 al Nodo 3 con probabilidad 0.5.
    (2, 4, {"prob": 0.5})  # Transición del Nodo 2 al Nodo 4 con probabilidad 0.5.
])

# Aplica el algoritmo de Iteración de Valores al grafo para calcular el valor óptimo de cada estado.
optimal_values = value_iteration(G)

# Imprime los valores óptimos calculados para cada nodo.
print("Valores óptimos de los nodos:")
for node, value in optimal_values.items():
    # Formatea el valor a 4 decimales para una mejor legibilidad.
    print(f"Nodo {node}: {value:.4f}")