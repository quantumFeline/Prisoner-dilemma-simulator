from player_types import *

# Main parameters.

PLAYER_TYPES = [Cooperator, Defector, TitForTat]
MODE = Mode.QUANTITY
MAX_ROUNDS = int(2e3)

# Set up one, depending on mode. This determines the number of players in the game.
# TODO: probability mode
PROBABILITIES = [0.1, 0.2, 0.6, 0.1]
QUANTITIES = [5, 5, 5]

# Technical. Generally speaking, is not to be changed.
PLAYER_TYPE_NAMES = [player().name() for player in PLAYER_TYPES]
PLAYERS_N = sum(QUANTITIES)

if MODE == Mode.QUANTITY:
    assert len(PLAYER_TYPES) == len(QUANTITIES)
elif MODE == Mode.PROBABILITY:
    assert len(PLAYER_TYPES) == len(PROBABILITIES)
else:
    raise ValueError("MODE not set")
