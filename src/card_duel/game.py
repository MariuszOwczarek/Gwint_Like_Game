from src.card_duel.card import RowAffinity
from src.card_duel.board import Board
from src.card_duel.player import Player
from src.card_duel.rules import Rules
from typing import List


class Game:
    def __init__(self,
                 players: List[Player],
                 board: Board,
                 rules: Rules) -> None:

        if not players:
            raise ValueError("Game requires at least one player")
        if len(players) != 2:
            raise ValueError("Current implementation supports "
                             "exactly 2 players")

        self.players: dict[int, Player] = {p.id: p for p in players}
        self.player_order: list[int] = [p.id for p in players]
        self.board: Board = board
        self.rules = rules
        self.current_round: int = 0
        self.active_player_id: int | None = None
        self.starting_player_id = self.player_order[0]
        self.is_round_active: bool = False

    def start_match(self) -> None:
        self.current_round = 0
        self.is_round_active = False
        self.board.clear()
        self.active_player_id = self.player_order[0]
        self.starting_player_id = self.player_order[0]
        for player in self.players.values():
            player.reset_for_new_match()

    def start_round(self) -> None:
        self.current_round += 1
        self.is_round_active = True
        for player in self.players.values():
            player.reset_for_new_round()

        if self.current_round > 1:
            self.starting_player_id = self.get_opponent_id(self.starting_player_id)

        self.active_player_id = self.starting_player_id
        self.board.clear()

    def get_active_player_id(self) -> int | None:
        return self.active_player_id

    def get_opponent_id(self, player_id: int) -> int:
        if player_id not in self.players:
            raise ValueError(f"Unknown player_id={player_id}")

        for player in self.players.keys():
            if player != player_id:
                return player

        raise ValueError(f"No opponent found for player_id={player_id}")

    def play_card(self,
                  player_id: int,
                  card_index: int,
                  row_affinity: RowAffinity) -> None:

        if player_id != self.active_player_id:
            raise ValueError(f"{player_id} is not active player")
        if self.players[player_id].has_passed:
            raise ValueError('No possibility to play card if turn passed')
        if not self.is_round_active:
            raise ValueError("Cannot play card when round is not active")

        card = self.players[player_id].play_card(card_index)
        self.board.place_card(player_id, card, row_affinity)

        if self.is_round_over():
            self.end_round()
        else:
            self.active_player_id = self.get_opponent_id(player_id)

    def pass_turn(self, player_id: int) -> None:
        if player_id != self.active_player_id:
            raise ValueError('Inactive player cannot pass turn')

        if not self.is_round_active:
            raise ValueError("Cannot pass when round is not active")

        self.players[player_id].pass_round()

        if self.is_round_over():
            self.end_round()
        else:
            self.active_player_id = self.get_opponent_id(player_id)

    def is_round_over(self) -> bool:
        return self.rules.is_round_over(list(self.players.values()))

    def end_round(self) -> None:
        player_list = list(self.players.values())
        winner_id = self.rules.get_round_winner_id(self.board, player_list)

        if winner_id is not None:
            self.players[winner_id].increment_rounds_won()
        self.is_round_active = False
        self.active_player_id = None

    def is_match_over(self) -> bool:
        return self.rules.is_match_over(list(self.players.values()))

    def get_match_winner_id(self) -> int | None:
        return self.rules.get_match_winner_id(list(self.players.values()))

    def serialize(self) -> dict:
        return {
            "players": [player.serialize()
                        for player
                        in self.players.values()],
            "board": self.board.serialize(),
            "rules": {
                "rounds_to_win": self.rules.rounds_to_win
            },
            "current_round": self.current_round,
            "active_player_id": self.active_player_id,
            "starting_player_id": self.starting_player_id,
            "is_round_active": self.is_round_active,
        }
