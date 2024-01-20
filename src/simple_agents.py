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
        moves =  board.list_moves(current_player, filter_out_symmetrics=True)
        future_boards = [board.move(move, current_player) for move in moves]
        cooked_moves = []                                                       #will contain moves that do not make you lose
        for future_board, move in zip(future_boards, moves):
            winner = future_board.winner(1 - current_player)
            if winner is None:
                cooked_moves.append(move)
            elif winner == current_player:
                return ((move[0][1], move[0][0]), move[1])
        chosen_move = choice(cooked_moves) if len(cooked_moves) != 0 else choice(moves)
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