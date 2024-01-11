from typing import Callable
from src.board import Board, PlayerID, change_symbols, count_moves
from numpy import trace, flip

# TODO: this should be a private method but it needs to be imported for testing in test_advisor
def line_majority_count(board: Board) -> tuple[int, int]:
    """Computes for each player the number of lines (among the 5 rows, 5 cols and 2 diagonals)
    where they have more symbols compared to the opponent"""
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
    return (o_major_lines, x_major_lines)

def line_majority(board: Board, player: PlayerID) -> float:
    o_major, x_major = line_majority_count(board)
    if player == 'X' or player == 1:
        return x_major * 100 / (o_major + x_major)
    elif player == 'O' or player == 0:
        return o_major * 100 / (o_major + x_major)


def available_moves_majority(board: Board, player: PlayerID) -> float:
    o_moves, x_moves = count_moves(board)
    if player == 'X' or player == 1:
        return x_moves * 100 / (x_moves + o_moves)
    elif player == 'O' or player == 0:
        return o_moves * 100 / (x_moves + o_moves)
    raise ValueError(f'{player =} is not valid')

Advisor = Callable[[Board, PlayerID], float]
ALL_ADVISORS: list[Advisor] = [
    line_majority,
    # TODO: add available_moves_majority,
]