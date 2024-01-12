from lib.game import Game, Player, Move

class BetterRandomPlayer(Player):
    """Player calss that should not get stuck in infinite stochastic loops"""
    def __init__(self) -> None:
        super().__init__()

    def choose_move(self, game: Game) -> tuple[tuple[int, int], Move]:
        return choice(Board(game.get_board()).list_moves(current_player = game.get_current_player())) # type: ignore