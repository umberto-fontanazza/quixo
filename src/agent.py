from __future__ import annotations
from src.oracle_stats import StatsOracle
from src.board_stats import BoardStats
from src.board import CompleteMove
from src.player import PlayerID, change_player, player_int
from lib.game import Game, Move, Player
from joblib import Parallel, delayed
from typing import Callable, Literal
from functools import wraps

SCORE_VICTORY = 100
SCORE_LOSS = 0

GOOD_WEIGHTS = [75.66562344604507, 6.235901212974498, 8.553351675764317, 35.104301950764615]

class Agent(Player):
    def __init__(self, oracle_weights: list[float] | None = None, depth_limit: int = 4) -> None:
        super().__init__()
        # self.__oracle = Oracle(weights = oracle_weights)
        self.__oracle: StatsOracle = StatsOracle(weights = oracle_weights)
        self.__episode: list[BoardStats] = []
        self.depth_limit = depth_limit
        self.training = True

    def __easy_win_complex_boards_moves(self, current_board: BoardStats, current_player: PlayerID, opponent: PlayerID, minmax: Literal['min', 'max']) -> tuple[bool, list[BoardStats], list[CompleteMove]]:
        """returns a tuple: 1st element is found an easy win, 2nd is the filtered board list, 3rd is filtered moves list"""
        moves_player: PlayerID = current_player if minmax == 'max' else opponent                          # player that makes the move
        moves_players_opponent: PlayerID = opponent if minmax == 'max' else current_player                # and his opponent
        possible_moves: list[CompleteMove] = current_board.list_moves(moves_player, shuffle=True, filter_out_symmetrics=True)
        future_boards: list[BoardStats] = [current_board.move(move, moves_player) for move in possible_moves]
        complex_future_boards: list[BoardStats] = []
        complex_moves: list[CompleteMove] = []
        for future_board, move in zip(future_boards, possible_moves):
            winners = future_board.check_winners()
            if moves_player in winners and len(winners) == 1:
                return True, [future_board], [move]
            if moves_players_opponent not in winners:
                complex_future_boards.append(future_board)
                complex_moves.append(move)
        return False, complex_future_boards, complex_moves

    def __min_max(self, board: BoardStats, current_player: PlayerID, minmax: Literal['min', 'max'], alpha: float = 0.0, beta: float = 100.0, curr_depth: int = 1) -> float:
        opponent = change_player(current_player)
        # if we are above the tree depth limit, return the oracle predictions
        if curr_depth >= self.depth_limit:
            return self.oracle.advantage(board, current_player)
        easy_win, complex_future_boards, _ = self.__easy_win_complex_boards_moves(board, current_player, opponent, minmax)
        best_value = SCORE_LOSS if minmax == 'max' else SCORE_VICTORY       # used for early returns
        # if some board is directly winnable, return the corresponding score: (100 - best_value)
        if easy_win:
            return 100 - best_value
        # if all the boards are won by the opponent, return max = 0 or min = 100 (best_value)
        if len(complex_future_boards) == 0:
            return best_value
        # minimax with a/b pruning
        for future_board in complex_future_boards:
            if minmax == 'max':
                tmp = self.__min_max(future_board, current_player, 'min', alpha, beta, curr_depth + 1)
                best_value = max(best_value, tmp)
                alpha = max(alpha, best_value)
            else:
                tmp = self.__min_max(future_board, current_player, 'max', alpha, beta, curr_depth + 1)
                best_value = min(best_value, tmp)
                beta = min(beta, best_value)
            if beta <= alpha:                   # pruning
                break
        return best_value

    def __parallel_minmax(self, board: BoardStats, complex_moves: list[CompleteMove], current_player: PlayerID, minmax: Literal['min', 'max']) -> list[float]:
        """minmax wrapper for multithreading"""
        minmax_wrapper = lambda board, current_player, minmax, alpha, beta, curr_depth: self.__min_max(board, current_player, minmax, alpha, beta, curr_depth)
        scores: list[float] = Parallel(n_jobs=-1)(delayed(minmax_wrapper)(board.move(move, current_player), current_player, 'min', 0.0, 100.0, 1) for move in complex_moves)      #type: ignore
        return scores

    def make_move(self, game: Game) -> tuple[tuple[int, int], Move]:
        """Alias is required by lib"""
        current_player = 1 if game.get_current_player() in (1, 'X') else 0
        position, slide = self.choose_move(BoardStats(array = game.get_board()), current_player, parallel = False if self.__depth_limit <= 1 else True)
        position = (position[1], position[0])
        return position, slide

    @staticmethod
    def use_for_training(choose_move_method) -> Callable:
        @wraps(choose_move_method) # TODO: https://stackoverflow.com/questions/147816/preserving-signatures-of-decorated-functions fixes help() but Pylance is dumb
        def wrapper(*args, **kwargs):
            agent, board, player = [*args, *kwargs.values()][:3]
            chosen_move = choose_move_method(*args, **kwargs)
            next_board = board.move(chosen_move, player)
            agent.__train(board, next_board, player)
            return chosen_move
        return wrapper

    @use_for_training
    def choose_move(self, board: BoardStats, current_player: PlayerID, parallel: bool = False) -> CompleteMove:
        """Choose and return a move, without applying it to the board"""
        current_player, opponent = player_int(current_player), change_player(current_player)
        easy_win, _, complex_moves = self.__easy_win_complex_boards_moves(board, current_player, opponent, 'max')
        if easy_win:                            # return the winning move you found
            return complex_moves[0]
        if len(complex_moves) == 0:             # return random move if the opponent wins in any case
            return board.list_moves(current_player, shuffle=True, filter_out_symmetrics = True)[0]
        if parallel:                            # parallel minmax
            scores = self.__parallel_minmax(board, complex_moves, current_player, 'min')
        else:                                   # sequential minmax
            scores: list[float] = [self.__min_max(board.move(move, current_player), current_player, 'min') for move in complex_moves]
        chosen_move, _ = max(zip(complex_moves, scores), key = lambda tup: tup[1])
        return chosen_move

    def __train(self, board: BoardStats, next_board: BoardStats, current_player: PlayerID) -> None:
        """board = result of opponent move, next_board = board + my move"""
        if not self.training:
            return
        if not board.is_empty and (not (len(self.__episode) == 0 and board.min_played_moves > 1)):
            self.__episode.append(board)
        if not (len(self.__episode) == 0 and board.min_played_moves > 2):
            self.__episode.append(next_board)
        opponent = change_player(current_player)
        if next_board.winner(current_player = opponent) == current_player:
            # leaving the last one out because it's a trivial prediction
            self.oracle.feedback(self.__episode[:-1], current_player, 'Win')
            self.__episode = []
        elif any([next_board.move(move, opponent).winner(current_player = current_player) == opponent for move in next_board.list_moves(opponent, filter_out_symmetrics = True)]):
            self.oracle.feedback(self.__episode, current_player, 'Loss')
            self.__episode = []

    @property
    def oracle(self) -> StatsOracle:
        return self.__oracle

    @property
    def depth_limit(self) -> int:
        return self.__depth_limit

    @depth_limit.setter
    def depth_limit(self, depth_limit: int) -> None:
        if not isinstance(depth_limit, int) or depth_limit <= 0:
            raise ValueError(f'{type(depth_limit) =}, {depth_limit =}')
        self.__depth_limit = depth_limit

    @property
    def training(self) -> bool:
        return self.__training

    @training.setter
    def training(self, training: bool) -> None:
        if not training:
            self.__episode = []
        self.__training = training

    def save(self, filename = 'trained_agent.json'):
        with open(filename, 'w') as file:
            file.write(self.to_json())

    def to_json(self) -> str:
        return self.oracle.to_json()

    @staticmethod
    def from_json(json_string: str):
        oracle = StatsOracle.from_json(json_string)
        return Agent(oracle.weights)