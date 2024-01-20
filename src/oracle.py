from __future__ import annotations
from src.board import Board, Outcome
from src.player import PlayerID
from src.advisor import Advisor, ALL_ADVISORS
from json import dumps, loads

class Oracle():
    def __init__(self, rules: list[Advisor] = ALL_ADVISORS, weights: list[float] | None = None):
        self.__rules = rules
        if not weights or len(weights) != len(rules):
            self.__weights = [1 for _ in rules]
        else:
            self.__weights = weights

    @staticmethod
    def __is_good_prediction(score: float, outcome: Outcome) -> bool:
        if score >= 50 and outcome == 'Win':
            return True
        if score < 50 and outcome == 'Loss':
            return True
        return False

    def __adjust_rule_weights(self, board: Board, player: PlayerID, outcome: Outcome):
        growth_factor = .1
        shrink_factor = .1
        rule_scores: list[float] = [rule(board, player) for rule in self.__rules]
        rule_success = [self.__is_good_prediction(score, outcome) for score in rule_scores]
        updated_weights = []
        for success, weight in zip(rule_success, self.weights):
            if success:
                updated_weight = weight * (1 + growth_factor)
            else:
                updated_weight = weight * (1 - shrink_factor)
            updated_weights.append(updated_weight)
        self.__weights = updated_weights

    def feedback(self, board_states: list[Board], player: PlayerID, outcome: Outcome) -> None:
        for board in board_states:
            self.__adjust_rule_weights(board, player, outcome)

    def advantage(self, board: Board, player: PlayerID) -> float:
        """Returns win likelihood for the @param{player}"""
        advisor_advantages: list[float] = [rule(board, player) for rule in self.__rules]
        total_score = 0
        for i, rule_score in enumerate(advisor_advantages):
            rule_weight = self.__weights[i]
            total_score += rule_score * rule_weight
        return total_score / sum(self.__weights)

    def to_json(self) -> str:
        return dumps(self.weights)

    @staticmethod
    def from_json(json_string: str):
        data = loads(json_string)
        return Oracle()

    @property
    def weights(self):
        return [weight for weight in self.__weights]