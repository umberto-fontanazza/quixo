from lib.game import Move
from src.position import Position, CORNERS, BORDERS
from typing import Literal, Annotated
from copy import deepcopy
from numpy.typing import NDArray
import numpy as np

Board = Annotated[NDArray[np.int8], Literal[5, 5]]
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

def get_possible_moves(board: Board, current_player: int) -> list[tuple[Position, Move]]:
    """returns all the possible moves given a Game object
        that is, a list of tuples (Position, Move)"""
    possible = []
    for position in BORDERS:
        if board[position] == -1 or board[position] == current_player:                                #if it is blank (-1) or mine (idx)
            if position[0] == 0:                                                    #in the top row
                if position[1] == 0:
                    possible += [(position, Move.BOTTOM), (position, Move.RIGHT)]
                elif position[1] == 4:
                    possible += [(position, Move.BOTTOM), (position, Move.LEFT)]
                else:
                    possible += [(position, Move.BOTTOM), (position, Move.LEFT), (position, Move.RIGHT)]
            elif position[0] == 4:
                if position[1] == 0:
                    possible += [(position, Move.TOP), (position, Move.RIGHT)]            #in the bottom row
                elif position[1] == 4:
                    possible += [(position, Move.TOP), (position, Move.LEFT)]
                else:
                    possible += [(position, Move.TOP), (position, Move.LEFT), (position, Move.RIGHT)]
            elif position[1] == 0:                                                 #other rows (1,2,3) on left side
                possible += [(position, Move.TOP), (position, Move.BOTTOM), (position, Move.RIGHT)]
            else:                                                           #other rows on right side
                possible += [(position, Move.TOP), (position, Move.LEFT), (position, Move.BOTTOM)]
    # i know, it is going to be evaluated again by game, but i think we could really save up some time
    np.random.shuffle(possible)
    return possible

def count_moves(board: Board) -> tuple[int, int]:
    """Returns the count of all available moves for O and for X as a tuple.
    A piece taken from the corner of the board accounts for 2 moves while a piece
    from the side accounts for 3 moves."""
    o_moves_count, x_moves_count = 0, 0
    for position in BORDERS:
        slide_count = 2 if position in CORNERS else 3
        if board[position] == -1:
            o_moves_count += slide_count
            x_moves_count += slide_count
        elif board[position] == 1:
            x_moves_count += slide_count
        else:
            o_moves_count += slide_count
    return (o_moves_count, x_moves_count)
