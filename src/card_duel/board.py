from typing import List, Dict
from src.card_duel.card import RowAffinity, Card
from src.card_duel.row import Row


class Board:
    def __init__(self, player_ids: List[int]):
        self.player_ids = player_ids
        self.rows_by_player: Dict[int, Dict[RowAffinity, Row]] = {}

        ROW_LANES = (RowAffinity.MELEE, RowAffinity.RANGED, RowAffinity.SIEGE)

        for player_id in self.player_ids:
            player_rows: Dict[RowAffinity, Row] = {}

            for affinity in ROW_LANES:
                player_rows[affinity] = Row(name=affinity)

            self.rows_by_player[player_id] = player_rows

    def get_row(self, player_id: int, row_affinity: RowAffinity) -> Row:
        row = self.rows_by_player[player_id][row_affinity]
        return row

    def place_card(self,
                   player_id: int,
                   card: Card,
                   row_affinity: RowAffinity) -> None:

        row = self.get_row(player_id, row_affinity)
        row.add_card(card)

    def get_row_power(self, player_id: int, row_affinity: RowAffinity) -> int:
        row = self.get_row(player_id, row_affinity)
        return row.total_power()

    def get_total_power(self, player_id: int) -> int:
        total_power = 0
        for row in self.rows_by_player[player_id].values():
            total_power += row.total_power()
        return total_power
# sum(row.total_power() for row in self.rows_by_player[player_id].values())

    def clear(self) -> None:
        for player_id in self.rows_by_player:
            for row in self.rows_by_player[player_id].values():
                row.clear()

    def serialize(self) -> dict:
        rows_serialized: dict[int, dict[str, list[dict]]] = {}

        for player_id, rows_by_affinity in self.rows_by_player.items():
            player_rows: dict[str, list[dict]] = {}

            for affinity, row in rows_by_affinity.items():
                player_rows[affinity.name] = [
                    card.serialize() for card in row.cards
                ]

            rows_serialized[player_id] = player_rows

        return {
            "player_ids": list(self.player_ids),
            "rows": rows_serialized,
        }
