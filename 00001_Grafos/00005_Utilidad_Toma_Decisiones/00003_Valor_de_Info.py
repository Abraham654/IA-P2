import networkx as nx

class DecisionNetwork:
    def __init__(self):
        # Inicializa la red como un grafo dirigido
        self.G = nx.DiGraph()

    def add_decision_node(self, node, options):
        # Agrega nodo de decisión con opciones (diccionario: opción -> probabilidad)
        self.G.add_node(node, type="decision", options=options)

    def add_information_node(self, node, outcomes):
        # Agrega nodo de información con posibles resultados (diccionario: resultado -> probabilidad)
        self.G.add_node(node, type="information", outcomes=outcomes)

    def add_utility_node(self, node, value):
        # Agrega nodo de utilidad con un valor numérico
        self.G.add_node(node, type="utility", value=value)

    def expected_utility(self, node):
        # Calcula la utilidad esperada recursivamente desde un nodo
        # Retorna 0 si el nodo no existe o no es decision/utility
        if node not in self.G.nodes or "type" not in self.G.nodes[node]:
            return 0

        # Si es un nodo de utilidad, retorna su valor directo
        if self.G.nodes[node]["type"] == "utility":
            return self.G.nodes[node].get("value", 0)
        
        # Si es un nodo de decisión, calcula la suma ponderada de utilidades esperadas de las opciones
        if self.G.nodes[node]["type"] == "decision":
            utility = 0
            for option, prob in self.G.nodes[node]["options"].items():
                # Suma (probabilidad de la opción * utilidad esperada de la opción)
                if option in self.G.nodes: # Asegura que la opción referenciada exista como nodo
                    utility += prob * self.expected_utility(option)
            return utility

        return 0

    def value_of_information(self, decision_node, info_node):
        # Calcula el Valor de la Información (VoI) para un nodo de información dado un nodo de decisión.
        # Compara la utilidad esperada con y sin la información.
        if self.G.nodes[info_node]["type"] != "information":
            return None # Solo aplica a nodos de información

        # Utilidad esperada sin considerar la información (decisión basada en creencias previas)
        expected_without_info = self.expected_utility(decision_node)
        expected_with_info = 0

        # Calcula la utilidad esperada si la decisión se toma DESPUÉS de conocer el resultado del nodo de información
        for outcome, prob in self.G.nodes[info_node]["outcomes"].items():
            # Para cada posible resultado de la info, calcula la utilidad esperada subsiguiente
            outcome_utility = self.expected_utility(outcome)
            # Suma (probabilidad del resultado de la info * utilidad esperada tras ese resultado)
            expected_with_info += prob * outcome_utility if outcome_utility is not None else 0

        # VoI = (Utilidad con información) - (Utilidad sin información)
        return expected_with_info - expected_without_info

# --- Uso del código ---
network = DecisionNetwork()

# Nodos: Decisión, Información, Utilidad
network.add_decision_node("Invertir", {"Alta rentabilidad": 0.6, "Baja rentabilidad": 0.4})
network.add_information_node("Informe Económico", {"Alta rentabilidad": 0.7, "Baja rentabilidad": 0.3})
network.add_utility_node("Alta rentabilidad", 100) # Nodo que representa la utilidad si ocurre "Alta rentabilidad"
network.add_utility_node("Baja rentabilidad", 30)  # Nodo que representa la utilidad si ocurre "Baja rentabilidad"

# Cálculo del valor de la información
voi = network.value_of_information("Invertir", "Informe Económico")
print(f"Valor de la Información del informe económico: {voi}")