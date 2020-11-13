import random
import numpy as np
import matplotlib.pyplot as plt
from consts import *
from player_types import PLAYER_TYPES, PLAYER_NAMES

AWARDS = {(COOPERATE, COOPERATE): (3, 3),
          (COOPERATE, DEFECT): (0, 5),
          (DEFECT, COOPERATE): (5, 0),
          (DEFECT, DEFECT): (1, 1)}

PROBABILITIES = [0.1, 0.2, 0.7]
QUANTITIES = [1, 2, 7]


def play_round(player1, player2):
    answer1 = player1.answer(player2)
    answer2 = player2.answer(player1)
    # print(player1.state(), answer1, player2.state(), answer2)
    award1, award2 = AWARDS[(answer1, answer2)]
    player1.update(player2, answer2, award1)
    player2.update(player1, answer1, award2)


def create_random_player():
    return random.choice(PLAYER_TYPES)()


class Aquarium:
    def __init__(self, n = 10, random = False, quantities=None, p=None):

        if random:
            self.players = np.array([player() for player in np.random.choice(PLAYER_TYPES, size=n, p=p)])

        else:
            if not quantities:
                raise NotImplementedError("Need to use about-even quantities of players")
            else:
                self.players = np.concatenate([np.array([player() for _ in range(quantities[i])])
                                                        for i, player in enumerate(PLAYER_TYPES)], axis=0)

        # print(self.players)
        self.types_n = {player_name: sum([player.name() == player_name for player in self.players])
                        for player_name in PLAYER_NAMES}
        # print(self.types_n)

    def play_random_round(self, rounds=1):
        for _ in range(rounds):
            players = np.random.choice(self.players, size=2, replace=False)
            play_round(*players)

    def get_sums(self):
        sums = {player_name: 0 for player_name in PLAYER_NAMES}
        for player in self.players:
            sums[player.name()] += player.score
        return sums

    def get_averages(self):
        sums = self.get_sums()
        return {player_name: (sums[player_name] / self.types_n[player_name] if self.types_n[player_name] != 0 else 0)
                for player_name in PLAYER_NAMES}

    def show_state(self):
        for player in self.players:
            print(player.name(), player.score)

    def show_statistic(self):
        sums = self.get_sums()
        for player_name in PLAYER_NAMES:
            if self.types_n[player_name] != 0:
                print(f"{player_name}: SUM = {sums[player_name]}, AVG={sums[player_name] / self.types_n[player_name]}")


def simulate(quantities=None, rounds=10):
    aquarium = Aquarium(quantities=quantities)
    aquarium.play_random_round(rounds=rounds)
    # aquarium.show_statistic()
    return aquarium.get_averages()


# aquarium = Aquarium(quantities=QUANTITIES)

PLAYERS_N = sum(QUANTITIES)
MAX_ROUNDS = int(1e2)
game_logs = {player_name: np.zeros((MAX_ROUNDS,)) for player_name in PLAYER_NAMES}

for rounds in range(MAX_ROUNDS):
    result = simulate(QUANTITIES, rounds)

    for player_name in PLAYER_NAMES:
        game_logs[player_name][rounds] = result.get(player_name, 0)

print(game_logs)

fig, ax = plt.subplots()
fig.suptitle(f'Results of aquarium simulations for {PLAYERS_N} players: {QUANTITIES}')
ax.set_xlabel('Rounds played')
ax.set_ylabel('Average scores')

for player_name in PLAYER_NAMES:
    # averaged_logs =
    ax.scatter(range(MAX_ROUNDS), game_logs[player_name], label=player_name)

ax.legend()
plt.show()
