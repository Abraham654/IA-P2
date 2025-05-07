import numpy as np
import itertools
from collections import defaultdict

class DynamicBayesianNetwork:
    def __init__(self, variables, estructura, distribuciones_iniciales, transiciones):
        # Inicializa la red con variables, estructura, distribuciones y transiciones
        self.variables = variables
        self.estructura = estructura
        self.inicial = distribuciones_iniciales
        self.transiciones = transiciones
        self.tiempo_actual = 0
        self.creencia_actual = distribuciones_iniciales.copy()

    def actualizar_creencia(self, evidencias):
        # Actualiza las creencias con el filtro de Bayes usando evidencias observadas
        nueva_creencia = {}
        for variable in self.variables:
            if variable in evidencias:
                # Si hay evidencia directa, se usa como certeza
                nueva_creencia[variable] = {evidencias[variable]: 1.0}
            else:
                padres_t, padres_t_1 = self.estructura[variable]
                prob = defaultdict(float)

                # Calcula probabilidad marginal integrando padres en t y t-1
                for valor in self.obtener_dominio(variable):
                    for config_t in self.generar_configuraciones(padres_t):
                        for config_t_1 in self.generar_configuraciones(padres_t_1):
                            p_trans = self.obtener_prob_transicion(variable, valor, config_t, config_t_1)
                            p_padres = self.prob_conjunta_padres(config_t, config_t_1)
                            prob[valor] += p_trans * p_padres

                total = sum(prob.values())
                if total > 0:
                    for valor in prob:
                        prob[valor] /= total

                nueva_creencia[variable] = dict(prob)

        self.creencia_actual = nueva_creencia
        self.tiempo_actual += 1
        return self.creencia_actual

    def obtener_prob_transicion(self, variable, valor, padres_t, padres_t_1):
        # Retorna la probabilidad P(variable=valor|padres) desde CPT inicial o de transición
        cpt = self.inicial[variable] if self.tiempo_actual == 0 else self.transiciones[variable]
        key = (valor,) + tuple(padres_t.items()) + tuple(padres_t_1.items())
        return cpt.get(key, 0.0)

    def prob_conjunta_padres(self, padres_t, padres_t_1):
        # Calcula la probabilidad conjunta de las configuraciones de padres
        prob = 1.0
        for var, val in padres_t.items():
            prob *= self.creencia_actual.get(var, {}).get(val, 0.0)
        for var, val in padres_t_1.items():
            prob *= self.creencia_actual.get(var, {}).get(val, 0.0)
        return prob

    def generar_configuraciones(self, variables):
        # Genera todas las combinaciones posibles de valores para un conjunto de variables
        if not variables:
            return [{}]
        dominios = [self.obtener_dominio(var) for var in variables]
        return [dict(zip(variables, comb)) for comb in itertools.product(*dominios)]

    def obtener_dominio(self, variable):
        # Retorna el conjunto de valores posibles que puede tomar una variable
        if self.tiempo_actual == 0:
            claves = self.inicial[variable].keys()
        else:
            claves = self.transiciones[variable].keys()
        return set(clave[0] for clave in claves)

# Ejemplo práctico: detección de fallo en sensor
if __name__ == "__main__":
    variables = ['Fallo', 'Lectura']

    # Define padres por tiempo: [padres_t, padres_t-1]
    estructura = {
        'Fallo': [[], ['Fallo']],
        'Lectura': [['Fallo'], []]
    }

    # CPT inicial (t = 0)
    inicial = {
        'Fallo': {
            (False,): 0.9,
            (True,): 0.1
        },
        'Lectura': {
            (True, False): 0.8,
            (False, False): 0.2,
            (True, True): 0.1,
            (False, True): 0.9
        }
    }

    # CPTs para transición temporal (t > 0)
    transiciones = {
        'Fallo': {
            (False, ('Fallo', False)): 0.7,
            (True, ('Fallo', False)): 0.3,
            (False, ('Fallo', True)): 0.4,
            (True, ('Fallo', True)): 0.6
        },
        'Lectura': {
            (True, ('Fallo', False)): 0.8,
            (False, ('Fallo', False)): 0.2,
            (True, ('Fallo', True)): 0.1,
            (False, ('Fallo', True)): 0.9
        }
    }

    dbn = DynamicBayesianNetwork(variables, estructura, inicial, transiciones)

    evidencias = [{'Lectura': True}, {'Lectura': False}, {'Lectura': False}]
    for t, evidencia in enumerate(evidencias):
        creencia = dbn.actualizar_creencia(evidencia)
        print(f"\nTiempo {t+1}:")
        print(f"Creencia en Fallo: {creencia['Fallo']}")
        print(f"Creencia en Lectura: {creencia['Lectura']}")
