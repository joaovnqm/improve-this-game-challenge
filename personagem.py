from abc import ABC
import random


class Personagem(ABC):
    """Classe base para personagens (heróis, vilões, NPCs).

    Fornece atributos comuns: nome, idade, vida, ataque e defesa, além de
    coleções para habilidades e itens. Métodos retornam mensagens de ação
    que podem ser registradas pelo sistema de jogo.
    """

    def __init__(self, nome, idade, vida, ataque=10, defesa=5):
        self.nome = nome
        self.idade = idade
        self.vida = vida
        self.ataque = ataque
        self.defesa = defesa
        self.habilidades = []
        self.itens = {}
        self.status = {}

    def to_dict(self):
        return {
            'nome': self.nome,
            'idade': self.idade,
            'vida': self.vida,
            'ataque': self.ataque,
            'defesa': self.defesa,
            'habilidades': list(self.habilidades),
            'itens': dict(self.itens),
            'status': dict(self.status),
        }

    def upgrade_vida(self, incremento=10):
        self.vida += incremento
        return f'Vida de {self.nome} aumentou em {incremento}. (Agora: {self.vida})'

    def downgrade_vida(self, dano=15):
        self.vida = max(0, self.vida - dano)
        return f'{self.nome} recebeu {dano} de dano. (Vida: {self.vida})'

    def update_nome(self, nome_editado):
        antigo = self.nome
        self.nome = nome_editado
        return f'Nome atualizado: {antigo} → {self.nome}'

    def receber_dano(self, dano):
        self.vida = max(0, self.vida - dano)
        return f'{self.nome} recebeu {dano} de dano. (Vida agora: {self.vida})'

    def atacar(self, alvo):
        variacao = random.randint(-2, 2)
        dano = max(1, self.ataque - getattr(alvo, 'defesa', 0) + variacao)
        mensagem = alvo.receber_dano(dano)
        return f'{self.nome} atacou {alvo.nome} causando {dano} de dano. / {mensagem}'

    def dialogar(self, outro, mensagem):
        return f'{self.nome}: {mensagem}'

    def __str__(self):
        return f'Personagem: {self.nome}, Idade: {self.idade}, Vida: {self.vida}, Atq: {self.ataque}, Def: {self.defesa}'
