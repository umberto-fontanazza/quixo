from typing import Callable
from src.board import Board
from src.player import PlayerID
from numpy import trace, flip
from functools import cache

Advisor = Callable[[Board, PlayerID], float]

@cache
def __rule_advantage(o_major: int, x_major: int, player: PlayerID) -> float:
    if o_major == x_major == 0:
        return 50
    elif player == 'X' or player == 1:
        return x_major * 100 / (o_major + x_major)
    elif player == 'O' or player == 0:
        return o_major * 100 / (o_major + x_major)
    else:
        return 50

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
    return __rule_advantage(*line_majority_count(board), player)

def available_moves_majority(board: Board, player: PlayerID) -> float:
    return __rule_advantage(*board.count_moves(), player)

# TODO: somehow makes the agent slow down a loooot
def compact_board(board: Board, player: PlayerID) -> float:
    """counts the O close to others O and the X close to others X and returns a score"""
    count_x, count_o = 0, 0
    arr = board.ndarray
    for pos in [(x, y) for x in range(5) for y in range(5)]:
        player = arr[pos]
        if player not in (0, 1):
            continue
        adjacents = [(pos[0]-1,pos[1]-1),(pos[0]-1,pos[1]),(pos[0]-1,pos[1]+1),(pos[0]+1,pos[1]-1),(pos[0]+1,pos[1]),(pos[0]+1,pos[1]+1),(pos[0],pos[1]-1),(pos[0],pos[1]+1)]
        for adjacent in adjacents:
            if is_legal(adjacent) and arr[adjacent] == player:
                if player == 1:
                    count_x += 1
                elif player == 0:
                    count_o += 1
    return __rule_advantage(count_o, count_x, player)

def compact_board_version2(board: Board, player: PlayerID) -> float:
    """counts the O close to others O and the X close to others X and returns a score
        only takes into consideration the positions inside the board not the perimeter"""
    count_x, count_o = 0, 0
    arr = board.ndarray
    for pos in [(x, y) for x in range(1,4) for y in range(1,4)]:
        player = arr[pos]
        if player not in (0, 1):
            continue
        adjacents = [(pos[0]-1,pos[1]-1),(pos[0]-1,pos[1]),(pos[0]-1,pos[1]+1),(pos[0]+1,pos[1]-1),(pos[0]+1,pos[1]),(pos[0]+1,pos[1]+1),(pos[0],pos[1]-1),(pos[0],pos[1]+1)]
        for adjacent in adjacents:
            if arr[adjacent] == player:
                if player == 1:
                    count_x += 1
                elif player == 0:
                    count_o += 1
    return __rule_advantage(count_o, count_x, player)

def more_disturbing_pieces(board: Board, player: PlayerID) -> float:
    """counts the O close to X and the X close to O and returns a score"""
    count_x = 0
    count_o = 0
    arr = board.ndarray
    for pos in [(x, y) for x in range(5) for y in range(5)]:
        if arr[pos] == 1:
            for pos1 in [(pos[0]-1,pos[1]-1),(pos[0]-1,pos[1]),(pos[0]-1,pos[1]+1),(pos[0]+1,pos[1]-1),(pos[0]+1,pos[1]),(pos[0]+1,pos[1]+1),(pos[0],pos[1]-1),(pos[0],pos[1]+1)]:
                if is_legal(pos1):
                    if arr[pos1] == 0:
                        count_x = count_x + 1
        elif arr[pos] == 0:
            for pos1 in [(pos[0]-1,pos[1]-1),(pos[0]-1,pos[1]),(pos[0]-1,pos[1]+1),(pos[0]+1,pos[1]-1),(pos[0]+1,pos[1]),(pos[0]+1,pos[1]+1),(pos[0],pos[1]-1),(pos[0],pos[1]+1)]:
                if is_legal(pos1):
                    if arr[pos1] == 1:
                        count_o  = count_o + 1
    return __rule_advantage(count_o, count_x, player)

def is_legal(pos: tuple) -> bool:
    """utility func for compact_board"""
    return 0 <= pos[0] and pos[0] < 5 and 0 <= pos[1] and pos[1] < 5

def board_majority(board: Board, player: PlayerID) -> int:
    """advisor based on the difference of placed tiles between the players"""
    total_count: int = int(Board.change_symbols(board.ndarray).sum())
    return total_count * 2 + 50 if player == 1 else 50 - 2 * total_count

ALL_ADVISORS: list[Advisor] = [
    line_majority,
    # compact_board,                # TODO: somehow makes the agent slow down a loooot
    available_moves_majority,
    board_majority,
    more_disturbing_pieces
]
