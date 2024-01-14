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
        current_player = 1 if game.get_current_player() else 0
        moves = boardcopy.list_moves(current_player)               # type: ignore
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
        chosen_move = choice(Board(game.get_board()).list_moves(current_player = game.get_current_player())) #type: ignore
        #need to invert from the numpy indexing to the game indexing (rows vs columns)
        return  ((chosen_move[0][1], chosen_move[0][0]), chosen_move[1]) # type: ignore


class ManualPlayer(Player):
    """Random Player class that should not get stuck in infinite stochastic loops"""
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: Game) -> tuple[tuple[int, int], Move]:
        """needed by the library to interface"""
        return self.choose_move(game)

    def print_pretty_board(self, game: Game) -> None:
        boardcopy = game.get_board()
        stringy_board = [['❌' if elem == 1 else '⭕️' if elem == 0 else '⬜️' for elem in row] for row in boardcopy]
        for row in stringy_board:
            print(row, '\n')

    def choose_move(self, game: Game) -> tuple[tuple[int, int], Move]:
        self.print_pretty_board(game)
        boardcopy = Board(game.get_board())
        available_moves = boardcopy.list_moves(game.get_current_player(), filter_out_symmetrics=True) #type: ignore
        for index, move in enumerate(available_moves):
            print('index', index, '->', move)
        ok = False
        while not ok:
            move_index = int(input('choose a move index from the list: '))
            if move_index < len(available_moves) and move_index >= 0:
                ok = True
        chosen_move = available_moves[move_index] #type: ignore
        return  ((chosen_move[0][1], chosen_move[0][0]), chosen_move[1]) # type: ignore