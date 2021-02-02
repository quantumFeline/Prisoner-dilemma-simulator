from consts import *


class Player:
    id = 0

    def __init__(self):
        self.memory_used = False

        self.rounds_played = 0
        self.id = Player.id
        self.score = 0
        Player.id += 1

    def update(self, opponent, opponent_answer, award):
        self.score += award
        self.rounds_played += 1

    def name(self):
        return type(self).__name__

    def state(self):
        return f"I'm {self.name()} {self.id}, score={self.score}"


class PlayerWithMemory(Player):
    def __init__(self):
        super().__init__()
        self.memory_used = True
        self.memory = {}

    def update(self, opponent, opponent_answer, award):
        super().update(opponent, opponent_answer, award)
        if opponent_answer == COOPERATE:
            self.memory[opponent.id] = Memory.TRUSTWORTHY
        else:
            self.memory[opponent.id] = Memory.UNTRUSTWORTHY
