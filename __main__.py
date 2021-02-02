import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from settings import *
from tqdm import tqdm


def create_random_player():
    return random.choice(PLAYER_TYPES)()


class Aquarium:

    def __init__(self, n=10, randomised=False, quantities=None, p=None):

        if randomised:
            self.players = np.array([player() for player in np.random.choice(PLAYER_TYPES, size=n, p=p)])

        else:
            if not quantities:
                # Generate about-even quantities for each player.
                # Careful - the difference might turn out to be significant
                # if the total quantity is small.
                types_n = len(PLAYER_TYPES)
                quantities = [n//types_n] * types_n
                quantities[-1] = n - (n // types_n * types_n)

            self.players = np.concatenate([np.array([player() for _ in range(quantities[i])])
                                               for i, player in enumerate(PLAYER_TYPES)], axis=0)

        self.sums = {player_name: 0 for player_name in PLAYER_NAMES}
        self.types_n = {player_name: sum([player.name() == player_name for player in self.players])
                        for player_name in PLAYER_NAMES}
        self.rounds_played = 0

    def _play_round(self, player1, player2):
        answer1 = player1.answer(player2)
        answer2 = player2.answer(player1)

        award1, award2 = AWARDS[(answer1, answer2)]

        player1.update(player2, answer2, award1)
        player2.update(player1, answer1, award2)

        self.sums[player1.name()] += award1
        self.sums[player2.name()] += award2

        self.rounds_played += 1

    def _get_sums(self):
        return self.sums

    def play_random_rounds(self, rounds_to_play=1):
        for _ in range(rounds_to_play):
            players = np.random.choice(self.players, size=2, replace=False)
            self._play_round(*players)

    def get_averages(self):
        return {player_name: (self.sums[player_name] / self.types_n[player_name]
                              if self.types_n[player_name] != 0 else 0)
                for player_name in PLAYER_NAMES}

    def show_state(self):
        for player in self.players:
            print(player.name(), player.score)

    def show_statistic(self):
        sums = self._get_sums()
        for player_name in PLAYER_NAMES:
            if self.types_n[player_name] != 0:
                print(f"{player_name}: SUM = {sums[player_name]}, AVG={sums[player_name] / self.types_n[player_name]}")


def simulate(quantities=None, rounds_to_play=10):
    aquarium = Aquarium(quantities=quantities)
    aquarium.play_random_rounds(rounds_to_play=rounds_to_play)
    return aquarium.get_averages()


def average_logs(logs, window_size):
    game_logs_pd = pd.Series(logs[player_name])
    return game_logs_pd.rolling(window_size).mean()


WINDOW = int(MAX_ROUNDS / 15)
game_logs = {player_name: np.zeros((MAX_ROUNDS,)) for player_name in PLAYER_NAMES}

for rounds in tqdm(range(MAX_ROUNDS)):
    result = simulate(QUANTITIES, rounds)

    for player_name in PLAYER_NAMES:
        game_logs[player_name][rounds] = result.get(player_name, 0)

fig, (ax, ax2) = plt.subplots(1, 2, figsize=(15, 5))

for player_name in PLAYER_NAMES:
    ax.plot(range(MAX_ROUNDS), average_logs(game_logs, WINDOW), label=player_name + " averaged")
    ax.scatter(range(MAX_ROUNDS)[::WINDOW], game_logs[player_name][::WINDOW], label=player_name)

for player_name in PLAYER_NAMES:
    game_logs_normalised = {player_name: game_logs[player_name] / ([1] + list(range(1, MAX_ROUNDS)))
                            for player_name in game_logs.keys()}
    ax2.plot(range(MAX_ROUNDS), average_logs(game_logs_normalised, WINDOW),
             label=player_name + " averaged and normalised")

sup_title = f'Full results of aquarium simulation for {PLAYERS_N} players: {QUANTITIES} and {MAX_ROUNDS} max rounds'
fig.suptitle(sup_title)

ax.set_xlabel('Rounds played')
ax.set_ylabel('Average scores')
ax.legend()

ax2.set_xlabel('Rounds played')
ax2.set_ylabel('Average score per round')
ax2.legend()

plt.tight_layout()
plt.savefig(f'results/{sup_title}.png')
plt.show()
