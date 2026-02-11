import os


class entidade:
    def __init__(self, nome, vida, vida_max, nivel):
        self.nome = nome
        self.vida = vida
        self.vida_max = vida_max
        self.nivel = nivel


    def receber_dano(self, dano):
        self.vida -= dano




def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')