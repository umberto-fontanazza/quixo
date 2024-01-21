from __future__ import annotations
from src.board import Outcome
from src.player import PlayerID
from src.board_stats import BoardStats
from json import dumps, loads

class StatsOracle():
    def __init__(self, weights: list[float] | None = None):
        stats = BoardStats().all_stats
        if not weights or len(weights) != len(stats):
            self.__weights = [1 for _ in stats]
        else:
            self.__weights = weights

    @staticmethod
    def __is_good_prediction(score: float, outcome: Outcome) -> bool:
        if score >= 50 and outcome == 'Win':
            return True
        if score < 50 and outcome == 'Loss':
            return True
        return False

    def __compute_stats_scores(self, board_stats: BoardStats, player: PlayerID) -> list[float]:
        """from the stats of the board returns some scores between 0 and 100"""
        if player in ("X",1):
            return [((stat[1] - stat[0]) / stat[2]) * 50 + 50 for stat in board_stats.all_stats]    #statX - statO
        return [((stat[0] - stat[1]) / stat[2]) * 50 + 50 for stat in board_stats.all_stats]        #statO - statX

    def __adjust_rule_weights(self, board_stats: BoardStats, player: PlayerID, outcome: Outcome):
        growth_factor = .001
        shrink_factor = .001
        stats_scores = self.__compute_stats_scores(board_stats, player)
        stats_success = [self.__is_good_prediction(stat_score, outcome) for stat_score in stats_scores]
        updated_weights = []
        for success, weight in zip(stats_success, self.weights):
            if success:
                updated_weight = weight * (1 + growth_factor)
            else:
                updated_weight = weight * (1 - shrink_factor)
            updated_weights.append(updated_weight)
        self.__weights = updated_weights

    def feedback(self, board_stats: list[BoardStats], player: PlayerID, outcome: Outcome) -> None:
        for board in board_stats:
            self.__adjust_rule_weights(board, player, outcome)

    def advantage(self, board_stats: BoardStats, player: PlayerID) -> float:
        """Returns win likelihood for the @param{player}"""
        stats_scores = self.__compute_stats_scores(board_stats, player)
        total_score = 0
        for i, stat_score in enumerate(stats_scores):
            total_score += stat_score * self.__weights[i]
        return total_score / sum(self.__weights)

    def to_json(self) -> str:
        return dumps(self.weights)

    @staticmethod
    def from_json(json_string: str):
        data = loads(json_string)
        return StatsOracle()

    @property
    def weights(self):
        return [weight for weight in self.__weights]