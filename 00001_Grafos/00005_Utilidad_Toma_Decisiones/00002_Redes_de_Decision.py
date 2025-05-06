import networkx as nx

class DecisionNetwork:
    def __init__(self):
        """ Inicializa una red de decisión como un grafo dirigido. """
        self.G = nx.DiGraph()

    def add_decision_node(self, node, options):
        """
        Agrega un nodo de decisión con múltiples opciones posibles.
        
        :param node: Identificador del nodo
        :param options: Diccionario con opciones y probabilidades
        """
        self.G.add_node(node, type="decision", options=options)

    def add_chance_node(self, node, probabilities):
        """
        Agrega un nodo de incertidumbre con probabilidades de ocurrencia.
        
        :param node: Identificador del nodo
        :param probabilities: Diccionario con estados y probabilidades
        """
        self.G.add_node(node, type="chance", probabilities=probabilities)

    def add_utility_node(self, node, value):
        """
        Agrega un nodo de utilidad que representa una ganancia o costo.
        
        :param node: Identificador del nodo
        :param value: Valor numérico asociado al nodo
        """
        self.G.add_node(node, type="utility", value=value)

    def expected_utility(self, node):
        """
        Calcula la utilidad esperada desde un nodo de decisión.
        
        :param node: Identificador del nodo de decisión
        :return: Utilidad esperada del nodo
        """
        if self.G.nodes[node]["type"] != "decision":
            return None  # La función solo aplica a nodos de decisión
        
        utility = 0
        for option, prob in self.G.nodes[node]["options"].items():
            if option in self.G.nodes and "value" in self.G.nodes[option]:  # Verifica si tiene utilidad definida
                utility += prob * self.G.nodes[option]["value"]  # Calcula el valor ponderado
        return utility

# Creación de la red de decisión
network = DecisionNetwork()

# Definir nodos: decisiones, incertidumbres y utilidad
network.add_decision_node("Invertir", {"Alta rentabilidad": 0.6, "Baja rentabilidad": 0.4})
network.add_utility_node("Alta rentabilidad", 100)
network.add_utility_node("Baja rentabilidad", 30)

# Cálculo de la utilidad esperada
expected_value = network.expected_utility("Invertir")
print(f"Utilidad esperada de invertir: {expected_value}")