import random
import numpy as np
from consts import *
from player_types import PLAYER_TYPES, PLAYER_NAMES

AWARDS = {(COOPERATE, COOPERATE): (3, 3),
          (COOPERATE, DEFECT): (0, 5),
          (DEFECT, COOPERATE): (5, 0),
          (DEFECT, DEFECT): (1, 1)}

probabilities = [0.1, 0.2, 0.7]


def play_round(player1, player2):
    answer1 = player1.answer(player2)
    answer2 = player2.answer(player1)
    print(player1.state(), answer1, player2.state(), answer2)
    award1, award2 = AWARDS[(answer1, answer2)]
    player1.update(player2, answer2, award1)
    player2.update(player1, answer1, award2)


def create_random_player():
    return random.choice(PLAYER_TYPES)()


class Aquarium:
    def __init__(self, n, p=None):
        self.players = np.array([player() for player in np.random.choice(PLAYER_TYPES, size=n, p=p)])
        self.types_n = {player_name: sum([player.name() == player_name for player in self.players])
                        for player_name in PLAYER_NAMES}
        print(self.types_n)

    def show_state(self):
        for player in self.players:
            print(player.name(), player.score)

    def show_statistic(self):
        sums = {player_name: 0 for player_name in PLAYER_NAMES}
        for player in self.players:
            sums[player.name()] += player.score
        for player_name in PLAYER_NAMES:
            if self.types_n[player_name] != 0:
                print(f"{player_name}: SUM = {sums[player_name]}, AVG={sums[player_name] / self.types_n[player_name]}")

    def play_random_round(self, rounds=1):
        for _ in range(rounds):
            players = np.random.choice(self.players, size=2, replace=False)
            play_round(*players)


aquarium = Aquarium(10, p=probabilities)
aquarium.play_random_round(rounds=100)
aquarium.show_statistic()
