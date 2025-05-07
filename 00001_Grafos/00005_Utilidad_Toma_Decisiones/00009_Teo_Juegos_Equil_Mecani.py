import numpy as np
from itertools import product

class Juego:
    def __init__(self, jugadores, estrategias, recompensas):
        # Inicializa el juego con jugadores, sus estrategias y recompensas por perfil
        self.jugadores = jugadores
        self.estrategias = estrategias
        self.recompensas = recompensas
        self.n_jugadores = len(jugadores)

    def encontrar_equilibrios_nash(self):
        # Busca todos los equilibrios de Nash en estrategias puras
        equilibrios = []
        for perfil in product(*self.estrategias.values()):  # Combinaciones posibles
            es_equilibrio = True
            for i, jugador in enumerate(self.jugadores):
                pago_actual = self.recompensas[perfil][i]
                mejor_pago = -np.inf
                for estrategia in self.estrategias[jugador]:  # Probar otras jugadas del jugador
                    nuevo_perfil = list(perfil)
                    nuevo_perfil[i] = estrategia
                    pago = self.recompensas[tuple(nuevo_perfil)][i]
                    mejor_pago = max(mejor_pago, pago)
                if mejor_pago > pago_actual:  # Si puede mejorar, no es equilibrio
                    es_equilibrio = False
                    break
            if es_equilibrio:
                equilibrios.append(perfil)
        return equilibrios

    def mecanismo_vickrey_auction(self, valores, verbose=True):
        # Subasta de segundo precio (Vickrey)
        participantes = list(valores.keys())
        if len(participantes) < 2:
            raise ValueError("Se necesitan al menos 2 jugadores")
        
        # Ordenar por mayor oferta
        valores_ordenados = sorted(valores.items(), key=lambda x: -x[1])
        ganador = valores_ordenados[0][0]           # Mayor oferta
        precio = valores_ordenados[1][1]            # Segundo mayor valor
        
        if verbose:
            print("\nResultado Subasta Vickrey:")
            print(f"Ganador: {ganador} (Valoración: {valores[ganador]})")
            print(f"Precio a pagar: {precio}")
            print(f"Utilidad del ganador: {valores[ganador] - precio}")
        
        return ganador, precio

# Ejemplo 1: Dilema del Prisionero
if __name__ == "__main__":
    print("=== Dilema del Prisionero ===")
    juego_prisionero = Juego(
        jugadores=["Prisionero A", "Prisionero B"],
        estrategias={
            "Prisionero A": ["Confesar", "Callar"],
            "Prisionero B": ["Confesar", "Callar"]
        },
        recompensas={
            ("Confesar", "Confesar"): (-5, -5),
            ("Confesar", "Callar"): (0, -10),
            ("Callar", "Confesar"): (-10, 0),
            ("Callar", "Callar"): (-1, -1)
        }
    )
    
    equilibrios = juego_prisionero.encontrar_equilibrios_nash()
    print("\nEquilibrios de Nash encontrados:")
    for eq in equilibrios:
        print(f"- {eq[0]} vs {eq[1]}")

    # Ejemplo 2: Subasta de Vickrey
    print("\n=== Subasta Vickrey (Segundo Precio) ===")
    valores = {
        "Alice": 120,
        "Bob": 100,
        "Charlie": 150,
        "Diana": 90
    }

    juego_subasta = Juego(jugadores=list(valores.keys()),
                          estrategias={},
                          recompensas={})
    
    juego_subasta.mecanismo_vickrey_auction(valores)
