from enum import Enum


class Memory(Enum):
    TRUSTWORTHY = 1
    UNTRUSTWORTHY = 0
    HALF_TRUSTWORTHY = 0.5
    NONE = -1


class Mode(Enum):
    PROBABILITY = 1
    QUANTITY = 2


class Answer(Enum):
    COOPERATE = True
    DEFECT = False
