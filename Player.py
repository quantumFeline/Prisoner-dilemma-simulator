from consts import *


class Player:
    id = 0

    def __init__(self):
        self.memory = {}
        self.id = Player.id
        self.score = 0
        Player.id += 1

    # def answer(self, opponent)

    def update(self, opponent, opponent_answer, award):
        print(self.name(), "me:", self.id, "opponent:", opponent.id, opponent_answer)
        if opponent_answer == COOPERATE:
            self.memory[opponent.id] = Memory.TRUSTWORTHY
            # print("trusting")
        else:
            self.memory[opponent.id] = Memory.UNTRUSTWORTHY
            # print("memory:", self.memory)
            # print("distrusting")
        self.score += award

    def name(self):
        return type(self).__name__

    def state(self):
        return f"I'm {self.name()} {self.id}, score={self.score}"
