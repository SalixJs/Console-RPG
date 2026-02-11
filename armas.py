import random

class criar_madeira:
    def __init__(self):
        self.nome = "pedaco de madeira"
        self.nivel = random.choice([0,1])
        self.dano = 3 + self.nivel
        self.crit_chance = 0.05 + (self.nivel * 0.05)
        self.crit_mult = 1.5
        self.durabilidade = 20 + (self.nivel * 5)

