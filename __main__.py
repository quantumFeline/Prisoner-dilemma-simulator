import sys
from settings import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
from datetime import datetime
from simulators import Aquarium


def simulate(quantities: list = None, rounds_to_play: int = 10):
    aquarium = Aquarium(quantities=quantities, awards=AWARDS)
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
                 f"Players list: {player_str_list};     Awards: {AWARDS}"
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
