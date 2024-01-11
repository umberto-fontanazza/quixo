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

BORDER_POSITIONS = [(x, y) for x in range(5) for y in (0, 4)] + [(x, y) for x in (0,4) for y in range(1, 4)]
CORNER_POSITIONS = [(x, y) for x in (0, 4) for y in (0, 4)]

def get_possible_moves(board: Board, current_player: int) -> list[tuple[Position, Move]]:
    """returns all the possible moves given a Game object
        that is, a list of tuples (Position, Move)"""
    possible = []
    for position in BORDER_POSITIONS:
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
    for position in BORDER_POSITIONS:
        slide_count = 2 if position in CORNER_POSITIONS else 3
        if board[position] == -1:
            o_moves_count += slide_count
            x_moves_count += slide_count
        elif board[position] == 1:
            x_moves_count += slide_count
        else:
            o_moves_count += slide_count
    return (o_moves_count, x_moves_count)

def check_winner(board: Board) -> set[PlayerID]:
        '''Check the winner.
        Returns the player IDs that have a winning row, column, or diagonal'''
        winners = []

        # for each row
        for x in range(board.shape[0]):
            # if a player has completed an entire row
            if board[x, 0] != -1 and all(board[x, :] == board[x, 0]):
                winners.append(board[x, 0])
        # for each column
        for y in range(board.shape[1]):
            # if a player has completed an entire column
            if board[0, y] != -1 and all(board[:, y] == board[0, y]):
                winners.append(board[0, y])
        # if a player has completed the principal diagonal
        if board[0, 0] != -1 and all(
            [board[x, x]
                for x in range(board.shape[0])] == board[0, 0]
        ):
            winners.append(board[0, 0])
        # if a player has completed the secondary diagonal
        if board[0, -1] != -1 and all(
            [board[x, -(x + 1)]
             for x in range(board.shape[0])] == board[0, -1]
        ):
            winners.append(board[0, -1])
        return set(winners)