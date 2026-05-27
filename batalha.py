import random


class Batalha:
    """Gerencia batalhas entre listas de heróis e vilões, registrando ações."""

    def __init__(self, herois, viloes):
        self.herois = herois
        self.viloes = viloes
        self.log = []
        self.interactive = False

    def vivos(self, grupo):
        return [p for p in grupo if getattr(p, 'vida', 0) > 0]

    def imprimir_status(self):
        print('\n--- Status ---')
        for heroi in self.herois:
            print(f'Herói -> {heroi}')
            
        for vilao in self.viloes:
            print(f'Vilão -> {vilao}')
        print('--------------\n')

    def registrar(self, mensagem):
        self.log.append(mensagem)
        print(mensagem)

    def rodada(self):
        # Turno dos herois
        for heroi in self.vivos(self.herois):
            if not self.vivos(self.viloes):
                break

            if getattr(self, 'interactive', False):
                print(f"\nTurno do herói: {heroi.nome} (Vida: {heroi.vida}, Energia: {getattr(heroi,'energia',0)}/{getattr(heroi,'energia_max',0)})")
                if heroi.vida <= 25 and heroi.itens.get('pocao', 0) > 0:
                    escolha_p = input(f'Deseja usar uma poção? (s/n) > ').strip().lower()
                    if escolha_p == 's':
                        msg = heroi.usar_pocao()
                        self.registrar(msg)
                        continue

                viloes_vivos = self.vivos(self.viloes)
                print('Vilões disponíveis:')
                for i, v in enumerate(viloes_vivos, 1):
                    print(f'  {i}) {v.nome} (Vida: {v.vida})')

                if hasattr(heroi, 'mostrar_tipos_ataque'):
                    print('\nTipos de ataque:')
                    print(heroi.mostrar_tipos_ataque())

                tipo = input('Escolha o tipo de ataque (nome) > ').strip().lower()
                try:
                    idx = int(input('Escolha o número do vilão alvo > ').strip()) - 1
                    alvo = viloes_vivos[idx]

                except Exception:
                    alvo = random.choice(viloes_vivos)

                if hasattr(heroi, 'executar_ataque'):
                    while True:
                        ok, message = heroi.executar_ataque(tipo, alvo, current_round=getattr(self, 'current_round', None))
                        if ok:
                            self.registrar(message)
                            break

                        print(message)
                        escolha = input('Deseja escolher outro ataque? (s para escolher / qualquer outra tecla para atacar normalmente) > ').strip().lower()
                        if escolha == 's':
                            tipo = input('Escolha o tipo de ataque (nome) > ').strip().lower()
                            try:
                                idx = int(input('Escolha o número do vilão alvo > ').strip()) - 1
                                alvo = viloes_vivos[idx]
                            except Exception:
                                alvo = random.choice(viloes_vivos)
                            continue
                        else:
                            # fallback: ataque simples
                            msg = heroi.atacar(alvo)
                            self.registrar(msg)
                            break

                else:
                    message = heroi.atacar(alvo)
                    self.registrar(message)
                continue

            if heroi.vida <= 25 and heroi.itens.get('pocao', 0) > 0:
                message = heroi.usar_pocao()
                self.registrar(message)
                continue

            alvo = random.choice(self.vivos(self.viloes))

            if hasattr(heroi, 'executar_ataque') and random.random() < 0.6:
                tipo = random.choices(['leve','forte','habilidade','ult'], weights=[40,30,20,10])[0]
                ataque_bem_sucedido, message = heroi.executar_ataque(tipo, alvo, current_round=getattr(self, 'current_round', None))
                if ataque_bem_sucedido:
                    self.registrar(message)
                else:
                    if getattr(heroi, 'energia', 0) >= heroi.tipos_ataque.get('leve', {}).get('custo', 0):
                        ataque_bem_sucedido2, msg2 = heroi.executar_ataque('leve', alvo, current_round=getattr(self, 'current_round', None))
                        if ataque_bem_sucedido2:
                            self.registrar(msg2)
                        else:
                            self.registrar(msg2)
                    else:
                        msg3 = heroi.atacar(alvo)
                        self.registrar(msg3)

                continue

            elif 'Golpe' in heroi.habilidades and random.random() < 0.4:
                message = heroi.usar_habilidade('Golpe', alvo)

            else:
                message = heroi.atacar(alvo)

            self.registrar(message)

        # Turno dos vilões
        for vilao in self.vivos(self.viloes):
            if not self.vivos(self.herois):
                break
            alvo = random.choice(self.vivos(self.herois))

            if random.random() < 0.35 and hasattr(vilao, 'ataque_especial'):
                message = vilao.ataque_especial(alvo)

            else:
                message = vilao.atacar(alvo)

            self.registrar(message)

    def run(self):
        round_num = 1
        print('Iniciando batalha!')
        while self.vivos(self.herois) and self.vivos(self.viloes):
            print(f'\n=== Rodada {round_num} ===')
            self.current_round = round_num
            self.rodada()
            for heroi in self.herois:
                if getattr(heroi, 'ult_cooldown', 0) > 0:
                    heroi.ult_cooldown = max(0, heroi.ult_cooldown - 1)
            self.imprimir_status()
            round_num += 1

        vencedores = 'Heróis' if self.vivos(self.herois) else 'Vilões'
        print(f'Batalha encerrada. Vencedores: {vencedores}')
        return {
            'vencedores': vencedores,
            'log': list(self.log),
        }

    def resumo(self, n=20):
        print('\n--- Registro de Ações (últimas) ---')
        for linha in self.log[-n:]:
            print('-', linha)
        print('-----------------------------------')
