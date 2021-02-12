from simulators import Automaton
from tqdm import tqdm
from player_types import SoRandom, TitForTat


automaton = Automaton()
opponent = SoRandom()
tit_for_tat = TitForTat()
so_random = SoRandom()

for rounds in tqdm(range(100)):
    automaton.play_round(opponent, tit_for_tat)
    automaton.play_round(opponent, so_random)

print(tit_for_tat.score, so_random.score)
