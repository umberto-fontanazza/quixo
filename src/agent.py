import random
from lib import game
from oracle import Oracle
Game, Move, Player = game.Game, game.Move, game.Player

class DelphiPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move
    

if __name__ == '__main__':
    print('helo uze theez 2 test')    