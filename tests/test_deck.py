from src.card_duel.card import Card, RowAffinity
from src.card_duel.deck import Deck
import pytest


# Helper do tworzenia kart zeyb nie powtarzac kodu
def make_cards(count: int) -> list[Card]:
    """Pomocniczo tworzy listę prostych kart MELEE o unikalnych id."""
    cards: list[Card] = []
    for i in range(1, count + 1):
        cards.append(
            Card(
                i,
                f"Card {i}",
                10 + i,    # dowolna, rosnąca siła – nie jest istotna dla Deck
                RowAffinity.MELEE,  # rodzaj rzędu nie ma znaczenia dla Deck
                tags=None,
            )
        )
    return cards


class TestDeck:

    def test_deck_init_and_len(self):
        cards = make_cards(3)
        deck = Deck("Dziki Gon", cards)

        assert deck.name == "Dziki Gon"
        assert len(deck) == 3
        assert deck.is_empty() is False

    def test_deck_is_empty_for_empty_deck(self):
        deck = Deck("Zima Piekieł", cards=[])

        assert len(deck) == 0
        assert deck.is_empty() is True

    def test_deck_shuffle_preserves_cards_and_size(self):
        cards = make_cards(4)
        deck = Deck("Diabelskie Nasienie", cards)

        original_cards_set = set(deck.cards)
        deck.shuffle()

        assert len(deck) == 4
        # Po shuffle dokładnie ten sam zestaw kart, tylko w innej kolejności
        assert set(deck.cards) == original_cards_set

    def test_deck_draw_one_returns_card_and_reduces_size(self):
        cards = make_cards(3)
        deck = Deck("Diabelskie Nasienie", cards)

        original_len = len(deck)
        drawn_card = deck.draw_one()

        assert len(deck) == original_len - 1
        assert isinstance(drawn_card, Card)
        # w talii nie powinno już być tej karty
        assert drawn_card not in deck.cards

    def test_deck_draw_one_from_empty_returns_none(self):
        deck = Deck("Diabelskie Nasienie", [])

        drawn_card = deck.draw_one()

        assert drawn_card is None
        assert len(deck) == 0
        assert deck.is_empty() is True

    def test_deck_draw_many_basic(self):
        cards = make_cards(5)
        deck = Deck("Diabelskie Nasienie", cards)

        drawn_cards = deck.draw_many(3)

        assert len(drawn_cards) == 3
        assert len(deck) == 2
        for card in drawn_cards:
            assert card not in deck.cards

    def test_deck_draw_many_more_than_available(self):
        cards = make_cards(2)
        deck = Deck("Diabelskie Nasienie", cards)

        drawn_cards = deck.draw_many(5)

        assert len(drawn_cards) == 2
        assert len(deck) == 0
        assert deck.is_empty() is True

    def test_deck_peek_does_not_modify_deck(self):
        cards = make_cards(5)
        deck = Deck("Diabelskie Nasienie", cards)

        original_cards = list(deck.cards)
        original_len = len(deck)

        peeked = deck.peek(2)

        assert len(peeked) == 2
        assert len(deck) == original_len
        # kolejność kart w talii nie powinna się zmienić
        assert deck.cards == original_cards

    def test_deck_peek_more_than_available(self):
        cards = make_cards(2)
        deck = Deck("Diabelskie Nasienie", cards)

        peeked = deck.peek(10)

        assert len(peeked) == len(cards)
        assert len(deck) == len(cards)
        assert peeked == deck.cards

    def test_deck_draw_many_negative_raises_value_error(self):
        cards = make_cards(2)
        deck = Deck("Diabelskie Nasienie", cards)

        with pytest.raises(ValueError):
            deck.draw_many(-5)

    def test_deck_peek_negative_raises_value_error(self):
        cards = make_cards(2)
        deck = Deck("Diabelskie Nasienie", cards)

        with pytest.raises(ValueError):
            deck.peek(-3)
