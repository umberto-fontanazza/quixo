from __future__ import annotations
from src.oracle import Oracle
from src.board import Board, CompleteMove
from src.player import PlayerID, change_player, player_int
from lib.game import Game, Move, Player
from joblib import Parallel, delayed
from typing import Callable, Literal
from functools import wraps

SCORE_VICTORY = 100
SCORE_LOSS = 0

class Agent(Player):
    def __init__(self, oracle_weights: list[float] | None = None, depth_limit: int = 4) -> None:
        super().__init__()
        self.__oracle = Oracle(weights = oracle_weights)
        self.__episode: list[Board] = []
        self.depth_limit = depth_limit
        self.training = True

    def __easy_win_complex_boards(self, current_board: Board, current_player: PlayerID, opponent: PlayerID, minmax: Literal['min', 'max']) -> tuple[bool, list[Board]]:
        """returns a tuple: 1st element is found an easy win, second is the filtered list"""
        future_boards: list[Board] = [current_board.move(move, current_player if minmax == 'max' else opponent) for move in current_board.list_moves(current_player, shuffle=True, filter_out_symmetrics=True)]
        complex_future_boards = []
        for future_board in future_boards:
            winners = future_board.check_winners()
            if minmax == 'max':
                if current_player in winners and len(winners) == 1:
                    return True, []
                if opponent not in winners:
                    complex_future_boards.append(future_board)
            elif minmax == 'min':
                if opponent in winners and len(winners) == 1:
                    return True, []
                if current_player not in winners:
                    complex_future_boards.append(future_board)
        return False, complex_future_boards

    def __max(self, board: Board, current_player: PlayerID, beta: float = 100.0, curr_depth: int = 0) -> float:
        opponent = change_player(current_player)
        # if we are above the tree depth limit, return the oracle predictions
        if curr_depth >= self.depth_limit:
            return self.oracle.advantage(board, current_player)
        easy_win, complex_future_boards = self.__easy_win_complex_boards(board, current_player, opponent, 'max')
        # if some board is directly winnable by the agent, return maximum
        if easy_win:
            return SCORE_VICTORY
        # if all the boards are won by the opponent, return max = 0
        if len(complex_future_boards) == 0:
            return SCORE_LOSS
        # go on with standard minimax
        alpha = SCORE_LOSS
        for board in complex_future_boards:
            tmp = self.__min(board, current_player, alpha, curr_depth + 1) # compute the min value for a board
            if tmp > beta:
                return tmp
            alpha = tmp if tmp > alpha else alpha                   # update alpha with the biggest value found so far
        return alpha

    def __min(self, board: Board, current_player: PlayerID, alpha: float = 0.0, curr_depth: int = 1) -> float:
        opponent = change_player(current_player)
        #if we are above the tree depth limit, return the prediction
        if curr_depth >= self.depth_limit:
            return self.oracle.advantage(board, current_player)
        easy_win, complex_future_boards = self.__easy_win_complex_boards(board, current_player, opponent, 'min')
        # if some board is directly winnable by opponent, return minimum
        if easy_win:
            return SCORE_LOSS
        # if all the boards are won by the current player, return min = 100
        if len(complex_future_boards) == 0:
            return SCORE_VICTORY
        # look for the other moves using minimax + pruning
        beta = SCORE_VICTORY                                        # largest oracle value
        for board in complex_future_boards:
            tmp = self.__max(board, current_player, beta, curr_depth + 1)
            if tmp < alpha:                                         # if we find a value smaller than alpha we stop and we return this value
                return tmp
            beta = tmp if tmp < beta else beta                      # update beta with the smallest value found so far
        return beta

    def make_move(self, game: Game) -> tuple[tuple[int, int], Move]:
        """Alias is required by lib"""
        current_player = 1 if game.get_current_player() in (1, 'X') else 0
        position, slide = self.choose_move(Board(game.get_board()), current_player, parallel = False if self.__depth_limit <= 1 else True)
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

    def __parallel_minmax(self, board: Board, complex_moves: list[CompleteMove], current_player: PlayerID) -> list[float]:
        """minmax with min wrapper for multithreading"""
        min_wrapper = lambda board, current_player, alpha, curr_depth: self.__min(board, current_player, alpha, curr_depth)
        scores: list[float] = Parallel(n_jobs=-1)(delayed(min_wrapper)(board.move(move, current_player), current_player, 0.0, 1) for move in complex_moves)      #type: ignore
        return scores

    @use_for_training
    def choose_move(self, board: Board, current_player: PlayerID, parallel: bool = False) -> CompleteMove:
        """Choose and return a move, without applying it to the board"""
        moves: list[CompleteMove] =  board.list_moves(current_player, shuffle=True,  filter_out_symmetrics = True)
        current_player, opponent = player_int(current_player), change_player(current_player)
        # checks if some moves give an instant win, filters moves that make the opponent win
        complex_moves: list[CompleteMove] = []
        for move in moves:
            winner = board.move(move, current_player).winner(current_player = opponent)
            if winner == current_player:
                return move
            elif winner is None:
                complex_moves.append(move)
        # if all moves make opponent win, choose a random one
        if len(complex_moves) == 0:
            return moves[0]
        if parallel:    # parallel minmax
            scores = self.__parallel_minmax(board, complex_moves, current_player)
        else:           # sequential minmax
            scores: list[float] = [self.__min(board.move(move, current_player), current_player) for move in complex_moves]
        chosen_move, _ = max(zip(complex_moves, scores), key = lambda tup: tup[1])
        return chosen_move

    def __train(self, board: Board, next_board: Board, current_player: PlayerID) -> None:
        """board = result of opponent move, next_board = board + my move"""
        if not self.training:
            return
        if not board.is_empty and (not (len(self.__episode) == 0 and board.min_played_moves > 1)):
            self.__episode.append(board)
        if not (len(self.__episode) == 0 and board.min_played_moves > 2):
            self.__episode.append(next_board)
        opponent = change_player(current_player)
        if next_board.winner(current_player = opponent):
            # leaving the last one out because it's a trivial prediction
            self.oracle.feedback(self.__episode[:-1], current_player, 'Win')
            self.__episode = []
        elif any([next_board.move(move, opponent).winner(current_player = current_player) for move in next_board.list_moves(opponent, filter_out_symmetrics = True)]):
            self.oracle.feedback(self.__episode, current_player, 'Loss')
            self.__episode = []

    @property
    def oracle(self) -> Oracle:
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
        oracle = Oracle.from_json(json_string)
        return Agent(oracle.weights)