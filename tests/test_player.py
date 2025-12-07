import pytest
from src.card_duel.player import Player
from src.card_duel.card import Card, RowAffinity
from src.card_duel.deck import Deck
from src.card_duel.board import Board


class TestPlayer:
    def test_player_initialization(self):
        card1 = Card(1, 'Wojownik', 10, RowAffinity.MELEE, tags=None)
        card2 = Card(2, 'Mag', 12, RowAffinity.RANGED, tags=None)
        card3 = Card(3, 'Nekromanta', 11, RowAffinity.MELEE, tags=None)
        deck = Deck('Dziki Gon', [card1, card2, card3])
        player = Player(0, deck)

        assert player.id == 0
        assert player.deck is deck
        assert player.hand == []
        assert len(player.hand) == 0
        assert player.hand_size() == 0
        assert player.rounds_won == 0
        assert player.has_passed is False

    def test_draw_from_deck_adds_cards_to_hand_and_reduces_deck(self):
        card1 = Card(1, 'Wojownik', 10, RowAffinity.MELEE, tags=None)
        card2 = Card(2, 'Mag', 12, RowAffinity.RANGED, tags=None)
        card3 = Card(3, 'Nekromanta', 11, RowAffinity.MELEE, tags=None)
        card4 = Card(4, 'Mag', 12, RowAffinity.RANGED, tags=None)
        card5 = Card(5, 'Nekromanta', 11, RowAffinity.MELEE, tags=None)
        deck = Deck('Dziki Gon', [card1, card2, card3, card4, card5])
        player = Player(0, deck)
        drawn = player.draw_from_deck(3)
        assert len(drawn) == 3
        assert len(player.hand) == 3
        assert drawn == player.hand
        assert len(player.deck) == 2

    def test_draw_from_deck_when_not_enough_cards_in_deck(self):
        card4 = Card(4, 'Mag', 12, RowAffinity.RANGED, tags=None)
        card5 = Card(5, 'Nekromanta', 11, RowAffinity.MELEE, tags=None)
        deck = Deck('Dziki Gon', [card4, card5])
        player = Player(0, deck)
        drawn = player.draw_from_deck(5)
        assert len(drawn) == 2
        assert len(player.hand) == 2
        assert len(player.deck) == 0
        assert set(player.hand) == set(drawn)

    def test_draw_from_deck_raises_on_negative_n(self):
        card4 = Card(4, 'Mag', 12, RowAffinity.RANGED, tags=None)
        card5 = Card(5, 'Nekromanta', 11, RowAffinity.MELEE, tags=None)
        deck = Deck('Dziki Gon', [card4, card5])
        player = Player(0, deck)

        with pytest.raises(ValueError):
            player.draw_from_deck(-1)
        assert player.hand == []
        assert len(player.deck) == 2

    def test_draw_starting_hand_draws_given_number_of_cards(self):
        card4 = Card(4, 'Mag', 12, RowAffinity.RANGED, tags=None)
        card5 = Card(5, 'Nekromanta', 11, RowAffinity.MELEE, tags=None)
        deck = Deck('Dziki Gon', [card4, card5])
        player = Player(0, deck)
        starting_hand = player.draw_starting_hand(2)
        assert len(starting_hand) == 2
        assert len(player.hand) == 2

        for card in starting_hand:
            assert card in player.hand

        assert len(player.deck) == 0

    def test_play_card_moves_card_from_hand_to_board(self):
        card1 = Card(1, 'Wojownik', 10, RowAffinity.MELEE, tags=None)
        deck = Deck('Dziki Gon', [card1])
        player = Player(0, deck)
        board = Board([player.id])
        player.draw_from_deck(1)
        assert player.hand_size() == 1
        card_in_hand = player.hand[0]
        player.play_card(card_in_hand, board, RowAffinity.MELEE)
        assert player.hand_size() == 0
        assert card_in_hand not in player.hand

        melee_row = board.get_row(player.id, RowAffinity.MELEE)
        ranged_row = board.get_row(player.id, RowAffinity.RANGED)
        siege_row = board.get_row(player.id, RowAffinity.SIEGE)

        assert card_in_hand in melee_row.cards
        assert len(melee_row) == 1
        assert len(ranged_row) == 0
        assert len(siege_row) == 0

    def test_play_card_raises_if_card_not_in_hand(self):
        card1 = Card(1, 'Wojownik', 10, RowAffinity.MELEE, tags=None)
        deck = Deck('Dziki Gon', [card1])
        player = Player(0, deck)
        board = Board([player.id])
        fake_card = Card(999, 'Podróbka', 1, RowAffinity.MELEE, tags=None)
        assert player.hand == []
        with pytest.raises(ValueError):
            player.play_card(fake_card, board, RowAffinity.MELEE)

        assert player.hand == []
        melee_row = board.get_row(player.id, RowAffinity.MELEE)
        assert fake_card not in melee_row.cards

    def test_hand_size_returns_number_of_cards_in_hand(self):
        card1 = Card(1, 'Wojownik', 10, RowAffinity.MELEE, tags=None)
        card2 = Card(2, 'Mag', 12, RowAffinity.RANGED, tags=None)
        card3 = Card(3, 'Nekromanta', 11, RowAffinity.MELEE, tags=None)
        deck = Deck('Dziki Gon', [card1, card2, card3])
        player = Player(0, deck)
        board = Board([player.id])
        assert player.hand_size() == 0
        player.draw_from_deck(2)
        assert player.hand_size() == 2
        card_to_play = player.hand[0]
        player.play_card(card_to_play, board, RowAffinity.MELEE)
        assert player.hand_size() == 1

    def test_pass_round_sets_has_passed_true(self):
        card1 = Card(1, 'Wojownik', 10, RowAffinity.MELEE, tags=None)
        deck = Deck('Dziki Gon', [card1])
        player = Player(0, deck)
        assert player.has_passed is False
        player.pass_round()
        assert player.has_passed is True
        player.pass_round()
        assert player.has_passed is True

    def test_reset_for_new_round_has_passed_but_not_rounds_won_or_hand(self):
        card1 = Card(1, 'Wojownik', 10, RowAffinity.MELEE, tags=None)
        card2 = Card(2, 'Mag', 12, RowAffinity.RANGED, tags=None)
        deck = Deck('Dziki Gon', [card1, card2])
        player = Player(0, deck)
        player.draw_from_deck(2)
        assert player.hand_size() == 2
        player.pass_round()
        player.increment_rounds_won()
        player.increment_rounds_won()

        assert player.has_passed is True
        assert player.rounds_won == 2

        player.reset_for_new_round()
        assert player.has_passed is False
        assert player.rounds_won == 2
        assert player.hand_size() == 2

    def test_increment_rounds_won_increases_counter(self):
        card1 = Card(1, 'Wojownik', 10, RowAffinity.MELEE, tags=None)
        deck = Deck('Dziki Gon', [card1])
        player = Player(0, deck)
        assert player.rounds_won == 0
        player.increment_rounds_won()
        player.increment_rounds_won()
        assert player.rounds_won == 2

    def test_serialize_returns_correct_dict_structure(self):
        card1 = Card(1, 'Wojownik', 10, RowAffinity.MELEE, tags=None)
        card2 = Card(2, 'Mag', 12, RowAffinity.RANGED, tags=None)
        deck = Deck('Dziki Gon', [card1, card2])
        player = Player(0, deck)
        player.draw_from_deck(1)
        player.increment_rounds_won()
        player.pass_round()
        data = player.serialize()

        assert isinstance(data, dict)
        assert data["id"] == player.id
        assert data["deck"] == player.deck.name
        assert data["rounds_won"] == player.rounds_won
        assert data["has_passed"] == player.has_passed
        expected_hand = [card.serialize() for card in player.hand]
        assert data["hand"] == expected_hand
