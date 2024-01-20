from src.board import Board, CompleteMove
from src.player import PlayerID
from lib.game import Move

# TODO: define some stats for the board: when you put one in
class BoardStats:
    def __init__(self,  board: Board, parent_board: Board | None = None, move: CompleteMove | None = None, player: PlayerID | None = None) -> None:
        # define stats that have to computed from scratch every time
        n_available_moves = board.count_moves()
        self.x_available_moves = n_available_moves[1]              # TODO: add more of these
        self.o_available_moves = n_available_moves[0]

        # define how to compute stats from a parent board
        if parent_board is not None and move is not None and player is not None:
            arr_parent = parent_board.ndarray
            if arr_parent[move[0]] == -1:
                if player in ('X', 1):
                    self.x_count = parent_board.stats.x_count + 1
                else:
                    self.o_count = parent_board.stats.o_count + 1
            else:
                self.o_count, self.x_count = parent_board.stats.o_count, parent_board.stats.x_count

        # define how to compute the SAME stats on a new board
        else:
            arr_board = board.ndarray
            self.x_count = arr_board[arr_board == 1].sum()
            self.o_count = arr_board[arr_board == 0].sum()


    @property
    def all_stats(self) -> list[int]:
        """get all the stats of the board"""
        return [
            self.x_count,
            self.o_count,
            self.x_available_moves,
            self.o_available_moves
        ]