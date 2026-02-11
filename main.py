import random
import time, keyboard, os
from player import player, mostrar_inventario
from caminho_1 import executar_caminho1



while True:
    # vida do player +20 por nivel
    nome = input("Digite seu nome de jogador:\n")
    player = player(nome)
    print("\nvc acorda no meio do nada nivel 1 com apenas um pedaço de madeira\n")
    time.sleep(0.5)
    guardar = input("voce percebe que tem um inventario com 3 slots, guardar o pedaço de madeira? (s/n)\n")
    
    if guardar == "s":
        player.desequipar_arma()

        


    print()
    time.sleep(0.8)
    print("olhando para frente voce ve 3 caminhos\n")
    print("(1)Caminho: facil com recompensas pequenas")

    p1 = input("para qual deles vc vai?\n")

    if p1 == "1":
        caminho_1 = executar_caminho1(player)
        print("\n\nCABO")
        break
    #if player.vida <= 0:
        r = input("Tentar denovo? (s/n): ")
        if r.lower() != "s":
            break


