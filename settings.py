from player_types import *

# Main parameters.

PLAYER_TYPES = [Cooperator, Defector, TitForTat]
MODE = Modes.QUANTITY
MAX_ROUNDS = int(5e2)

# Set up one, depending on mode. This determines the number of players in the game.
# TODO: probability mode
PROBABILITIES = [0.1, 0.2, 0.7]
QUANTITIES = [1, 2, 7]

# Technical. Generally speaking, is not to be changed.
PLAYER_TYPE_NAMES = [player().name() for player in PLAYER_TYPES]
PLAYERS_N = sum(QUANTITIES)
assert len(PROBABILITIES) == len(PLAYER_TYPES) == len(QUANTITIES)
