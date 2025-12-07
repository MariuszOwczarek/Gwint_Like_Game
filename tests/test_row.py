import pytest
from src.card_duel.row import Row
from src.card_duel.card import RowAffinity, Card


@pytest.fixture
def melee_row() -> Row:
    """Pusty rząd melee na start każdego testu."""
    return Row(RowAffinity.MELEE)


def make_card(card_id: int, power: int = 10) -> Card:
    """Prosta karta melee o zadanym id i sile."""
    return Card(card_id, "Warrior", power, RowAffinity.MELEE, tags=[])


class TestRow:

    def test_row_init_starts_empty(self, melee_row):
        row = melee_row

        assert row.name is RowAffinity.MELEE
        assert len(row) == 0
        assert row.is_empty() is True

    def test_row_add_card_increases_len_and_power(self, melee_row):
        row = melee_row
        card = make_card(1, power=10)

        row.add_card(card)

        assert len(row) == 1
        assert row.total_power() == card.base_power
        assert card in row.cards

    def test_row_add_multiple_cards_accumulates_power(self, melee_row):
        row = melee_row
        card1 = make_card(1, power=10)
        card2 = make_card(2, power=7)
        card3 = make_card(3, power=5)

        row.add_card(card1)
        row.add_card(card2)
        row.add_card(card3)

        assert row.total_power() == (card1.base_power +
                                     card2.base_power +
                                     card3.base_power)

    def test_row_clear_resets_cards_and_power(self, melee_row):
        row = melee_row
        card1 = make_card(1, power=10)
        card2 = make_card(2, power=7)
        card3 = make_card(3, power=5)

        row.add_card(card1)
        row.add_card(card2)
        row.add_card(card3)

        row.clear()

        assert len(row) == 0
        assert row.is_empty() is True
        assert row.total_power() == 0

    def test_row_remove_card_removes_only_that_card(self, melee_row):
        row = melee_row
        card1 = make_card(1, power=10)
        card2 = make_card(2, power=7)
        card3 = make_card(3, power=5)

        row.add_card(card1)
        row.add_card(card2)
        row.add_card(card3)

        length_before = len(row)
        power_before = row.total_power()

        row.remove_card(card2)

        assert card2 not in row.cards
        assert card1 in row.cards
        assert card3 in row.cards
        assert len(row) == length_before - 1
        assert row.total_power() == power_before - card2.base_power

    def test_row_remove_card_not_present_behavior(self, melee_row):
        row = melee_row
        card = make_card(99, power=10)

        deleted_card = row.remove_card(card)

        assert deleted_card is None
        assert len(row) == 0
        assert row.total_power() == 0
