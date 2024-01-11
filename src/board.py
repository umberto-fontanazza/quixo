from typing import Literal, Annotated
from numpy.typing import NDArray
from copy import deepcopy
from lib.game import Move
import numpy as np

Board = Annotated[NDArray[np.int8], Literal[5, 5]]
Position = tuple[int, int]
PlayerID = Literal['X', 'O', 1, 0]
Outcome = Literal['Win', 'Loss']

def random_board() -> Board:
    return np.random.choice([0, 1, -1], size=(5,5))

def change_symbols(board: Board) -> Board:
    '''Takes in a board where empty = -1, O = 0 and X = 1 and returns a board where empty = 0, O = -1 and X = 1'''
    b: NDArray = deepcopy(board)
    b = b * 2
    b = b -1
    b[b == -3] = 0
    return b

BORDER_POSITIONS = [(x, y) for x in range(5) for y in [0, 4]] + [(x, y) for x in [0, 4] for y in range(1, 4)]

def get_possible_moves(board: Board, current_player: int) -> list[tuple[Position, Move]]:
    """returns all the possible moves given a Game object
        that is, a list of tuples (Position, Move)"""
    possible = []
    for p in BORDER_POSITIONS:
        if board[p] == -1 or board[p] == current_player:                                #if it is blank (-1) or mine (idx)
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
    np.random.shuffle(possible)
    return possible