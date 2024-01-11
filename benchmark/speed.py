from cProfile import Profile
from pstats import Stats
from src.agent import DelphiPlayer
from lib.game import Game, Player
from lib.main import RandomPlayer

def main():
    with Profile() as profile:
        game = Game()
        player_1 = DelphiPlayer()
        player_2 = RandomPlayer()
        winner = game.play(player_1, player_2)
        print(f'{winner =}')
    stats = Stats(profile)
    stats.sort_stats('cumulative')
    stats.print_stats()

if __name__ == '__main__':
    main()