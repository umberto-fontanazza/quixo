import numpy as np                                      # Umbi so che non ti piace ma 
from random import choice
from oracle import Oracle as ocl

import sys                                              # Umbi probabilmente neanche questo ti piace ma
sys.path.append('../')
from quixo.lib.game import Game, Move, Player

Position = tuple[int, int]

# TODO: really implement
def getPossibleMoves(board: np.ndarray) -> list[tuple[Position, Move]]:
    """returns all the possible moves given a board
        that is, a list of tuples (Position, Move)"""
    slides = [Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT]
    positions = [(x, y) for x in range(5) for y in [0, 4]] + [(x, y) for x in [0, 4] for y in range(5)]
    return [(p, s) for p in positions for s in slides]


class DelphiPlayer(Player):
    def __init__(self) -> None:
        super().__init__()
        self.delphi: ocl = ocl() 
        self.episode: list[np.ndarray] = [np.ndarray]   

    # TODO: implement minmax
    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        chosen: tuple[Position, Move] = choice(getPossibleMoves(game.get_board()))
        #implement minmax
        self.episode.append(chosen[0])
        return chosen
    
    def feedback(self, won: bool) -> None:
        """at the end of a game, gives feedback to the oracle"""
        for s in self.episode:
            self.delphi.train(s, won)
        self.episode = []    

    

if __name__ == '__main__':
    print('helo uze theez 2 test')    
    dp = DelphiPlayer()
    g = Game()
    g.play(dp, dp)
    g.print()