from personagem import Personagem
import random


class Heroi(Personagem):
    """Herói com habilidades próprias (salvar_refem, usar_pocao, etc.)."""

    def __init__(self, nome, idade, vida, ataque=12, defesa=6, poder=None):
        super().__init__(nome, idade, vida, ataque, defesa)
        self.poder = poder
        self.itens.setdefault('pocao', 1)
        self.habilidades.extend(['Golpe', 'Socorrer'])
        self.energia_max = 100
        self.energia = self.energia_max
        self.tipos_ataque = {
            'leve': {'custo': 5, 'descr': 'Ataque rápido, baixo custo'},
            'forte': {'custo': 12, 'descr': 'Ataque forte, maior dano'},
            'habilidade': {'custo': 20, 'descr': 'Usa habilidade especial'},
            'ult': {'custo': 40, 'descr': 'Ataque ultimate, muito dano'},
        }
        self.ult_cooldown = 0

    def usar_pocao(self):
        qtd = self.itens.get('pocao', 0)
        if qtd <= 0:
            return f'{self.nome} tentou usar uma poção, mas não tem nenhuma.'
        
        cura = 30
        self.vida += cura
        self.itens['pocao'] = qtd - 1
        return f'{self.nome} usou uma poção e recuperou {cura} de vida. (Vida: {self.vida})'

    def salvar_refem(self, refem, captor):
        roll = random.randint(1, 100)
        chance = 50 + (self.ataque - getattr(captor, 'ataque', 10)) * 2
        success = roll <= max(10, min(90, chance))
        if success:
            refem.status['livre'] = True
            return f'{self.nome} libertou {refem.nome}! (roll {roll} <= {chance})'
        
        else:
            return f'{self.nome} falhou ao tentar libertar {refem.nome}. (roll {roll} > {chance})'

    def usar_habilidade(self, nome_hab, alvo):
        if nome_hab not in self.habilidades:
            return f'{self.nome} não conhece a habilidade "{nome_hab}".'

        if nome_hab == 'Golpe':
            dano = max(1, self.ataque + 5 - getattr(alvo, 'defesa', 0))
            msg = alvo.receber_dano(dano)
            return f'{self.nome} usou Golpe em {alvo.nome} causando {dano}. / {msg}'
        
        if nome_hab == 'Socorrer':
            cura = 10
            self.vida += cura
            return f'{self.nome} usou Socorrer e recuperou {cura} de vida. (Vida: {self.vida})'
        
        return f'Habilidade {nome_hab} executada.'

    def executar_ataque(self, tipo, alvo, current_round=None):
        tipo = tipo.lower()
        if tipo not in self.tipos_ataque:
            return self.executar_ataque('leve', alvo, current_round=current_round)

        custo = self.tipos_ataque[tipo]['custo']
        if self.energia < custo:
            return False, f'{self.nome} tentou usar {tipo}, mas não tem energia suficiente ({self.energia}/{custo}).'

        if tipo == 'ult':
            if current_round is None or current_round < 3:
                return False, f'Ultimate só disponível a partir da rodada 3. (rodada atual: {current_round})'
            
            if getattr(self, 'ult_cooldown', 0) > 0:
                return False, f'{self.nome} tentou usar ultimate, mas está em cooldown por {self.ult_cooldown} rodada(s).'

        self.energia -= custo

        if tipo == 'leve':
            variacao = 0
            dano = max(1, self.ataque + variacao - getattr(alvo, 'defesa', 0))

        elif tipo == 'forte':
            variacao = 2
            dano = max(1, self.ataque + 6 + variacao - getattr(alvo, 'defesa', 0))

        elif tipo == 'habilidade':
            if 'Golpe' in self.habilidades:
                dano = max(1, self.ataque + 8 - getattr(alvo, 'defesa', 0))

            else:
                dano = max(1, self.ataque + 4 - getattr(alvo, 'defesa', 0))

        elif tipo == 'ult':
            dano = max(1, int(self.ataque * 2.2) - getattr(alvo, 'defesa', 0))
            self.ult_cooldown = 3

        else:
            dano = max(1, self.ataque - getattr(alvo, 'defesa', 0))

        msg = alvo.receber_dano(dano)
        return True, f'{self.nome} usou {tipo} em {alvo.nome}, custo {custo} de energia, causando {dano} de dano. / {msg} (Energia restante: {self.energia})'

    def mostrar_tipos_ataque(self):
        linhas = []
        for k, v in self.tipos_ataque.items():
            linhas.append(f'{k} - custo {v["custo"]}: {v["descr"]}')

        return '\n'.join(linhas)

    def __str__(self):
        return f'Herói: {self.nome}, Vida: {self.vida}, Atq: {self.ataque}, Def: {self.defesa}, Poder: {self.poder}'