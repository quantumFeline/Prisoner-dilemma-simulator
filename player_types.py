from consts import *
from Player import Player, PlayerWithMemory
from numpy.random import randint


class Cooperator(Player):
    def answer(self, opponent):
        return Answer.COOPERATE


class Defector(Player):
    def answer(self, opponent):
        return Answer.DEFECT


class TitForTat(PlayerWithMemory):

    def answer(self, opponent):
        trust = self.memory.get(opponent.id, Memory.TRUSTWORTHY)
        if trust == Memory.TRUSTWORTHY:
            return Answer.COOPERATE
        else:
            return Answer.DEFECT


class ForgivingTitForTat(PlayerWithMemory):

    def answer(self, opponent):
        trust = self.memory.get(opponent.id, Memory.TRUSTWORTHY)
        if trust == Memory.TRUSTWORTHY or trust == Memory.HALF_TRUSTWORTHY:
            return Answer.COOPERATE
        else:
            return Answer.DEFECT

    def update_memory(self, opponent, opponent_answer):

        prev_memory = self.memory.get(opponent.id, Memory.TRUSTWORTHY)

        if opponent_answer == Answer.COOPERATE:
            self.memory[opponent.id] = Memory.TRUSTWORTHY

        elif prev_memory == Memory.TRUSTWORTHY and opponent_answer == Answer.DEFECT:
            self.memory[opponent.id] = Memory.HALF_TRUSTWORTHY

        else:
            self.memory[opponent.id] = Memory.UNTRUSTWORTHY


class SoRandom(Player):
    def answer(self, opponent):
        return Answer.COOPERATE if randint(2) == 1 else Answer.DEFECT
