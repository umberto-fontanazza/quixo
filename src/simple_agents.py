from lib.game import Game, Player, Move
from random import choice
from src.board import Board

class CleverPlayer(Player):
    """Player class that does not make the opponent win with a move and tries to win if possible"""
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: Game) -> tuple[tuple[int, int], Move]:
        """needed by the library to interface"""
        return self.choose_move(game)

    def choose_move(self, game: Game) -> tuple[tuple[int, int], Move]:
        board: Board = Board(game.get_board())
        current_player = game.get_current_player()
        moves = board.list_moves(current_player)
        cooked_moves = []
        for move in moves:
            # TODO: why is the next line inside a loop?
            terminal_value = board.check_for_terminal_conditions(current_player)
            if terminal_value == 100:
                return ((move[0][1], move[0][0]), move[1])
            elif terminal_value == -1:
                cooked_moves.append(move)
        chosen_move = choice(cooked_moves) if len(cooked_moves) != 0 else choice(moves)
        #need to invert from the numpy indexing to the game indexing (rows vs columns)
        return ((chosen_move[0][1], chosen_move[0][0]), chosen_move[1]) # type: ignore

class BetterRandomPlayer(Player):
    """Random Player class that should not get stuck in infinite stochastic loops"""
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: Game) -> tuple[tuple[int, int], Move]:
        """needed by the library to interface"""
        return self.choose_move(game)

    def choose_move(self, game: Game) -> tuple[tuple[int, int], Move]:
        chosen_move = choice(Board(game.get_board()).list_moves(current_player = game.get_current_player()))
        #need to invert from the numpy indexing to the game indexing (rows vs columns)
        return  ((chosen_move[0][1], chosen_move[0][0]), chosen_move[1]) # type: ignore