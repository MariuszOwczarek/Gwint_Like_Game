from src.card_duel.row import Row
from src.card_duel.card import RowAffinity, Card


class TestRow:

    def test_row_init_starts_empty(self):
        row = Row(RowAffinity.MELEE)

        assert row.name == RowAffinity.MELEE
        assert len(row) == 0
        assert row.is_empty() is True

    def test_row_add_card_increases_len_and_power(self):
        row = Row(RowAffinity.MELEE)
        card1 = Card(1, "Warrior", 10, RowAffinity.MELEE, tags=[])
        row.add_card(card=card1)

        assert len(row) == 1
        assert row.total_power() == card1.base_power
        assert card1 in row.cards

    def test_row_add_multiple_cards_accumulates_power(self):
        row = Row(RowAffinity.MELEE)
        card1 = Card(1, "Warrior", 10, RowAffinity.MELEE, tags=[])
        card2 = Card(2, "Warrior", 10, RowAffinity.MELEE, tags=[])
        card3 = Card(3, "Warrior", 10, RowAffinity.MELEE, tags=[])
        row.add_card(card=card1)
        row.add_card(card=card2)
        row.add_card(card=card3)

        assert row.total_power() == (card1.base_power +
                                     card2.base_power +
                                     card3.base_power)

    def test_row_clear_resets_cards_and_power(self):
        row = Row(RowAffinity.MELEE)
        card1 = Card(1, "Warrior", 10, RowAffinity.MELEE, tags=[])
        card2 = Card(2, "Warrior", 10, RowAffinity.MELEE, tags=[])
        card3 = Card(3, "Warrior", 10, RowAffinity.MELEE, tags=[])
        row.add_card(card=card1)
        row.add_card(card=card2)
        row.add_card(card=card3)
        row.clear()

        assert len(row) == 0
        assert row.is_empty() is True
        assert row.total_power() == 0

    def test_row_remove_card_removes_only_that_card(self):
        row = Row(RowAffinity.MELEE)
        card1 = Card(1, "Warrior", 10, RowAffinity.MELEE, tags=[])
        card2 = Card(2, "Warrior", 10, RowAffinity.MELEE, tags=[])
        card3 = Card(3, "Warrior", 10, RowAffinity.MELEE, tags=[])
        row.add_card(card=card1)
        row.add_card(card=card2)
        row.add_card(card=card3)
        row_length_before_remove = len(row)
        row_total_power_before_remove = row.total_power()
        row.remove_card(card2)

        assert card2 not in [card for card in row.cards]
        assert card1 in [card for card in row.cards]
        assert card3 in [card for card in row.cards]
        assert len(row) == row_length_before_remove - 1
        assert row.total_power() == (row_total_power_before_remove
                                     - card2.base_power)

    def test_row_remove_card_not_present_behavior(self):
        row = Row(RowAffinity.MELEE)
        card3 = Card(2, "Warrior", 10, RowAffinity.MELEE, tags=[])
        deleted_card = row.remove_card(card3)
        assert deleted_card is None
