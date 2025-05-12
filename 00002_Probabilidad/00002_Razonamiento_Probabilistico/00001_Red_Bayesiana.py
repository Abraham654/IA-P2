from collections import defaultdict
import itertools

class RedBayesiana:
    def __init__(self):
        self.nodos = {}  # nombre: [valores posibles]
        self.padres = defaultdict(list)  # nombre: [padres]
        self.cpts = defaultdict(dict)  # nombre: {(valor, *valores_padres): prob}

    def agregar_nodo(self, nombre, valores, padres=None):
        self.nodos[nombre] = valores
        if padres:
            self.padres[nombre] = padres
            for comb in itertools.product(*[self.nodos[p] for p in padres]):
                for val in valores:
                    self.cpts[nombre][(val,) + comb] = 0.0

    def agregar_cpt(self, nodo, distribucion):
        for clave, prob in distribucion.items():
            if clave in self.cpts[nodo]:
                self.cpts[nodo][clave] = prob

    def inferencia_por_enum(self, consulta, evidencia={}):
        for var in consulta + list(evidencia):
            if var not in self.nodos:
                raise ValueError(f"{var} no definida")
        ocultas = [v for v in self.nodos if v not in consulta and v not in evidencia]
        probas = defaultdict(float)

        for config in self._combinaciones(ocultas):
            escen = {**evidencia, **config}
            for var in consulta:
                if var not in escen:
                    escen[var] = self.nodos[var][0]
            p = 1.0
            for nodo in self.nodos:
                val = escen[nodo]
                padres_val = [escen[p] for p in self.padres[nodo]]
                clave = (val,) + tuple(padres_val)
                p *= self.cpts[nodo].get(clave, 0.0)
            clave_consulta = tuple(escen[v] for v in consulta)
            probas[clave_consulta] += p

        total = sum(probas.values())
        return {k: v / total for k, v in probas.items()} if total > 0 else {}

    def _combinaciones(self, variables):
        if not variables:
            return [{}]
        dominios = [self.nodos[v] for v in variables]
        for c in itertools.product(*dominios):
            yield dict(zip(variables, c))

# Ejemplo de uso
if __name__ == "__main__":
    rb = RedBayesiana()

    rb.agregar_nodo('Fiebre', ['Alta', 'Normal'])
    rb.agregar_nodo('Tos', ['Si', 'No'])
    rb.agregar_nodo('Enfermedad', ['Gripe', 'Resfriado', 'Ninguna'], padres=['Fiebre', 'Tos'])

    rb.agregar_cpt('Fiebre', {
        ('Alta',): 0.2,
        ('Normal',): 0.8
    })
    rb.agregar_cpt('Tos', {
        ('Si',): 0.3,
        ('No',): 0.7
    })
    rb.agregar_cpt('Enfermedad', {
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

    print("P(Enfermedad | Fiebre=Alta, Tos=Si):")
    resultado = rb.inferencia_por_enum(['Enfermedad'], {'Fiebre': 'Alta', 'Tos': 'Si'})
    for enf, p in resultado.items():
        print(f"{enf[0]}: {p:.2f}")
