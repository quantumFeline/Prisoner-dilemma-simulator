from settings import *
import numpy as np


class Automaton:
    """A class that organizes matches between players
    and updates their scores.
    """
    DEFAULT_AWARDS = [0, 1, 3, 5]

    @staticmethod
    def set_awards(cd, dd, cc, dc):
        return {(Answer.COOPERATE, Answer.COOPERATE): (cc, cc),
                      (Answer.COOPERATE, Answer.DEFECT): (cd, dc),
                      (Answer.DEFECT, Answer.COOPERATE): (dc, cd),
                      (Answer.DEFECT, Answer.DEFECT): (dd, dd)}

    def __init__(self, aquarium: 'Aquarium' = None, awards: list = None) -> None:

        if awards:
            awards_list = awards
        else:
            awards_list = Automaton.DEFAULT_AWARDS

        self.AWARDS = Automaton.set_awards(*awards_list)
        self.aquarium = aquarium

    def play_round(self, player1: Player, player2: Player):
        answer1 = player1.answer(player2)
        answer2 = player2.answer(player1)

        award1, award2 = self.AWARDS[(answer1, answer2)]

        player1.update(player2, answer2, award1, self.aquarium)
        player2.update(player1, answer1, award2, self.aquarium)


class Aquarium:

    def __init__(self, n=10, randomised=False, quantities=None, p=None, awards=None):

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
        self.automaton = Automaton(aquarium=self, awards=awards)

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
