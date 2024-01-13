from lib.game import Game, Player, Move
from random import choice
from src.board import Board

class BetterRandomPlayer(Player):
    """Player class that should not get stuck in infinite stochastic loops"""
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: Game) -> tuple[tuple[int, int], Move]:
        """needed by the library to interface"""
        return self.choose_move(game)

    def choose_move(self, game: Game) -> tuple[tuple[int, int], Move]:
        chosen_move = choice(Board(game.get_board()).list_moves(current_player = game.get_current_player()))
        #need to invert from the numpy indexing to the game indexing (rows vs columns)
        return  ((chosen_move[0][1], chosen_move[0][0]), chosen_move[1]) # type: ignore
