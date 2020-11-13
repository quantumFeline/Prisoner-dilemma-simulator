from consts import *
from Player import Player


class Cooperator(Player):
    def __init__(self):
        super().__init__()
        self.memory_used = False

    def answer(self, opponent):
        return COOPERATE


class Defector(Player):
    def __init__(self):
        super().__init__()
        self.memory_used = False

    def answer(self, opponent):
        return DEFECT


class TitForTat(Player):
    def answer(self, opponent):
        trust = self.memory.get(opponent.id, Memory.TRUSTWORTHY)
        if trust == Memory.TRUSTWORTHY:
            return COOPERATE
        else:
            return DEFECT


PLAYER_TYPES = [Cooperator, Defector, TitForTat]
PLAYER_NAMES = [player().name() for player in PLAYER_TYPES]