from src.card_duel.player import Player
from src.card_duel.board import Board


class Rules:
    def __init__(self, rounds_to_win: int = 2):
        self.rounds_to_win = rounds_to_win

    def is_round_over(self, players: list[Player]) -> bool:
        players_passed = []
        for player in players:
            players_passed.append(player.has_passed)
        return all(players_passed)
    # return all(player.has_passed for player in players)

    def get_round_winner_id(self,
                            board: Board,
                            players: list[Player]) -> int | None:

        power_by_player_id = {}
        for player in players:
            power = board.get_total_power(player.id)
            power_by_player_id[player.id] = power

        max_power = max(power_by_player_id.values())

        winner_ids = []
        for player_id, power in power_by_player_id.items():
            if power == max_power:
                winner_ids.append(player_id)

        if len(winner_ids) == 1:
            return winner_ids[0]
        return None

    def is_match_over(self, players: list[Player]) -> bool:
        for player in players:
            if player.rounds_won >= self.rounds_to_win:
                return True
        return False
    # return any(player.rounds_won >= self.rounds_to_win for player in players)

    def get_match_winner_id(self, players: list[Player]) -> int | None:
        qualified = []
        for player in players:
            if player.rounds_won >= self.rounds_to_win:
                qualified.append(player)

        if len(qualified) == 1:
            return qualified[0].id
        return None
