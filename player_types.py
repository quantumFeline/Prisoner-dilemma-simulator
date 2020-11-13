from consts import *
from Player import Player


class Cooperator(Player):
    def answer(self, opponent):
        return COOPERATE


class Defector(Player):
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
PLAYER_NAMES = [p_type.__name__ for p_type in PLAYER_TYPES]
