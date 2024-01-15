from cProfile import Profile
from pstats import Stats
from src.agent import DelphiPlayer
from lib.game import Game, Player
from lib.main import RandomPlayer
from src.simple_agents import CleverPlayer
from src.advisor import Advisor, ALL_ADVISORS
from test.example_boards import board_1, board_2, board_3, example_boards
from itertools import product
from tqdm import tqdm

def play_game():
    opponent = CleverPlayer()
    oracle_player = DelphiPlayer(tree_depth=2)
    N_GAMES = 100
    players = [oracle_player, opponent]
    starting = 0
    wins, losses = 0, 0
    for _ in tqdm(range(N_GAMES)):
        g = Game()
        winner_idx = g.play(players[starting], players[1-starting])
        agent_won = winner_idx == 0 and starting == 0
        if agent_won:
            wins += 1
        else:
            losses += 1
    print('depth', 2, ':', wins, losses)
    starting = 1 if starting == 0 else 0

def benchmark_advisors():
    for board, advisor in product([board_1, board_2, board_3, *example_boards], ALL_ADVISORS):
        score = advisor(board, 'X')


def main():
    with Profile() as profile:
        # play_game()
        for _ in range(100):
            benchmark_advisors()
    stats = Stats(profile)
    stats.sort_stats('cumulative')
    stats.print_stats()

if __name__ == '__main__':
    main()