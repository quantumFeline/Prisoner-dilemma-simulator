from consts import *


class Player:
    id = 0

    def __init__(self):
        self.memory_used = False

        self.rounds_played = 0
        self.id = Player.id
        self.score = 0
        Player.id += 1

    def update(self, opponent: 'Player', opponent_answer: Answer, award, aquarium=None):
        self.score += award
        self.rounds_played += 1
        if aquarium:
            aquarium.sum_per_team[self.name()] += award

    def answer(self, player: 'Player'):
        return Answer.COOPERATE

    def name(self):
        return type(self).__name__

    def state(self):
        return f"I'm {self.name()} {self.id}, score={self.score}"


class PlayerWithMemory(Player):
    def __init__(self):
        super().__init__()
        self.memory_used = True
        self.memory = {}

    def update(self, opponent, opponent_answer, award, aquarium=None):
        super().update(opponent, opponent_answer, award, aquarium)
        self.update_memory(opponent, opponent_answer)

    def update_memory(self, opponent, opponent_answer):
        # Default describes Tit-for-Tat behaviour.
        if opponent_answer == Answer.COOPERATE:
            self.memory[opponent.id] = Memory.TRUSTWORTHY
        else:
            self.memory[opponent.id] = Memory.UNTRUSTWORTHY
