import pytest
from src.card_duel.player import Player
from src.card_duel.card import Card, RowAffinity
from src.card_duel.deck import Deck
from src.card_duel.board import Board


def make_card(card_id: int,
              power: int = 10,
              affinity: RowAffinity = RowAffinity.MELEE) -> Card:
    """Prosta karta, domyślnie MELEE, z możliwością zmiany affinity."""
    return Card(card_id, f"Card {card_id}", power, affinity, tags=[])


def make_deck_with_n_cards(n: int) -> Deck:
    """Tworzy talię z n prostymi kartami MELEE o rosnącej sile."""
    cards = [make_card(i, power=10 + i) for i in range(1, n + 1)]
    return Deck("Test Deck", cards)


class TestPlayer:
    def test_player_initialization(self):
        deck = make_deck_with_n_cards(3)
        player = Player(0, deck)

        assert player.id == 0
        assert player.deck is deck
        assert player.hand == []
        assert player.hand_size() == 0
        assert player.rounds_won == 0
        assert player.has_passed is False

    def test_draw_from_deck_adds_cards_to_hand_and_reduces_deck(self):
        deck = make_deck_with_n_cards(5)
        player = Player(0, deck)

        drawn = player.draw_from_deck(3)

        assert len(drawn) == 3
        assert len(player.hand) == 3
        assert drawn == player.hand
        assert len(player.deck) == 2

    def test_draw_from_deck_when_not_enough_cards_in_deck(self):
        deck = make_deck_with_n_cards(2)
        player = Player(0, deck)

        drawn = player.draw_from_deck(5)

        assert len(drawn) == 2
        assert len(player.hand) == 2
        assert len(player.deck) == 0
        assert set(player.hand) == set(drawn)

    def test_draw_from_deck_raises_on_negative_n(self):
        deck = make_deck_with_n_cards(2)
        player = Player(0, deck)

        with pytest.raises(ValueError):
            player.draw_from_deck(-1)

        assert player.hand == []
        assert len(player.deck) == 2

    def test_draw_starting_hand_draws_given_number_of_cards(self):
        deck = make_deck_with_n_cards(2)
        player = Player(0, deck)

        starting_hand = player.draw_starting_hand(2)

        assert len(starting_hand) == 2
        assert len(player.hand) == 2
        for card in starting_hand:
            assert card in player.hand
        assert len(player.deck) == 0

    def test_play_card_moves_card_from_hand_to_board(self):
        deck = make_deck_with_n_cards(1)
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
        deck = make_deck_with_n_cards(1)
        player = Player(0, deck)
        board = Board([player.id])
        fake_card = make_card(999, power=1, affinity=RowAffinity.MELEE)

        assert player.hand == []

        with pytest.raises(ValueError):
            player.play_card(fake_card, board, RowAffinity.MELEE)

        assert player.hand == []
        melee_row = board.get_row(player.id, RowAffinity.MELEE)
        assert fake_card not in melee_row.cards

    def test_hand_size_returns_number_of_cards_in_hand(self):
        deck = make_deck_with_n_cards(3)
        player = Player(0, deck)
        board = Board([player.id])

        assert player.hand_size() == 0

        player.draw_from_deck(2)
        assert player.hand_size() == 2

        card_to_play = player.hand[0]
        player.play_card(card_to_play, board, RowAffinity.MELEE)

        assert player.hand_size() == 1

    def test_pass_round_sets_has_passed_true(self):
        deck = make_deck_with_n_cards(1)
        player = Player(0, deck)

        assert player.has_passed is False

        player.pass_round()
        assert player.has_passed is True

        # kolejne wywołanie nie powinno już nic zmieniać
        player.pass_round()
        assert player.has_passed is True

    def test_resets_has_passed_but_not_rounds_won_or_hand(self):
        deck = make_deck_with_n_cards(2)
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
        # tu talia nie ma specjalnego znaczenia, może być nawet pusta
        deck = Deck("Test Deck", [])
        player = Player(0, deck)

        assert player.rounds_won == 0

        player.increment_rounds_won()
        player.increment_rounds_won()

        assert player.rounds_won == 2

    def test_serialize_returns_correct_dict_structure(self):
        deck = make_deck_with_n_cards(2)
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
