from itertools import product
from collections import defaultdict

class ReglaCadena:
    def __init__(self, variables):
        self.variables = variables                      # {variable: [valores]}
        self.probabilidades = {}                        # almacena CPTs y padres

    def agregar_probabilidad(self, variable, padres, distribucion):
        for p in padres:                                # verificar padres definidos
            if p not in self.variables:
                raise ValueError(f"Padre no definido: {p}")
        self.probabilidades[variable] = {
            'padres': padres,
            'distribucion': distribucion                # {(valor, *valores_padres): prob}
        }

    def calcular_conjunta(self):
        for var in self.variables:
            if var not in self.probabilidades:          # validar CPTs completas
                raise ValueError(f"Falta CPT de: {var}")
        nombres = list(self.variables.keys())
        combinaciones = list(product(*[self.variables[v] for v in nombres]))
        resultados = {}

        for c in combinaciones:                         # para cada combinación posible
            prob = 1.0
            estado = dict(zip(nombres, c))              # estado = {'Var': valor}
            for v in nombres:
                datos = self.probabilidades[v]
                padres = tuple(estado[p] for p in datos['padres'])
                clave = (estado[v],) + padres
                prob *= datos['distribucion'].get(clave, 0.0)
            resultados[c] = prob                        # guardar prob conjunta
        return resultados

    def marginalizar(self, variable, conjunta):
        if variable not in self.variables:
            raise ValueError(f"Variable inválida: {variable}")
        idx = list(self.variables).index(variable)
        resultado = defaultdict(float)
        for c, p in conjunta.items():
            clave = tuple(v for i, v in enumerate(c) if i != idx)
            resultado[clave] += p                       # suma marginal
        return dict(resultado)

# Ejemplo de uso
if __name__ == "__main__":
    variables = {
        'Fiebre': ['Alta', 'Normal'],
        'Tos': ['Si', 'No'],
        'Enfermedad': ['Gripe', 'Resfriado', 'Ninguna']
    }

    rc = ReglaCadena(variables)

    rc.agregar_probabilidad('Fiebre', [], {
        ('Alta',): 0.2, ('Normal',): 0.8
    })
    rc.agregar_probabilidad('Tos', [], {
        ('Si',): 0.3, ('No',): 0.7
    })
    rc.agregar_probabilidad('Enfermedad', ['Fiebre', 'Tos'], {
        ('Gripe', 'Alta', 'Si'): 0.6, ('Gripe', 'Alta', 'No'): 0.3,
        ('Gripe', 'Normal', 'Si'): 0.1, ('Gripe', 'Normal', 'No'): 0.05,
        ('Resfriado', 'Alta', 'Si'): 0.25, ('Resfriado', 'Alta', 'No'): 0.1,
        ('Resfriado', 'Normal', 'Si'): 0.3, ('Resfriado', 'Normal', 'No'): 0.2,
        ('Ninguna', 'Alta', 'Si'): 0.15, ('Ninguna', 'Alta', 'No'): 0.6,
        ('Ninguna', 'Normal', 'Si'): 0.6, ('Ninguna', 'Normal', 'No'): 0.75
    })

    conjunta = rc.calcular_conjunta()
    print("Distribución conjunta (primeras 5):")
    for i, (c, p) in enumerate(conjunta.items()):
        if i >= 5: break
        print(f"{dict(zip(variables, c))}: {p:.4f}")

    print("\nDistribución marginal P(Fiebre, Tos):")
    marginal = rc.marginalizar('Enfermedad', conjunta)
    for c, p in marginal.items():
        print(f"{dict(zip(['Fiebre', 'Tos'], c))}: {p:.4f}")
