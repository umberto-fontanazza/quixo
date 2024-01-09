from typing import Literal
from numpy.typing import NDArray

Board = NDArray
Position = tuple[int, int]
Outcome = Literal['Win', 'Loss']
