import random
from armas import criar_madeira
from defs import entidade


class player(entidade):
    def __init__(self, nome,):
        super().__init__(nome, 100, 100, 1)

        self.stats = {
            "forca": 5,  # dano físico corpo a corpo
            "destreza": 5,  # chance de acerto, esquiva e crítico
            "constituicao": 5,  # vida máxima e resistência
            "inteligencia": 5,  # habilidades especiais / diálogo técnico   SABER
            "sabedoria": 5,  # percepção, decisões em diálogo, status    ENTENDER
            "carisma": 5  # diálogo, intimidação, persuasão   CONVENCER
        }

        self.nome = nome

        self.vida_max = 50 + (self.stats["constituicao"] * 10)
        self.vida = self.vida_max

        self.defesa = 25
        self.xp = 0
        self.xp_max = 100
        self.pontos = 0
        self.tentativas = 0
        self.bloqueando = False
        self.arma = criar_madeira()

        self.inventario = []
        self.inventario.extend([None, None, None])

    def atacar(self, lista_inimigos, penalidade=0):
        escolha_alvo = int(input("escolha seu alvo:\n"))
        alvo = lista_inimigos[escolha_alvo - 1]

        arma = self.arma

        if arma is None:
            print("voce esta desarmado")
            return False


        forca = self.stats["forca"]
        destreza = self.stats["destreza"]

        dano = arma.dano + int(forca * 0.4) + random.randint(0, 2) - round(penalidade * 100)

        crit_chance = arma.crit_chance + (destreza * 0.01)

        crit_chance = min(0.5, crit_chance)

        if random.random() < crit_chance:
            dano = int(dano * arma.crit_mult)
            print("critico")

        dano = max(1, dano)

        arma.durabilidade -= 1
        alvo.vida -= dano

        print(f"Você causou {dano} de dano com {arma.nome}")

        if arma.durabilidade <= 0:
            print(f"{arma.nome} quebrou!")
            self.arma = None

        if alvo.vida > 0:
            alvo.disparar_habilidade(self, "ao_ser_atacado")
        if alvo.vida <= 0:
            alvo.disparar_habilidade(self, "ao_morrer")
            lista_inimigos.remove(alvo)

        if not lista_inimigos:
            print("Você ganhou!")
            self.tentativas = 0

            return "fim"

        return "inimigos"


    def acao_bloqueio(self):
        print(f"voce entrou em posicao de bloqueio")
        self.bloqueando = True
        return "inimigos"


    def tentar_bloquear(self, inimigo):
        p_nivel = self.nivel
        i_nivel = inimigo.nivel

        status_const = self.stats["constituicao"]

        diferenca = p_nivel - i_nivel
        chance = 30 + (diferenca * 2) + (status_const * 2)
        chance_final = max(20, min(80, int(chance)))

        if random.randint(1, 100) <= chance_final:

            return True
        return False


    def dialogo(self):
        tentativas = self.tentativas

        carisma = self.stats["carisma"]


        chance = (5 + (carisma * 3) - (tentativas * 10))

        chance = max(2, min(50, int(chance)))

        roll = random.randint(1, 100)
        self.tentativas = tentativas + 1

        if roll <= chance:
            print("voce conseguiu acalmar a situacao")
            return "fim"

        print("voce falhou em acalmar")
        return False


    def fugir(self, inimigos, penalidade=0):
        nivel_inimigos = sum(i.nivel for i in inimigos)/ len(inimigos)
        diferenca = self.nivel - nivel_inimigos

        destreza = self.stats["destreza"]

        chance = 30 + (destreza * 4) + (diferenca * 3) - round(penalidade * 100)
        chance = max(5, min(90, int(chance)))


        if random.randint(1,100) <= chance:
            print("voce conseguiu fugir da batalha")
            return "fim"

        print("os inimigos nao te deixaram fugir")
        return False


    def tentiva_fuga(self, inimigos):
        penalidade_total = 0

        for inimigo in inimigos:
            for hab in inimigo.habilidade:
                if hab["gatilho"] == "fora_combate" and hab["efeito"] == "penalidade_fuga":
                    penalidade_total += hab["valor"]
                    print(f"o {inimigo.nome} {inimigo.tipo} dificulta a fuga.")
        if penalidade_total > 0:
            print(f"penalidade {int(penalidade_total*100)}")

        return self.fugir(inimigos, penalidade_total)

    def equipar_arma(self, indice):
        nova = self.inventario[indice]

        if nova is None:
            print("espaco vazio")
            return

        antiga = self.arma
        self.arma = nova
        self.inventario[indice] = antiga
        print(f"voce equipou {nova.nome}")


    def desequipar_arma(self):
        if self.arma is None:
            print("voce nao tem arma equipada")
            return

        for i in range(len(self.inventario)):
            if self.inventario[i] is None:
                arma_guardada = self.arma
                self.inventario[i] = arma_guardada

                print(f"voce guardou {arma_guardada.nome} no espaco {i + 1}")

                self.arma = None
                return

        print("inventario cheio")


    def esquiva(self, nivel_inimigo, penalidade=0):

        destreza = self.stats["destreza"]


        chance = 10 + (destreza * 2) - (nivel_inimigo * 1.5) - round(penalidade * 100)
        chance = max(5, min(90, chance))

        roll = random.randint(1, 100)

        if roll <= chance:
            print("voce esquivou")
            return True

        return False


    def subir_nivel(self):
        self.xp -= self.xp_max
        self.nivel += 1
        self.xp_max = int(player.xp_max * 1.35 + 20)

        print(f"voce subiu para o nivel {self.nivel}")

        distribuir_pontos()


    def ganhar_xp(self, quantidade):
        self.xp += quantidade

        if self.xp == self.xp_max:
            self.subir_nivel()




def distribuir_pontos(player):
        player.pontos += 3

        while player.pontos > 0:
            print("escolha um atributo para upar")
            for stat, valor in player.stats.items():
                print(f"{stat}: {valor}")

                escolha = input("> ").lower()

                if escolha in player.stats:
                    player.stats[escolha] += 1
                    player.pontos -= 1
                else:
                    print("atributo invalido")




def mostrar_inventario(inventario):
    print("\n=== INVENTÁRIO ===")

    for i, item in enumerate(inventario):
        slot_nome = f"Espaço {i + 1}"

        if item is None:
            print(f"{slot_nome}: [vazio]")
        else:
            print(
                f"{slot_nome}: {item.nome} "
                f"(Nv {item.nivel}) | "
                f"Dano {item.dano} | "
                f"Dur {item.durabilidade}"
            )
    print("==================\n")



def menu_equipar_arma(player, inventario):
    mostrar_inventario(inventario)

    escolha = input("Escolha o slot (1/2/3) ou 0 para cancelar:\n")

    if escolha == "0":
        return "continuar"

    if escolha.isdigit():
        indice = int(escolha) - 1

        if 0 <= indice < len(inventario):
            player.equipar_arma(indice)
            return "continuar"
        else:
            print("slot vazio")
    else:
        print("digite apenas numeros")


    return "continuar"







#endregion

#region COISAS DO PLAYER

#region XP
















#endregion

#region MENUS


def mostrar_xp(player):
    total = 20
    cheio = int((player["xp"] / player["xp_max"]) * total)
    barra = "█" * cheio + "-" * (total - cheio)

    print(f"XP [{barra}] {player['xp']}/{player['xp_max']}")









#endregion

#endregion





