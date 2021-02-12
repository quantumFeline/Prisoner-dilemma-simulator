import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from settings import *
from tqdm import tqdm
from datetime import datetime


class Automaton:
    """A class that organizes matches between players
    and updates their scores.
    """
    DEFAULT_AWARDS = {(Answer.COOPERATE, Answer.COOPERATE): (3, 3),
                      (Answer.COOPERATE, Answer.DEFECT): (0, 5),
                      (Answer.DEFECT, Answer.COOPERATE): (5, 0),
                      (Answer.DEFECT, Answer.DEFECT): (1, 1)}

    def __init__(self, aquarium: 'Aquarium' = None, awards: dict = None) -> None:
        if awards:
            self.AWARDS = awards
        else:
            self.AWARDS = Automaton.DEFAULT_AWARDS

        self.aquarium = aquarium

    def play_round(self, player1: Player, player2: Player):
        answer1 = player1.answer(player2)
        answer2 = player2.answer(player1)

        award1, award2 = self.AWARDS[(answer1, answer2)]

        player1.update(player2, answer2, award1, self.aquarium)
        player2.update(player1, answer1, award2, self.aquarium)


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
                quantities = [n // types_n] * types_n
                quantities[-1] = n - (n // types_n * types_n)

            self.players = np.concatenate([np.array([player() for _ in range(quantities[i])])
                                           for i, player in enumerate(PLAYER_TYPES)], axis=0)

        self.sum_per_team = {player_name: 0 for player_name in PLAYER_TYPE_NAMES}
        self.types_n = {player_name: sum([player.name() == player_name for player in self.players])
                        for player_name in PLAYER_TYPE_NAMES}
        self.rounds_played = 0
        self.automaton = Automaton(aquarium=self)

    def _get_sums(self):
        return self.sum_per_team

    def play_random_rounds(self, rounds_to_play: int=1):

        for _ in range(rounds_to_play):
            players = np.random.choice(self.players, size=2, replace=False)
            self.automaton.play_round(*players)

        self.rounds_played += rounds_to_play

    def get_averages(self):
        return {player_name: (self.sum_per_team[player_name] / self.types_n[player_name]
                              if self.types_n[player_name] != 0 else 0)
                for player_name in PLAYER_TYPE_NAMES}

    def show_state(self):
        for player in self.players:
            print(player.name(), player.score)

    def show_statistic(self):
        sums = self._get_sums()
        for player_name in PLAYER_TYPE_NAMES:
            if self.types_n[player_name] != 0:
                print(f"{player_name}: SUM = {sums[player_name]}, "
                      f"AVG={sums[player_name] / self.types_n[player_name]}")


def simulate(quantities: list = None, rounds_to_play: int = 10):
    aquarium = Aquarium(quantities=quantities)
    aquarium.play_random_rounds(rounds_to_play=rounds_to_play)
    return aquarium.get_averages()


def average_logs(player_name, logs, window_size):
    game_logs_pd = pd.Series(logs[player_name])
    return game_logs_pd.rolling(window_size).mean()


WINDOW = int(MAX_ROUNDS / 15)
game_logs = {player_name: np.zeros((MAX_ROUNDS,)) for player_name in PLAYER_TYPE_NAMES}

for rounds in tqdm(range(MAX_ROUNDS)):
    result = simulate(QUANTITIES, rounds)

    for player_name in PLAYER_TYPE_NAMES:
        game_logs[player_name][rounds] = result.get(player_name, 0)


def generate_titles(players_n: list, quantities: list, max_rounds: list):
    player_str_list = "; ".join([f"{PLAYER_TYPE_NAMES[i]} - {quantities[i]}" for i in range(len(PLAYER_TYPE_NAMES))])
    full_title = f"Results of aquarium simulation for {players_n} players and {max_rounds} max rounds\n" \
                 f"Players list: {player_str_list}"
    short_title = f"Results for {players_n} players and {max_rounds} rounds {datetime.now()}"
    return {"short": short_title, "full": full_title}


def draw_graphs():
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(15, 5))

    for player_name in PLAYER_TYPE_NAMES:
        ax.plot(range(MAX_ROUNDS), average_logs(player_name, game_logs, WINDOW), label=player_name + " averaged")
        ax.scatter(range(MAX_ROUNDS)[::WINDOW], game_logs[player_name][::WINDOW], label=player_name)

    for player_name in PLAYER_TYPE_NAMES:
        game_logs_normalised = {player_name: game_logs[player_name] / ([1] + list(range(1, MAX_ROUNDS)))
                                for player_name in game_logs.keys()}
        ax2.plot(range(MAX_ROUNDS), average_logs(player_name, game_logs_normalised, WINDOW),
                 label=player_name + " averaged and normalised")

    titles = generate_titles(PLAYERS_N, QUANTITIES, MAX_ROUNDS)
    sup_title = titles['full']
    filename = titles['short']
    fig.suptitle(sup_title)

    ax.set_xlabel('Rounds played')
    ax.set_ylabel('Average scores')
    ax.legend()

    ax2.set_xlabel('Rounds played')
    ax2.set_ylabel('Average score per round')
    ax2.legend()

    plt.tight_layout()
    return filename, plt


name, plt = draw_graphs()
plt.savefig(f'results/{name}.png')
plt.show()
