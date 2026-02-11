import time
from batalhas import executar_batalha
from enemys import slime

def executar_caminho1(player):
    while True:
        print("\nvc encontra 3 slimes\n")
        print(
            "(1)passar escondido | (2)correr e dar a volta | (3)enfrentar eles | (4)observar eles"
        )
        c1p1 = input("oq vc faz?\n")
        if c1p1 == "1":
            print("vc tenta passar escondindo\n")
            time.sleep(1.5)
            print("mas vc acaba sendo visto\n")
            time.sleep(0.5)
            print("voce entra em batalha\n")
            time.sleep(1)


            grupo_inimigos = [slime() for _ in range(3)]

            resultado = executar_batalha(player, grupo_inimigos)
        return resultado
