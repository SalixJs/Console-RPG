import random
from defs import entidade
from player import player

tipos_slime = {
    "comum": {
        "vida": 1.0,
        "dano": 1.0,
        "esquiva_bonus": 0.0,
        "habilidades": []
    },
    "acido": {
        "vida": 0.8,
        "dano": 0.9,
        "esquiva_bonus": 0.0,
        "habilidades": [
            {
                "tipo": "passiva",
                "gatilho": "ao_atacar",
                "efeito": "corrosao",
                "chance": 25,
                "valor": 1
            },
            {
                "tipo": "passiva",
                "gatilho": "ao_atacar",
                "efeito": "dano_continuo",
                "chance": 25,
                "valor": 1
            }
        ]
    },
    "viscoso": {
        "vida": 1.2,
        "dano": 0.8,
        "esquiva_bonus": 0.0,
        "habilidades": [
            {
                "tipo": "passiva",
                "gatilho": "fora_combate",
                "efeito": "penalidade_fuga",
                "valor": 0.15
            },
            {
                "tipo": "passiva",
                "gatilho": "ao_ser_atacado",
                "efeito": "penalidade_esquiva",
                "valor": 0.10
            }
        ]
    },
    "explosivo": {
        "vida": 0.6,
        "dano": 1.3,
        "esquiva_bonus": 0.0,
        "habilidades": [
            {
                "tipo": "passiva",
                "gatilho": "ao_morrer",
                "efeito": "explosao",
                "valor": 10
            }
        ]
    },
    "leve": {
        "vida": 0.7,
        "dano": 0.9,
        "esquiva_bonus": 0.15,
        "habilidades": [
            {
                "tipo": "passiva",
                "gatilho": "ao_atacar",
                "efeito": "chance_ataque_extra",
                "chance": 25
            }
        ]
    },
    "pesado": {
        "vida": 1.5,
        "dano": 1.1,
        "esquiva_bonus": -0.2,
        "habilidades": [
            {
                "tipo": "passiva",
                "gatilho": "ao_ser_atacado",
                "efeito": "reduzir_ataque_inimigo",
                "valor": 0.25
            }
        ]
    }
}


def calc_vida(nivel, tipo_slime, constituicao):
    mult_vida = tipos_slime[tipo_slime]["vida"]
    vida_base = 20 + ((nivel - 1) + (constituicao * 0.5))
    return round(vida_base * mult_vida)


def calc_dano(nivel, tipo_slime, forca):
    mult_dano = tipos_slime[tipo_slime]["dano"]
    dano_base = 2 + (nivel * 1) + (forca * 0.5)
    return round(dano_base * mult_dano)


class slime(entidade):
    def __init__(self):
        self.nome = "slime"
        self.nivel = random.randint(1, 5)
        self.tipo = random.choice(list(tipos_slime.keys()))
        self.habilidade = tipos_slime[self.tipo]["habilidades"]


        self.stats = {
            "forca": 5,  # dano físico corpo a corpo
            "destreza": 5,  # chance de acerto, esquiva e crítico
            "constituicao": 5,  # vida máxima e resistência
            "inteligencia": 5,  # habilidades especiais / diálogo técnico   SABER
            "sabedoria": 5,  # percepção, decisões em diálogo, status    ENTENDER
            "carisma": 0  # diálogo, intimidação, persuasão   CONVENCER
        }


        self.vida = calc_vida(
            self.nivel,
            self.tipo,
            self.stats["constituicao"]
        )

        self.vida_max = self.vida


        self.dano = calc_dano(
            self.nivel,
            self.tipo,
            self.stats["forca"]
        )

        super().__init__(
            self.nome,
            self.vida,
            self.vida_max,
            self.nivel
        )


    def disparar_habilidade(self, alvo, gatilho):
        valor_acumulado = 0
        for hab in self.habilidade:
            if hab["gatilho"] != gatilho:
                continue

            chance = hab.get("chance", 100)
            if random.randint(1, 100) <= chance:
                if hab["efeito"] == "corrosao":
                    if alvo.defesa == 0:
                        return

                    alvo.defesa -= hab["valor"]
                    print(f"a acidez do {self.nome} {self.tipo} correu a defesa")
                    print(f"sua defesa caiu para {alvo.defesa}")

                elif hab["efeito"] == "dano_continuo":
                    dano_con = hab["valor"]
                    print(f"o {self.nome} {self.tipo} jogou acido em voce")
                    print(f"voce tomara {dano_con} por 2 rodadas")

                elif hab["efeito"] == "penalidade_fuga":
                    print(f"o {self.nome} {self.tipo} dificulta a fuga")
                    valor_acumulado = hab["valor"]

                elif hab["efeito"] == "penalidade_esquiva":
                    print(f"o {self.nome} {self.tipo} dificulta seus movimentos")
                    valor_acumulado = hab["valor"]

                elif hab["efeito"] == "explosao":
                    dano_exp = hab["valor"]
                    alvo.receber_dano(dano_exp)
                    print(f"o {self.nome} {self.tipo} explodiu e te causou {dano_exp} de dano")

                elif hab["efeito"] == "chance_ataque_extra":
                    print(f"o {self.nome} {self.tipo} atacou de novo")
                    alvo.receber_dano(self.dano)

                elif hab["efeito"] == "reduzir_ataque_inimigo":
                    print(f"o {self.nome} {self.tipo} diminuiu seu ataque")
                    valor_acumulado = hab["valor"]



        return valor_acumulado