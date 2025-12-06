from src.card_duel.card import Card, RowAffinity
from src.card_duel.deck import Deck
import pytest


class TestDeck:

    def test_deck_init_and_len(self):
        card1 = Card(1, 'Wojownik', 10, RowAffinity.MELEE, tags=None)
        card2 = Card(2, 'Mag', 12, RowAffinity.RANGED, tags=None)
        card3 = Card(3, 'Nekromanta', 11, RowAffinity.MELEE, tags=None)
        deck = Deck('Dziki Gon', [card1, card2, card3])

        assert deck.name == 'Dziki Gon'
        assert len(deck) == 3
        assert deck.is_empty() is False

    def test_deck_is_empty_for_empty_deck(self):
        deck = Deck('Zima Piekieł', cards=[])

        assert len(deck) == 0
        assert deck.is_empty() is True

    def test_deck_shuffle_preserves_cards_and_size(self):
        card1 = Card(1, 'Wojownik', 10, RowAffinity.MELEE, tags=None)
        card2 = Card(2, 'Mag', 12, RowAffinity.RANGED, tags=None)
        card3 = Card(3, 'Nekromanta', 11, RowAffinity.MELEE, tags=None)
        card4 = Card(4, 'Amazonka', 13, RowAffinity.SIEGE, tags=None)
        list_cards = [card1, card2, card3, card4]
        deck = Deck('Diabelskie Nasienie', list_cards)
        deck.shuffle()

        assert len(deck) == 4
        assert set(list_cards) == set(deck.cards)

    def test_deck_draw_one_returns_card_and_reduces_size(self):
        card1 = Card(1, 'Wojownik', 10, RowAffinity.MELEE, tags=None)
        card2 = Card(2, 'Mag', 12, RowAffinity.RANGED, tags=None)
        card3 = Card(3, 'Nekromanta', 11, RowAffinity.MELEE, tags=None)
        list_cards = [card1, card2, card3]
        deck = Deck('Diabelskie Nasienie', list_cards)
        len_deck = len(deck)
        draw_card = deck.draw_one()
        assert len_deck - 1 == len(deck)
        assert isinstance(draw_card, Card)
        for card in deck.cards:
            assert card is not draw_card

    def test_deck_draw_one_from_empty_returns_none(self):
        deck = Deck('Diabelskie Nasienie', [])
        draw_card = deck.draw_one()
        assert draw_card is None
        assert len(deck) == 0
        assert deck.is_empty() is True

    def test_deck_draw_many_basic(self):
        card1 = Card(1, 'Wojownik', 10, RowAffinity.MELEE, tags=None)
        card2 = Card(2, 'Mag', 12, RowAffinity.RANGED, tags=None)
        card3 = Card(3, 'Nekromanta', 11, RowAffinity.MELEE, tags=None)
        card4 = Card(4, 'Amazonka', 13, RowAffinity.SIEGE, tags=None)
        card5 = Card(5, 'Palladyn', 16, RowAffinity.MELEE, tags=None)
        list_cards = [card1, card2, card3, card4, card5]
        deck = Deck('Diabelskie Nasienie', list_cards)
        cards_draw = deck.draw_many(3)

        assert len(cards_draw) == 3
        assert len(deck) == 2

        for card in cards_draw:
            assert card not in deck.cards

    def test_deck_draw_many_more_than_available(self):
        card1 = Card(1, 'Wojownik', 10, RowAffinity.MELEE, tags=None)
        card4 = Card(4, 'Amazonka', 13, RowAffinity.SIEGE, tags=None)
        list_cards = [card1, card4]
        deck = Deck('Diabelskie Nasienie', list_cards)
        cards_draw = deck.draw_many(5)

        assert len(cards_draw) == len(list_cards)
        assert len(deck) == 0
        assert deck.is_empty() is True

    def test_deck_peek_does_not_modify_deck(self):
        card1 = Card(1, 'Wojownik', 10, RowAffinity.MELEE, tags=None)
        card2 = Card(2, 'Mag', 12, RowAffinity.RANGED, tags=None)
        card3 = Card(3, 'Nekromanta', 11, RowAffinity.MELEE, tags=None)
        card4 = Card(4, 'Amazonka', 13, RowAffinity.SIEGE, tags=None)
        card5 = Card(5, 'Palladyn', 16, RowAffinity.MELEE, tags=None)
        list_cards = [card1, card2, card3, card4, card5]
        deck = Deck('Diabelskie Nasienie', list_cards)
        deck_length = len(deck)
        deck.peek(2)
        assert len(deck) == deck_length
        assert len(deck) == len(list_cards)
        for i in range(len(list_cards)):
            assert list_cards[i].id == deck.cards[i].id

    def test_deck_peek_more_than_available(self):
        card1 = Card(1, 'Wojownik', 10, RowAffinity.MELEE, tags=None)
        card2 = Card(2, 'Mag', 12, RowAffinity.RANGED, tags=None)
        list_cards = [card1, card2]
        deck = Deck('Diabelskie Nasienie', list_cards)
        peek_list = deck.peek(10)

        assert len(peek_list) == 2
        assert len(deck) == len(list_cards)
        assert peek_list == deck.cards

    def test_deck_draw_many_negative_raises_value_error(self):
        card1 = Card(1, 'Wojownik', 10, RowAffinity.MELEE, tags=None)
        card4 = Card(4, 'Amazonka', 13, RowAffinity.SIEGE, tags=None)
        list_cards = [card1, card4]
        deck = Deck('Diabelskie Nasienie', list_cards)

        with pytest.raises(ValueError):
            deck.draw_many(-5)

    def test_deck_peek_negative_raises_value_error(self):
        card1 = Card(1, 'Wojownik', 10, RowAffinity.MELEE, tags=None)
        card4 = Card(4, 'Amazonka', 13, RowAffinity.SIEGE, tags=None)
        list_cards = [card1, card4]
        deck = Deck('Diabelskie Nasienie', list_cards)

        with pytest.raises(ValueError):
            deck.peek(-3)
