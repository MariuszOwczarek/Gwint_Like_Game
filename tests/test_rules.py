from src.card_duel.player import Player
from src.card_duel.deck import Deck
from src.card_duel.board import Board
from src.card_duel.card import Card, RowAffinity
from src.card_duel.rules import Rules


def make_player(player_id: int,
                has_passed: bool = False,
                rounds_won: int = 0) -> Player:

    """Pomocniczy gracz z minimalną talią."""
    deck = Deck("Test deck", cards=[])
    player = Player(player_id, deck=deck)
    player.has_passed = has_passed
    player.rounds_won = rounds_won
    return player


def make_card(card_id: int, power: int) -> Card:
    """Prosta karta melee o zadanej sile."""
    return Card(card_id, "Test Warrior", power, RowAffinity.MELEE, tags=[])


class TestRules:

    # --- is_round_over ---

    def test_is_round_over_returns_true_when_all_players_passed(self):
        rules = Rules()
        player1 = make_player(0, has_passed=True)
        player2 = make_player(1, has_passed=True)

        result = rules.is_round_over([player1, player2])

        assert result is True

    def test_is_round_over_returns_false_when_at_least_one_not_passed(self):
        rules = Rules()
        player1 = make_player(0, has_passed=True)
        player2 = make_player(1, has_passed=False)

        result = rules.is_round_over([player1, player2])

        assert result is False

    # --- get_round_winner_id ---

    def test_get_round_winner_id_returns_player_with_higher_total_power(self):
        rules = Rules()
        player1 = make_player(0)
        player2 = make_player(1)
        board = Board(player_ids=[player1.id, player2.id])

        stronger_card = make_card(1, power=12)
        weaker_card = make_card(2, power=8)

        # p1: 12, p2: 8
        board.place_card(player1.id,
                         stronger_card,
                         row_affinity=RowAffinity.MELEE)

        board.place_card(player2.id,
                         weaker_card,
                         row_affinity=RowAffinity.MELEE)

        result = rules.get_round_winner_id(board, [player1, player2])

        assert result == player1.id

    def test_get_round_winner_id_returns_none_on_tie(self):
        rules = Rules()
        player1 = make_player(0)
        player2 = make_player(1)
        board = Board(player_ids=[player1.id, player2.id])

        card = make_card(1, power=10)

        # p1: 10, p2: 10 -> remis
        board.place_card(player1.id, card, row_affinity=RowAffinity.MELEE)
        board.place_card(player2.id, card, row_affinity=RowAffinity.MELEE)

        assert rules.get_round_winner_id(board, [player1, player2]) is None

    # --- is_match_over ---

    def test_match_over_returns_false_when_no_one_reached_rounds_to_win(self):
        rules = Rules(rounds_to_win=2)
        player1 = make_player(0, rounds_won=1)
        player2 = make_player(1, rounds_won=1)

        result = rules.is_match_over([player1, player2])

        assert result is False

    def test_is_match_over_true_when_any_player_reached_rounds_to_win(self):
        rules = Rules(rounds_to_win=2)
        player1 = make_player(0, rounds_won=2)
        player2 = make_player(1, rounds_won=0)

        result = rules.is_match_over([player1, player2])

        assert result is True

    # --- get_match_winner_id ---

    def test_match_winner_id_returns_player_with_enough_rounds_won(self):
        rules = Rules(rounds_to_win=2)
        player1 = make_player(0, rounds_won=2)
        player2 = make_player(1, rounds_won=1)

        winner_id = rules.get_match_winner_id([player1, player2])

        assert winner_id == player1.id

    def test_match_winner_id_returns_none_when_no_one_has_rounds_to_win(self):
        rules = Rules(rounds_to_win=2)
        player1 = make_player(0, rounds_won=1)
        player2 = make_player(1, rounds_won=1)

        winner_id = rules.get_match_winner_id([player1, player2])

        assert winner_id is None

    def test_returns_none_when_few_players_got_rounds_to_win(self):
        rules = Rules(rounds_to_win=2)
        player1 = make_player(0, rounds_won=2)
        player2 = make_player(1, rounds_won=2)

        winner_id = rules.get_match_winner_id([player1, player2])

        assert winner_id is None
