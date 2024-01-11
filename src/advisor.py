from typing import Callable, Literal
from src.board import Board, PlayerID, change_symbols
from numpy import array, trace, flip

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


def count_moves(board: Board) -> tuple[int, int]:
    """Returns the count of all available moves for O and for X as a tuple.
    A piece taken from the corner of the board accounts for 2 moves while a piece
    from the side accounts for 3 moves."""
    o_moves_count, x_moves_count = 0
    for p in [(x, y) for x in range(5) for y in [0, 4]] + [(x, y) for x in [0, 4] for y in range(1, 4)]:
        addend = 2 if p[0] in [0, 4] or p[1] in [0, 4] else 3
        if board[p] == -1:
            o_moves_count += addend
            x_moves_count += addend   
        elif board[p] == 1:
            x_moves_count += addend
        else:
            o_moves_count += addend
    return (o_moves_count, x_moves_count)
    

def available_moves_majority(board: Board, player: PlayerID) -> float:
    o_moves, x_moves = count_moves(board)
    if player == 'X' or player == 1:
        return x_moves * 100 / (x_moves + o_moves)
    elif player == 'O' or player == 0:
        return o_moves * 100 / (x_moves + o_moves)
    raise ValueError(f'{player =} is not valid')

def compact_board(board: Board, player: PlayerID) -> float:
    """counts the O close to others O and the X close to others X and returns a weighted difference"""
    count_x = 0
    count_o = 0
    for p in [(x, y) for x in range(5) for y in range(5)]:
        if board[p] == 1:
            for p1 in [(p[0]-1,p[1]-1),(p[0]-1,p[1]),(p[0]-1,p[1]+1),(p[0]+1,p[1]-1),(p[0]+1,p[1]),(p[0]+1,p[1]+1),(p[0],p[1]-1),(p[0],p[1]+1)]:
                if is_legal(p1):
                    if board[p1] == 1:
                        count_x = count_x + 1
        elif board[p] == 0:
            for p1 in [(p[0]-1,p[1]-1),(p[0]-1,p[1]),(p[0]-1,p[1]+1),(p[0]+1,p[1]-1),(p[0]+1,p[1]),(p[0]+1,p[1]+1),(p[0],p[1]-1),(p[0],p[1]+1)]:
                if is_legal(p1):
                    if board[p1] == 0:
                        count_o  = count_o + 1
    print(player)
    if player == 'X' or player == 1:
        return count_x * 100 / (count_x + count_o)
    elif player == 'O' or player == 0:
        return count_o * 100 / (count_x + count_o)

def is_legal(p: tuple) -> bool:
    """usefull func for compact_board"""
    return 0 <= p[0] and p[0] < 5 and 0 <= p[1] and p[1] < 5

Advisor = Callable[[Board, PlayerID], float]
ALL_ADVISORS: list[Advisor] = [
    line_majority,
    compact_board,
    # TODO: add available_moves_majority,
]
