import pytest
from src.card_duel.board import Board
from src.card_duel.card import RowAffinity, Card
from src.card_duel.row import Row


def make_card(card_id: int,
              power: int,
              affinity: RowAffinity = RowAffinity.MELEE) -> Card:

    """Domyślnie tworzy kartę MELEE, ale pozwala zmienić affinity."""
    return Card(card_id, f"Card {card_id}", power, affinity, tags=[])


@pytest.fixture
def board_two_players() -> Board:
    return Board([0, 1])


class TestBoard:

    def test_rows_for_all_players_and_affinities(self, board_two_players):
        board = board_two_players

        assert board.player_ids == [0, 1]
        assert len(board.rows_by_player) == 2

        expected_affinities = {RowAffinity.MELEE,
                               RowAffinity.RANGED,
                               RowAffinity.SIEGE}

        for player_id in board.player_ids:
            player_rows = board.rows_by_player[player_id]
            assert set(player_rows.keys()) == expected_affinities

            for row in player_rows.values():
                assert isinstance(row, Row)
                assert row.is_empty()
                assert len(row) == 0

    def test_place_card_puts_card_only_in_target_row(self):
        board = Board([0])
        card = make_card(1, 10)

        board.place_card(0, card, row_affinity=RowAffinity.MELEE)

        melee_row = board.get_row(0, RowAffinity.MELEE)
        ranged_row = board.get_row(0, RowAffinity.RANGED)
        siege_row = board.get_row(0, RowAffinity.SIEGE)

        assert melee_row.cards == [card]
        assert len(ranged_row) == 0
        assert len(siege_row) == 0
        assert card not in ranged_row.cards
        assert card not in siege_row.cards

    def test_get_row_power_returns_correct_sum(self):
        board = Board([0])
        card1 = make_card(1, 4)
        card2 = make_card(2, 6)
        card3 = make_card(3, 1)

        board.place_card(0, card1, RowAffinity.MELEE)
        board.place_card(0, card2, RowAffinity.MELEE)
        board.place_card(0, card3, RowAffinity.MELEE)

        expected_power = card1.base_power + card2.base_power + card3.base_power

        assert board.get_row_power(0, RowAffinity.MELEE) == expected_power
        assert board.get_row_power(0, RowAffinity.RANGED) == 0
        assert board.get_row_power(0, RowAffinity.SIEGE) == 0

    def test_get_total_power_sums_all_rows_for_player(self, board_two_players):
        board = board_two_players

        card1 = make_card(1, 4)
        card2 = make_card(2, 6)
        card3 = make_card(3, 1, RowAffinity.RANGED)
        card4 = make_card(4, 5, RowAffinity.SIEGE)

        board.place_card(0, card1, RowAffinity.MELEE)
        board.place_card(0, card2, RowAffinity.MELEE)
        board.place_card(0, card3, RowAffinity.RANGED)
        board.place_card(0, card4, RowAffinity.SIEGE)

        expected_power = (
            card1.base_power +
            card2.base_power +
            card3.base_power +
            card4.base_power
        )

        assert board.get_row_power(0, RowAffinity.MELEE) == (card1.base_power +
                                                             card2.base_power)
        assert board.get_row_power(0, RowAffinity.RANGED) == card3.base_power
        assert board.get_row_power(0, RowAffinity.SIEGE) == card4.base_power
        assert board.get_total_power(0) == expected_power
        assert board.get_total_power(1) == 0

    def test_clear_resets_all_rows_and_total_power(self, board_two_players):
        board = board_two_players

        card1 = make_card(1, 4)
        card2 = make_card(2, 6)
        card3 = make_card(3, 1, RowAffinity.RANGED)
        card4 = make_card(4, 5, RowAffinity.SIEGE)

        board.place_card(0, card1, RowAffinity.MELEE)
        board.place_card(0, card2, RowAffinity.MELEE)
        board.place_card(0, card3, RowAffinity.RANGED)
        board.place_card(0, card4, RowAffinity.SIEGE)

        board.clear()

        for player_id in board.player_ids:
            for affinity in (RowAffinity.MELEE,
                             RowAffinity.RANGED,
                             RowAffinity.SIEGE):

                assert board.get_row_power(player_id, affinity) == 0

        assert board.get_total_power(0) == 0
        assert board.get_total_power(1) == 0

        for player_id in board.player_ids:
            for row in board.rows_by_player[player_id].values():
                assert row.is_empty()
                assert len(row) == 0
