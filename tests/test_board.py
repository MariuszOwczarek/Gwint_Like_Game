from src.card_duel.board import Board
from src.card_duel.card import RowAffinity, Card
from src.card_duel.row import Row


class TestBoard:
    def test_board_initializes_rows_for_all_players_and_affinities(self):
        board = Board([0, 1])
        ROW_LANES = (RowAffinity.MELEE, RowAffinity.RANGED, RowAffinity.SIEGE)
        assert board.player_ids == [0, 1]
        assert len(board.rows_by_player) == 2

        expected_affinities = {RowAffinity.MELEE,
                               RowAffinity.RANGED,
                               RowAffinity.SIEGE}

        for player_id in board.player_ids:
            player_rows = {affinity: Row(name=affinity) for
                           affinity in ROW_LANES}
            assert set(player_rows.keys()) == expected_affinities
            for row in player_rows.values():
                assert isinstance(row, Row)
                assert row.is_empty()
                assert len(row) == 0

    def test_place_card_puts_card_only_in_target_row(self):
        board = Board([0])
        card1 = Card(1, "Warrior", 10, RowAffinity.MELEE, tags=[])
        board.place_card(0, card1, row_affinity=RowAffinity.MELEE)

        melee_row = board.get_row(0, RowAffinity.MELEE)
        ranged_row = board.get_row(0, RowAffinity.RANGED)
        siege_row = board.get_row(0, RowAffinity.SIEGE)

        assert len(melee_row) == 1
        assert len(ranged_row) == 0
        assert len(siege_row) == 0
        assert card1 not in ranged_row.cards
        assert card1 not in siege_row.cards
        assert card1 in melee_row.cards
        assert melee_row.cards == [card1]

    def test_get_row_power_returns_correct_sum(self):
        board = Board([0])
        card1 = Card(1, 'Wojownik', 4, RowAffinity.MELEE, tags=[])
        card2 = Card(2, 'Mag', 6, RowAffinity.MELEE, tags=[])
        card3 = Card(3, 'Nekromanta', 1, RowAffinity.MELEE, tags=[])
        board.place_card(0, card1, row_affinity=RowAffinity.MELEE)
        board.place_card(0, card2, row_affinity=RowAffinity.MELEE)
        board.place_card(0, card3, row_affinity=RowAffinity.MELEE)
        expected_power = card1.base_power + card2.base_power + card3.base_power

        assert board.get_row_power(0, RowAffinity.MELEE) == expected_power
        assert board.get_row_power(0, RowAffinity.RANGED) == 0
        assert board.get_row_power(0, RowAffinity.SIEGE) == 0

        melee_row = board.get_row(0, RowAffinity.MELEE)
        assert len(melee_row) == 3
        for card in (card1, card2, card3):
            assert card in melee_row.cards

    def test_get_total_power_sums_all_rows_for_player(self):
        board = Board([0, 1])
        card1 = Card(1, 'Wojownik', 4, RowAffinity.MELEE, tags=[])
        card2 = Card(2, 'Mag', 6, RowAffinity.MELEE, tags=[])
        card3 = Card(3, 'Nekromanta', 1, RowAffinity.RANGED, tags=[])
        card4 = Card(4, 'Nekromanta', 5, RowAffinity.SIEGE, tags=[])
        board.place_card(0, card1, row_affinity=RowAffinity.MELEE)
        board.place_card(0, card2, row_affinity=RowAffinity.MELEE)
        board.place_card(0, card3, row_affinity=RowAffinity.RANGED)
        board.place_card(0, card4, row_affinity=RowAffinity.SIEGE)

        expected_power = (card1.base_power +
                          card2.base_power +
                          card3.base_power +
                          card4.base_power)

        assert board.get_row_power(0, RowAffinity.MELEE) == (card1.base_power +
                                                             card2.base_power)
        assert board.get_row_power(0, RowAffinity.RANGED) == card3.base_power
        assert board.get_row_power(0, RowAffinity.SIEGE) == card4.base_power
        assert board.get_total_power(0) == expected_power
        assert board.get_total_power(1) == 0

    def test_clear_resets_all_rows_and_total_power(self):
        board = Board([0, 1])
        card1 = Card(1, 'Wojownik', 4, RowAffinity.MELEE, tags=[])
        card2 = Card(2, 'Mag', 6, RowAffinity.MELEE, tags=[])
        card3 = Card(3, 'Nekromanta', 1, RowAffinity.RANGED, tags=[])
        card4 = Card(4, 'Nekromanta', 5, RowAffinity.SIEGE, tags=[])
        board.place_card(0, card1, row_affinity=RowAffinity.MELEE)
        board.place_card(0, card2, row_affinity=RowAffinity.MELEE)
        board.place_card(0, card3, row_affinity=RowAffinity.RANGED)
        board.place_card(0, card4, row_affinity=RowAffinity.SIEGE)

        expected_power = (card1.base_power +
                          card2.base_power +
                          card3.base_power +
                          card4.base_power)

        assert board.get_row_power(0, RowAffinity.MELEE) == (card1.base_power +
                                                             card2.base_power)
        assert board.get_row_power(0, RowAffinity.RANGED) == card3.base_power
        assert board.get_row_power(0, RowAffinity.SIEGE) == card4.base_power
        assert board.get_total_power(0) == expected_power
        assert board.get_total_power(1) == 0
        board.clear()
        assert board.get_row_power(0, RowAffinity.MELEE) == 0
        assert board.get_row_power(0, RowAffinity.RANGED) == 0
        assert board.get_row_power(0, RowAffinity.SIEGE) == 0
        assert board.get_total_power(0) == 0
        assert board.get_total_power(1) == 0

        for player_id in board.player_ids:
            for row in board.rows_by_player[player_id].values():
                assert row.is_empty()
                assert len(row) == 0

        for player_id in board.player_ids:
            for affinity in (RowAffinity.MELEE,
                             RowAffinity.RANGED,
                             RowAffinity.SIEGE):
                assert board.get_row_power(player_id, affinity) == 0
