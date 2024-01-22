import random
from lib.game import Game, Move, Player


class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move


class MyPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move


from src.agent import Agent, GOOD_WEIGHTS
from src.simple_agents import BetterRandomPlayer, ManualPlayer


if __name__ == '__main__':
    player1 = Agent(oracle_weights = GOOD_WEIGHTS, depth_limit = 3)                 # precomputed weights
    player1.training = False
    player2 = BetterRandomPlayer()
    winner = Game().play(player1, player2)
    print(f"\nWinner: {'Agent' if winner == 0 else 'Random'} \n")
    winner = Game().play(player2, player1)                                               # swapped players
    print(f"\nWinner: {'Agent' if winner == 1 else 'Random'} \n")

    print('\n\nNow it is your turn!\n')
    player1.depth_limit = 4
    player2 = ManualPlayer()
    g = Game()
    winner = g.play(player2, player1)
    print(f"\nWinner: {'Agent' if winner == 1 else 'Human'} \n")
    g.print()
