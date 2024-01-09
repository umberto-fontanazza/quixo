from typing import Literal
from numpy.typing import NDArray
import numpy as np

Board = NDArray
Position = tuple[int, int]
Outcome = Literal['Win', 'Loss']

def random_board() -> Board:
    return np.random.choice([0, 1, -1], size=(5,5))
