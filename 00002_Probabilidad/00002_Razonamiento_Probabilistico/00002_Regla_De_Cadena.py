from itertools import product
from collections import defaultdict  # Importación faltante añadida

class ReglaCadena:
    def __init__(self, variables):
        """
        Implementación corregida de la Regla de la Cadena para probabilidades conjuntas.
        
        Args:
            variables: Diccionario {nombre_variable: valores_posibles}
        """
        self.variables = variables
        self.probabilidades = {}

    def agregar_probabilidad(self, variable, padres, distribucion):
        """
        Añade P(variable|padres) a la red.
        
        Args:
            variable: Variable objetivo
            padres: Lista de variables padre
            distribucion: Dict {(valor, *valores_padres): probabilidad}
        """
        # Validar que los padres existan
        for p in padres:
            if p not in self.variables:
                raise ValueError(f"Variable padre '{p}' no definida")
        
        self.probabilidades[variable] = {
            'padres': padres,
            'distribucion': distribucion
        }

    def calcular_conjunta(self):
        """Calcula P(x1, x2, ..., xn) usando la regla de la cadena"""
        # Verificar que todas las variables tengan distribuciones definidas
        for var in self.variables:
            if var not in self.probabilidades:
                raise ValueError(f"Distribución no definida para variable '{var}'")
        
        # Generar todas las combinaciones posibles de valores
        nombres_vars = list(self.variables.keys())
        combinaciones = list(product(*[self.variables[var] for var in nombres_vars]))
        resultados = {}

        for combinacion in combinaciones:
            prob_conjunta = 1.0
            escenario = dict(zip(nombres_vars, combinacion))
            
            # Aplicar regla de la cadena
            for variable in nombres_vars:
                datos = self.probabilidades[variable]
                padres_vals = tuple(escenario[p] for p in datos['padres'])
                clave = (escenario[variable],) + padres_vals
                
                prob = datos['distribucion'].get(clave, 0.0)
                prob_conjunta *= prob
            
            resultados[combinacion] = prob_conjunta
        
        return resultados

    def marginalizar(self, variable, distribucion_conjunta):
        """Marginaliza una variable de la distribución conjunta"""
        if variable not in self.variables:
            raise ValueError(f"Variable '{variable}' no existe")
            
        nombres_vars = list(self.variables.keys())
        var_index = nombres_vars.index(variable)
        resultado = defaultdict(float)
        
        for combinacion, prob in distribucion_conjunta.items():
            # Crear clave sin la variable a marginalizar
            clave = tuple(val for i, val in enumerate(combinacion) if i != var_index)
            resultado[clave] += prob
        
        # Convertir a diccionario normal
        return dict(resultado)

# Ejemplo corregido: Sistema de diagnóstico médico
if __name__ == "__main__":
    # Definir variables y sus valores posibles
    variables = {
        'Fiebre': ['Alta', 'Normal'],
        'Tos': ['Si', 'No'],
        'Enfermedad': ['Gripe', 'Resfriado', 'Ninguna']
    }

    rc = ReglaCadena(variables)

    # Definir probabilidades condicionales P(variable|padres)
    rc.agregar_probabilidad('Fiebre', [], {
        ('Alta',): 0.2,
        ('Normal',): 0.8
    })

    rc.agregar_probabilidad('Tos', [], {
        ('Si',): 0.3,
        ('No',): 0.7
    })

    rc.agregar_probabilidad('Enfermedad', ['Fiebre', 'Tos'], {
        ('Gripe', 'Alta', 'Si'): 0.6,
        ('Gripe', 'Alta', 'No'): 0.3,
        ('Gripe', 'Normal', 'Si'): 0.1,
        ('Gripe', 'Normal', 'No'): 0.05,
        ('Resfriado', 'Alta', 'Si'): 0.25,
        ('Resfriado', 'Alta', 'No'): 0.1,
        ('Resfriado', 'Normal', 'Si'): 0.3,
        ('Resfriado', 'Normal', 'No'): 0.2,
        ('Ninguna', 'Alta', 'Si'): 0.15,
        ('Ninguna', 'Alta', 'No'): 0.6,
        ('Ninguna', 'Normal', 'Si'): 0.6,
        ('Ninguna', 'Normal', 'No'): 0.75
    })

    # Calcular distribución conjunta
    conjunta = rc.calcular_conjunta()

    print("Distribución conjunta completa (primeras 5 entradas):")
    nombres_vars = list(variables.keys())
    for i, (combinacion, prob) in enumerate(conjunta.items()):
        if i >= 5:
            break
        escenario = dict(zip(nombres_vars, combinacion))
        print(f"{escenario}: {prob:.4f}")

    # Marginalizar para obtener P(Fiebre, Tos)
    print("\nDistribución marginal P(Fiebre, Tos):")
    marginal = rc.marginalizar('Enfermedad', conjunta)
    vars_restantes = [v for v in nombres_vars if v != 'Enfermedad']
    for combinacion, prob in marginal.items():
        escenario = dict(zip(vars_restantes, combinacion))
        print(f"{escenario}: {prob:.4f}")