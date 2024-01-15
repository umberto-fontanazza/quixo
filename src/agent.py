from src.oracle import Oracle
from src.board import Board, PlayerID
from src.position import Position
from lib.game import Game, Move, Player
from joblib import Parallel, delayed
from typing import Literal

class DelphiPlayer(Player):
    def __init__(self, oracle_weights: list[float] | None = None, tree_depth: int = 4) -> None:
        super().__init__()
        self.__oracle = Oracle(weights = oracle_weights)
        self.__episode: list[Board] = []
        self.depth_limit = tree_depth
        self.player_index: PlayerID = 1
        self.training = True
        """         self.__previous_board_sum: int = -25
        self.__last_game_player_index = -1
        self.__last_chosen_future = None """

    def __max(self, board: Board, current_player: PlayerID, beta: float = 100.0, curr_depth: int = 0) -> float:
        #check if the board is a terminal condition
        value = board.check_for_terminal_conditions(current_player)
        if value >= 0:
            return value
        #check if we are above the tree depth limit
        if curr_depth >= self.depth_limit:
            return self.oracle.advantage(board, current_player)
        alpha = 0.0                                                 # smallest oracle value
        future_boards: list[Board] = [board.move(move, current_player) for move in board.list_moves(current_player, shuffle=True, filter_out_symmetrics=True)]
        for board in future_boards:
            tmp = self.__min(board, self.player_index, alpha, curr_depth + 1) # compute the min value for a board
            if tmp > beta:
                return tmp
            alpha = tmp if tmp > alpha else alpha                   # update alpha with the biggest value found so far
        return alpha
    
    def compute_score(self, board: Board, current_player: PlayerID, alpha: float = 0.0, curr_depth: int = 1) -> float:
        """wrapper for multithreading the min function"""
        return self.__min(board, current_player, alpha, curr_depth)

    def __min(self, board: Board, current_player: PlayerID, alpha: float = 0.0, curr_depth: int = 1) -> float:
        #check if the board is a terminal condition
        value = board.check_for_terminal_conditions(current_player)
        if value >= 0:
            return value
        #check if we are above the tree depth limit
        if curr_depth >= self.depth_limit:
            return self.oracle.advantage(board, current_player)
        beta = 100.0                                                # largest oracle value
        future_boards: list[Board] = [board.move(move, current_player) for move in board.list_moves(current_player, shuffle=True, filter_out_symmetrics=True)]
        for board in future_boards:
            tmp = self.__max(board, self.player_index, beta, curr_depth + 1)
            if tmp < alpha:                                         # if we find a value smaller than alpha we stop and we return this value
                return tmp
            beta = tmp if tmp < beta else beta                      # update beta with the smallest value found so far
        return beta

    def make_move(self, game: Game) -> tuple[tuple[int, int], Move]:
        """Alias is required by lib"""
        position, slide = self.choose_move(game, use_multithreading = False if self.__depth_limit <= 1 else True)
        position = position.as_tuple()
        position = (position[1], position[0])
        return position, slide

    def choose_move(self, game: Game, use_multithreading: bool) -> tuple[Position, Move]:
        """Choose and return a move, without applying it to the board"""
        current_player: Literal[0, 1] = game.get_current_player() # type: ignore
        self.player_index, opponent = current_player, 1 - current_player
        board = Board(game.get_board())
        moves: list[tuple[Position, Move]] =  board.list_moves(current_player, shuffle=True, filter_out_symmetrics=True)
        future_boards = [board.move(move, current_player) for move in moves]
        if not use_multithreading:      # standard minmax
            scores: list[float] = [self.__min(board, current_player) for board in future_boards]
        else:
            scores:list[float]  = Parallel(n_jobs=-1)(delayed(self.compute_score)(board, current_player) for board in future_boards)    #type: ignore
        chosen_move, next_board, _ = max(zip(moves, future_boards, scores), key = lambda triplet: triplet[2])
        if self.training:
            self.__train(board, next_board, current_player, opponent)
        return chosen_move

    def __train(self, board: Board, next_board: Board, current_player, opponent) -> None:
        if not board.is_empty and (not (len(self.__episode) == 0 and board.min_played_moves > 1)):
            self.__episode.append(board)
        if not (len(self.__episode) == 0 and board.min_played_moves > 2):
            self.__episode.append(next_board)
        if next_board.only_winner(current_player):
            # leaving the last one out because it's a trivial prediction
            self.oracle.feedback(self.__episode[:-1], current_player, 'Win')
            self.__episode = []
        if any([next_board.move(move, opponent).only_winner(opponent) for move in next_board.list_moves(opponent, filter_out_symmetrics = True)]):
            self.oracle.feedback(self.__episode, current_player, 'Loss')
            self.__episode = []

    """     def __is_winning_future(self, future_board: Board) -> bool:
        player = self.__last_game_player_index
        winners = future_board.check_winners()
        return player in winners and len(winners) == 1

    def __autotrain_oracle(self, board: Board, next_board: Board, move_score: float, move: tuple[Position, Move]) -> None:
        self.__last_game_player_index = self.player_index if self.__last_game_player_index == -1 else self.__last_game_player_index
        new_board_sum = board.ndarray.sum()
        if new_board_sum > self.__previous_board_sum:       # exit if it is the normal course of events (match not ended)
            self.__previous_board_sum = new_board_sum
            self.__last_chosen_future = move, next_board, move_score
            return
        self.__previous_board_sum = new_board_sum
        if not self.training:                             # clean up and exit if not in training mode
            self.__episode = []
            return
        self.train_oracle(self.__last_game_player_index, 'Win' if self.__is_winning_future(self.__last_chosen_future[1]) else 'Loss')
        self.__last_game_player_index = self.player_index   # update parameters
        self.__last_chosen_future = move, next_board, move_score

    def train_oracle(self, player: Literal[0, 1, 'O', 'X'], outcome: Outcome) -> None:
        self.oracle.feedback(self.__episode, player, outcome)
        self.__episode = [] """

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
        return DelphiPlayer(oracle.weights)