from typing import Callable
from src.board import Board, PlayerID
from numpy import trace, flip

Advisor = Callable[[Board, PlayerID], float]

# TODO: this should be a private method but it needs to be imported for testing in test_advisor
def line_majority_count(board: Board) -> tuple[int, int]:
    """Computes for each player the number of lines (among the 5 rows, 5 cols and 2 diagonals)
    where they have more symbols compared to the opponent"""
    b = Board.change_symbols(board.ndarray) # now empty = 0, and O = -1
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
    o_moves, x_moves = board.count_moves()
    if player == 'X' or player == 1:
        return x_moves * 100 / (x_moves + o_moves)
    elif player == 'O' or player == 0:
        return o_moves * 100 / (x_moves + o_moves)
    raise ValueError(f'{player =} is not valid')

def compact_board(board: Board, player: PlayerID) -> float:
    """counts the O close to others O and the X close to others X and returns a weighted difference"""
    count_x = 0
    count_o = 0
    arr = board.ndarray
    for p in [(x, y) for x in range(5) for y in range(5)]:
        if arr[p] == 1:
            for p1 in [(p[0]-1,p[1]-1),(p[0]-1,p[1]),(p[0]-1,p[1]+1),(p[0]+1,p[1]-1),(p[0]+1,p[1]),(p[0]+1,p[1]+1),(p[0],p[1]-1),(p[0],p[1]+1)]:
                if is_legal(p1):
                    if arr[p1] == 1:
                        count_x = count_x + 1
        elif arr[p] == 0:
            for p1 in [(p[0]-1,p[1]-1),(p[0]-1,p[1]),(p[0]-1,p[1]+1),(p[0]+1,p[1]-1),(p[0]+1,p[1]),(p[0]+1,p[1]+1),(p[0],p[1]-1),(p[0],p[1]+1)]:
                if is_legal(p1):
                    if arr[p1] == 0:
                        count_o  = count_o + 1
    if player == 'X' or player == 1:
        return count_x * 100 / (count_x + count_o)
    elif player == 'O' or player == 0:
        return count_o * 100 / (count_x + count_o)

def is_legal(p: tuple) -> bool:
    """utility func for compact_board"""
    return 0 <= p[0] and p[0] < 5 and 0 <= p[1] and p[1] < 5

def board_majority(board: Board, player: PlayerID) -> int:
    """advisor based on the difference of placed tiles between the players"""
    arr = Board.change_symbols(board.ndarray)
    total_count: int = int(arr.sum())
    return total_count if player == 1 else -total_count


ALL_ADVISORS: list[Advisor] = [
    line_majority,
    compact_board,
    available_moves_majority,
    board_majority
]
