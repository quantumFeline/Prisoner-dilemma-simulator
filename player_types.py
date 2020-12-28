from consts import *
from Player import Player
from numpy.random import randint


class Cooperator(Player):
    def __init__(self):
        super().__init__(False)

    def answer(self, opponent):
        return COOPERATE


class Defector(Player):
    def __init__(self):
        super().__init__(False)

    def answer(self, opponent):
        return DEFECT


class TitForTat(Player):
    def answer(self, opponent):
        trust = self.memory.get(opponent.id, Memory.TRUSTWORTHY)
        if trust == Memory.TRUSTWORTHY:
            return COOPERATE
        else:
            return DEFECT


class ForgivingTitForTat(Player):
    def answer(self, opponent):
        trust = self.memory.get(opponent.id, Memory.TRUSTWORTHY)
        if trust == Memory.TRUSTWORTHY or trust == Memory.HALF_TRUSTWORTHY:
            return COOPERATE
        else:
            return DEFECT

    def update(self, opponent, opponent_answer, award):
        old_memory =  self.memory.get(opponent.id, Memory.TRUSTWORTHY)
        super().update(opponent, opponent_answer, award)
        new_memory = self.memory.get(opponent.id, Memory.TRUSTWORTHY)

        if old_memory == Memory.TRUSTWORTHY and new_memory == Memory.UNTRUSTWORTHY:
            self.memory[opponent.id] = Memory.HALF_TRUSTWORTHY

class SoRandom(Player):
    def __init__(self):
        super().__init__(False)

    def answer(self, opponent):
        return COOPERATE if randint(2) == 1 else DEFECT
