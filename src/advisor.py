from typing import Callable
from src.board import Board, change_symbols
from numpy import array, trace, flip

""" b = array([ [-1, 1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, 0, 0, -1, -1]]) """

def line_majority(board: Board, player: int) -> float | int:
    b = change_symbols(board) # now empty = 0, and O = -1
    o_major_lines = 0
    x_major_lines = 0
    sum_by_cols = b.sum(axis = 0)
    sum_by_rows = b.sum(axis = 1)
    for col_sum in sum_by_cols:
        if col_sum < 0: o_major_lines += 1
        if col_sum > 0: x_major_lines += 1
    for row_sum in sum_by_rows:
        if row_sum < 0: o_major_lines += 1
        if row_sum > 0: x_major_lines += 1
    diagonal_sum = trace(b)
    antidiagonal_sum = trace(flip(b, axis=1))
    if diagonal_sum < 0: o_major_lines += 1
    if diagonal_sum > 0: x_major_lines += 1
    if antidiagonal_sum < 0: o_major_lines += 1
    if antidiagonal_sum > 0: x_major_lines += 1
    print(f'{o_major_lines =}, {x_major_lines =}')
    raise NotImplementedError()

Advisor = Callable[[Board, int], float]
ALL_ADVISORS: list[Advisor] = [
    line_majority
]