import numpy as np                                      # Umbi so che non ti piace ma 
from random import choice
from oracle import Oracle as Ocl

import sys                                              # Umbi probabilmente neanche questo ti piace ma
sys.path.append('../')
from quixo.lib.game import Game, Move, Player

Position = tuple[int, int]
SLIDES = [Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT]
BORDER_POSITIONS = [(x, y) for x in range(5) for y in [0, 4]] + [(x, y) for x in [0, 4] for y in range(1, 4)]

def getPossibleMoves(board: np.ndarray, idx: int) -> list[tuple[Position, Move]]:
    """returns all the possible moves given a Game object
        that is, a list of tuples (Position, Move)"""
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
    # i know, it is going to be evaluated again by game, but i think we could really save up some time
    assert len(possible) > 0
    return possible


class DelphiPlayer(Player):
    def __init__(self, tree_depth: int = 4) -> None:
        super().__init__()
        self.delphi: Ocl = Ocl() 
        self.episode: list[np.ndarray] = [np.ndarray]   
        self.depth = tree_depth if tree_depth % 2 == 0 else tree_depth + 1                  # should it be an even number ? 

    # TODO: implement these
    def __max(self, board: np.ndarray, idx: int, curr_depth: int = 0) -> float:
        if curr_depth >= self.depth:
            return self.delphi(board)

        max = self.__min(board, (idx + 1) % 1, curr_depth + 1)
        return max

    def __min(self, board: np.ndarray, idx: int, curr_depth: int = 1) -> float:
        min = self.__max(board, (idx + 1) % 1, curr_depth + 1)
        return min
    
    # TODO: implement
    def __apply_move(self, board: np.ndarray, move: tuple[Position, Move], idx: int) -> np.ndarray:
        """given a board, a move and an index gives out a copy of the board after the move is applied"""
        pass

    # TODO: implement minmax
    # TODO: is the position to be given to Oracle the current one or the future one (after the move), or the one where i get after minmax? 
    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        idx: int = game.get_current_player()
        # chosen: tuple[Position, Move] = choice(getPossibleMoves(game.get_board(), idx))
        # minmax
        future_boards = [self.apply_move(p) for p in getPossibleMoves(game.get_board(), idx)]
        evaluated = [(b, self.__min(b)) for b in future_boards]
        chosen = max(evaluated, key = lambda move_qual: move_qual[1])
        self.episode.append(chosen[0])                                                                  #episode is used in feedback
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

    # informal test getPossibleMoves
    if False:
        b = g.get_board()
        for s in BORDER_POSITIONS:
            b[s] = 0
        b[0,0] = 1    
        print(b)
        print(len(getPossibleMoves(b, 1)))

    if True:
        g.play(dp, dp)
        g.print()
        print(g.check_winner())