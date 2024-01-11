from typing import Literal, Annotated
from numpy.typing import NDArray
from copy import deepcopy
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