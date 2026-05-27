from personagem import Personagem
import random


class Vilao(Personagem):
    """Vilão com nível de maldade que influencia atributos e comportamento."""

    def __init__(self, nome, idade, vida, maldade='Média', ataque=None, defesa=None):
        # ajusta ataque/defesa baseado na maldade
        niveis_validos = ['Baixa', 'Média', 'Alta']
        if maldade not in niveis_validos:
            raise ValueError(f"Nível de maldade inválido! Escolha entre {niveis_validos}")
        base_atq = {'Baixa': 8, 'Média': 12, 'Alta': 18}
        base_def = {'Baixa': 4, 'Média': 6, 'Alta': 10}
        atk = ataque if ataque is not None else base_atq[maldade]
        df = defesa if defesa is not None else base_def[maldade]
        super().__init__(nome, idade, vida, ataque=atk, defesa=df)
        self.maldade = maldade
        self.habilidades.extend(['Intimidar', 'Investida'])

    def ataque_especial(self, alvo):
        variacao = random.randint(0, 5)
        dano = max(1, self.ataque + variacao - getattr(alvo, 'defesa', 0))
        msg = alvo.receber_dano(dano)
        return f'{self.nome} usou Investida em {alvo.nome} causando {dano}. / {msg}'

    def intimidar(self, alvo):
        # reduz temporariamente a defesa do alvo (simulado como dano leve + mensagem)
        dano = 3
        msg = alvo.receber_dano(dano)
        return f'{self.nome} intimidou {alvo.nome}, causando {dano} de dano psicológico. / {msg}'

    def __str__(self):
        return f'Vilão: {self.nome}, Vida: {self.vida}, Atq: {self.ataque}, Def: {self.defesa}, Maldade: {self.maldade}'
