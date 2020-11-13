from consts import *


class Player:
    id = 0

    def __init__(self):
        self.memory = {}
        self.memory_used = True
        self.id = Player.id
        self.score = 0
        Player.id += 1

    def update(self, opponent, opponent_answer, award):
        self.score += award
        if self.memory_used:
            if opponent_answer == COOPERATE:
                self.memory[opponent.id] = Memory.TRUSTWORTHY
            else:
                self.memory[opponent.id] = Memory.UNTRUSTWORTHY

    def name(self):
        return type(self).__name__

    def state(self):
        return f"I'm {self.name()} {self.id}, score={self.score}"
