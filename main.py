from vilao import Vilao
from heroi import Heroi
from npc import NPC
from batalha import Batalha


def main():
    # Criando heróis e vilões (listas)
    herois = [
        Heroi('Link', 16, 100, ataque=14, defesa=6, poder='Ocarina do Tempo'),
        Heroi('Impa', 28, 90, ataque=12, defesa=8, poder='Espada Ancestral'),
    ]

    viloes = [
        Vilao('Ganon', 45, 120, maldade='Alta'),
        Vilao('Darknut', 30, 80, maldade='Média'),
    ]

    npc = NPC('Zelda', 16, 80, 'Princesa')

    # Apresentação inicial com diálogos
    print('\nPersonagens:')
    for heroi in herois:
        print('-', heroi)
    print('-', npc)
    for vilao in viloes:
        print('-', vilao)

    print('\nDiálogo:')
    print(viloes[0].dialogar(herois[0], 'Você não poderá salvar a todos dessa vez, garoto! Eu esperei por isso por anos... Estou mais forte do que nunca, a sua derrota é inevitável!'))
    input("Pressione Enter para continuar...")
    input(herois[0].dialogar(npc, f'Precisamos salvar o reino! {npc.nome}, você tem alguma pista de onde {viloes[0].nome} pode estar escondido?'))
    input(npc.dar_missao())
    input(npc.dialogar(herois[0], 'Link! Atrás de você!'))
    input(viloes[0].intimidar(herois[0]))
    input(viloes[0].dialogar(herois[0], 'Hahaha! Você é fraco, Link! Eu sou o poder supremo!'))
    input(herois[0].dialogar(viloes[0], f'Eu não vou desistir! Eu vou lutar até o fim para proteger este reino e as pessoas que amo! {herois[1].nome}, vamos acabar com ele!'))

    # Pergunta se jogador quer modo interativo
    batalha = Batalha(herois, viloes)
    while True:
        escolha = input('Executar batalha em modo interativo? (s/n) > ').strip().lower()
        if escolha.lower() == 's':
            batalha.interactive = True
            break

        elif escolha.lower() == 'n':
            batalha.interactive = False
            break
        
        else:
            print('Opção inválida. Digite "s" para sim ou "n" para não.')

    resultado = batalha.run()
    batalha.resumo()

    # Mostrar dicionários dos personagens (exemplo de uso de dicts)
    print('\nEstado final dos personagens:')
    for heroi in herois:
        print(heroi.to_dict())
    for vilao in viloes:
        print(vilao.to_dict())


if __name__ == "__main__":
    main()
