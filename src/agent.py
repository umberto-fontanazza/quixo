import numpy as np                                      # Umbi so che non ti piace ma 
from random import choice
from oracle import Oracle as ocl

import sys                                              # Umbi probabilmente neanche questo ti piace ma
sys.path.append('../')
from quixo.lib.game import Game, Move, Player

Position = tuple[int, int]
SLIDES = [Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT]
BORDER_POSITIONS = [(x, y) for x in range(5) for y in [0, 4]] + [(x, y) for x in [0, 4] for y in range(1, 4)]

def getPossibleMoves(game: Game) -> list[tuple[Position, Move]]:
    """returns all the possible moves given a Game object
        that is, a list of tuples (Position, Move)"""
    board: np.ndarray = game.get_board()
    idx: int = game.get_current_player()

    possible = []
    for p in BORDER_POSITIONS:
        if board[p] == -1 or board[p] == idx:                                #if it is blank (-1) or mine (idx)
            if p[0] == 0:                                                    #in the top row
                if p[1] == 0:
                    possible += [(p, Move.BOTTOM), (p, Move.RIGHT)]
                elif p[1] == 4:
                    possible += [(p, Move.BOTTOM), (p, Move.LEFT)]    
                else:
                    possible += [(p, Move.BOTTOM), (p, Move.LEFT), (p, Move.RIGHT)]    
            elif p[0] == 4:
                if p[1] == 0:
                    possible += [(p, Move.TOP), (p, Move.RIGHT)]            #in the bottom row
                elif p[1] == 4:
                    possible += [(p, Move.TOP), (p, Move.LEFT)]    
                else:
                    possible += [(p, Move.TOP), (p, Move.LEFT), (p, Move.RIGHT)]
            elif p[1] == 0:                                                 #other rows (1,2,3) on left side
                possible += [(p, Move.TOP), (p, Move.BOTTOM), (p, Move.RIGHT)]
            else:                                                           #other rows on right side
                possible += [(p, Move.TOP), (p, Move.LEFT), (p, Move.BOTTOM)]     
    # i know, it is going to be evaluated again, but i think we could really save up some time
    return possible


class DelphiPlayer(Player):
    def __init__(self) -> None:
        super().__init__()
        self.delphi: ocl = ocl() 
        self.episode: list[np.ndarray] = [np.ndarray]   

    # TODO: implement minmax
    # TODO: is the position to be given to Oracle the current one or the future one (after the move)? 
    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        chosen: tuple[Position, Move] = choice(getPossibleMoves(game))
        #implement minmax
        self.episode.append(chosen[0])
        return chosen
    
    def feedback(self, won: bool) -> None:
        """at the end of a game, gives feedback to the oracle"""
        for s in self.episode:
            self.delphi.train(s, won)
        self.episode = []    

    

# TODO: remove this
if __name__ == '__main__':
    # used for testing  

    dp = DelphiPlayer()
    g = Game()

    g.play(dp, dp)
    g.print()
    print(g.check_winner())