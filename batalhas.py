import random
import time
from player import player, menu_equipar_arma



def executar_batalha(player, inimigos):
    turno = "player"



    while True:
        if turno == "fim":
            break

        # ================= TURNO DO PLAYER =================
        elif turno == "player":
            if player.arma is None:
                print("Você está sem arma")
                menu_equipar_arma(player, player.inventario)
            
            
            print()

            for i, oponente in enumerate(inimigos):
                print(f"{oponente.nome} {oponente.tipo} | nivel {oponente.nivel} | vida {oponente.vida}/{oponente.vida_max}")

            print("\n(1) atacar | (2) trocar arma | (3) bloquear | (4) dialogo | (5) fugir")
            escolha = input("Selecione sua ação:\n")




            acoes = {
                "1": lambda: player.atacar(inimigos),
                "2": lambda: menu_equipar_arma(player, player.inventario),
                "3": lambda: player.acao_bloqueio(),
                "4": lambda: player.dialogo(),
                "5": lambda: player.tentiva_fuga(inimigos),

            }

            if escolha in acoes:
                resultado = acoes[escolha]()
                if resultado == "fim":
                    return player  # ou "vitoria", etc
                elif resultado != "continuar":
                    turno = "inimigos"

            else:
                print("comando desconhecido")





        # ================= TURNO DOS INIMIGOS =================
        elif turno == "inimigos":
            print("\nturno inimigo:\n")
            time.sleep(1)
            penalidade_esq = 0
            for oponente in inimigos:
                penalidade_esq += oponente.disparar_habilidade(player, "ao_ser_atacado")

            atacante = random.choice(inimigos)

            dano = atacante.dano

            if player.esquiva(atacante.nivel, penalidade=penalidade_esq):
                dano = 0


            if player.bloqueando:
                if player.tentar_bloquear(atacante):
                    print("voce bloqueou o ataque")
                    dano = 0
                else:
                    print("bloqueio falhou")

                player.bloqueando = False


            player.vida -= dano

            if dano > 0:
                print(f"{atacante.nome} {atacante.tipo} te causou {dano} de dano")

            atacante.disparar_habilidade(player, "ao_atacar")
            if player.vida <= 0:
                print("voce morreu")
                return player

            print(f"sua vida atual: {player.vida}")
            time.sleep(1)

            turno = "player"

