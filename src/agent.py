from src.oracle import Oracle
from src.board import Board, Outcome
from src.position import Position
from lib.game import Game, Move, Player
from typing import Literal
from src.simple_agents import BetterRandomPlayer, CleverPlayer

class DelphiPlayer(Player):
    def __init__(self, oracle_weights: list[float] | None = None, tree_depth: int = 4) -> None:
        super().__init__()
        self.__oracle = Oracle(weights = oracle_weights)
        self.__episode: list[Board] = []
        self.depth_limit = tree_depth
        self.player_index: int = 1
        self.training = True
        self.__previous_board_sum: int = -25
        self.__last_game_player_index = -1
        self.__last_chosen_future = None

    def __max(self, board: Board, current_player: Literal[0,1], beta: float = 100.0, curr_depth: int = 0) -> float:
        #check if the board is a terminal condition
        value = Board.check_for_terminal_conditions(board, current_player)
        if value >= 0:
            return value
        #check if we are above the tree depth limit
        if curr_depth >= self.depth_limit:
            return self.oracle.advantage(board, current_player)
        alpha = 0.0                                                 # smallest oracle value
        future_boards: list[Board] = [board.move(move, current_player) for move in board.list_moves(current_player, shuffle=True, filter_out_symmetrics=True)]
        for b in future_boards:
            tmp = self.__min(b, self.player_index, alpha, curr_depth + 1) # compute the min value for a board
            if tmp > beta:
                return tmp
            alpha = tmp if tmp > alpha else alpha                   # update alpha with the biggest value found so far
        return alpha

    def __min(self, board: Board, current_player: Literal[0,1], alpha: float = 0.0, curr_depth: int = 1) -> float:
        #check if the board is a terminal condition
        value = Board.check_for_terminal_conditions(board, current_player)
        if value >= 0:
            return value
        #check if we are above the tree depth limit
        if curr_depth >= self.depth_limit:
            return self.oracle.advantage(board, current_player)
        beta = 100.0                                                # largest oracle value
        future_boards: list[Board] = [board.move(move, current_player) for move in board.list_moves(current_player, shuffle=True, filter_out_symmetrics=True)]
        for b in future_boards:
            tmp = self.__max(b, self.player_index, beta, curr_depth + 1)
            if tmp < alpha:                                         # if we find a value smaller than alpha we stop and we return this value
                return tmp
            beta = tmp if tmp < beta else beta                      # update beta with the smallest value found so far
        return beta

    def make_move(self, game: Game) -> tuple[tuple[int, int], Move]:
        """Alias is required by lib"""
        position, slide = self.choose_move(game)
        position = position.as_tuple()
        position = (position[1], position[0])
        return position, slide

    def choose_move(self, game: Game) -> tuple[Position, Move]:
        """Choose and return a move, without applying it to the board"""
        current_player: Literal[0, 1] = game.get_current_player() # type: ignore
        self.player_index = current_player
        board = Board(game.get_board())
        moves: list[tuple[Position, Move]] =  board.list_moves(current_player, shuffle=True, filter_out_symmetrics=True)
        future_boards: list[Board] = [board.move(move, current_player) for move in moves]
        evaluated: list[tuple[Board, float, tuple[Position, Move]]] = [(b, self.__min(b, self.player_index), p) for b, p in zip(future_boards, moves)]
        chosen_move: tuple[Board, float, tuple[Position, Move]] = max(evaluated, key = lambda move_qual: move_qual[1])
        self.__autotrain_oracle(board, chosen_move)
        self.__episode.append(chosen_move[0])
        return chosen_move[2]

    def __is_winning_future(self, future: tuple[Board, float, tuple[Position, Move]]) -> bool:
        """checks if the future position is a winning state"""
        if Board.check_for_terminal_conditions(future[0], self.__last_game_player_index) == 100:
            return True
        return False

    def __autotrain_oracle(self, board: Board, chosen_future: tuple[Board, float, tuple[Position, Move]]) -> None:
        """caveat: does not work if the opponent made the agent win"""
        self.__last_game_player_index = self.player_index if self.__last_game_player_index == -1 else self.__last_game_player_index
        new_board_sum = board.ndarray.sum()
        if new_board_sum > self.__previous_board_sum:       # exit if it is the normal course of events (match not ended)
            self.__previous_board_sum = new_board_sum
            self.__last_chosen_future = chosen_future
            return
        self.__previous_board_sum = new_board_sum
        if not self.training:                             # clean up and exit if not in training mode
            self.__episode = []
            return
        self.train_oracle(self.__last_game_player_index, 'Win' if self.__is_winning_future(self.__last_chosen_future) else 'Loss')
        self.__last_game_player_index = self.player_index   # update parameters
        self.__last_chosen_future = chosen_future

    def train_oracle(self, player: Literal[0, 1, 'O', 'X'], outcome: Outcome) -> None:
        """at the end of a game, gives feedback to the oracle"""
        self.oracle.feedback(self.__episode, player, outcome)
        self.__episode = []

    @property
    def oracle(self) -> Oracle:
        return self.__oracle

    @property
    def depth_limit(self) -> int:
        return self.__depth_limit

    @depth_limit.setter
    def depth_limit(self, depth_limit: int) -> None:
        if not isinstance(depth_limit, int) and depth_limit > 0:
            raise ValueError(f'{type(depth_limit) =}, {depth_limit =}')
        self.__depth_limit = depth_limit

    @property
    def training(self) -> bool:
        return self.__training

    @training.setter
    def training(self, training: bool) -> None:
        # TODO: if setting to false clear cached boards and forecasts
        self.__training = training
