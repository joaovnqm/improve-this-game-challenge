from personagem import Personagem


class NPC(Personagem):
    """Personagem não jogável com papel social (que pode dar quests ou diálogos)."""

    def __init__(self, nome, idade, vida, papel):
        super().__init__(nome, idade, vida)
        self.papel = papel

    def dar_missao(self):
        return f'{self.nome} oferece uma missão: "Ajude-me a vencer Ganon e salvar não só o reino, mas o mundo."'

    def __str__(self):
        return f'NPC: {self.nome}, Papel: {self.papel}, Vida: {self.vida}'