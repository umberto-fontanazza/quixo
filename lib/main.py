import random
from lib.game import Game, Move, Player
from src.agent import Agent


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


if __name__ == '__main__':
    g = Game()
    g.print()
    player1 = MyPlayer()
    player2 = RandomPlayer()
    winner = g.play(player1, player2)
    g.print()
    print(f"Winner: Player {winner}")

    player = Agent()
    all_weights = []
    for _ in range(5):
        g.play(player, player1)
        won = g.check_winner() == 1
        player.train_oracle('Win' if won else 'Loss')
        all_weights.append(player.__oracle.__weights)
    for _ in range(5):
        g.play(player1, player)
        won = g.check_winner() == 0
        player.train_oracle('Win' if won else 'Loss')
        all_weights.append(player.__oracle.__weights)    