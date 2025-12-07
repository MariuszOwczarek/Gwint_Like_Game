import pytest

from src.card_duel.card import Card, RowAffinity
from src.card_duel.deck import Deck
from src.card_duel.player import Player
from src.card_duel.board import Board
from src.card_duel.rules import Rules
from src.card_duel.game import Game


# --- HELPERY -----------------------------------------------------------------
def make_card(
    card_id: int,
    power: int = 5,
    affinity: RowAffinity = RowAffinity.MELEE,
) -> Card:
    return Card(
        id=card_id,
        name=f"Card {card_id}",
        base_power=power,
        row_affinity=affinity,
        tags=set(),
    )


def make_deck_with_n_cards(n: int) -> Deck:
    cards = [make_card(i) for i in range(1, n + 1)]
    return Deck(name="Test Deck", cards=cards)


def make_player(player_id: int, n_cards: int = 5) -> Player:
    deck = make_deck_with_n_cards(n_cards)
    player = Player(id=player_id, deck=deck)
    # dobierzmy od razu kilka kart, żeby można było grać
    player.draw_from_deck(3)
    return player


@pytest.fixture
def game_two_players() -> Game:
    player1 = make_player(1, n_cards=5)
    player2 = make_player(2, n_cards=5)

    board = Board(player_ids=[player1.id, player2.id])
    rules = Rules(rounds_to_win=2)

    game = Game(players=[player1, player2], board=board, rules=rules)
    return game


# --- TESTY INICJALIZACJI -----------------------------------------------------
def test_game_init_requires_at_least_one_player(board=None, rules=None) -> None:
    board = Board(player_ids=[]) if board is None else board
    rules = Rules(rounds_to_win=2) if rules is None else rules

    with pytest.raises(ValueError):
        Game(players=[], board=board, rules=rules)


def test_game_init_requires_exactly_two_players() -> None:
    board = Board(player_ids=[1])
    rules = Rules(rounds_to_win=2)

    p1 = make_player(1)

    with pytest.raises(ValueError):
        Game(players=[p1], board=board, rules=rules)


def test_game_initial_state(game_two_players: Game) -> None:
    game = game_two_players

    assert game.current_round == 0
    assert game.is_round_active is False
    assert game.active_player_id is None
    assert game.starting_player_id in game.players
    assert set(game.player_order) == set(game.players.keys())


# --- GET_OPPONENT_ID ---------------------------------------------------------


def test_get_opponent_id_returns_other_player(game_two_players: Game) -> None:
    game = game_two_players

    p1, p2 = game.player_order
    assert game.get_opponent_id(p1) == p2
    assert game.get_opponent_id(p2) == p1


def test_get_opponent_id_raises_for_unknown_player(game_two_players: Game) -> None:
    game = game_two_players

    with pytest.raises(ValueError):
        game.get_opponent_id(999)


# --- START_ROUND -------------------------------------------------------------


def test_start_round_initializes_round_state(game_two_players: Game) -> None:
    game = game_two_players

    assert game.current_round == 0
    assert game.is_round_active is False
    assert game.get_active_player_id() is None

    game.start_round()

    assert game.current_round == 1
    assert game.is_round_active is True
    active_id = game.get_active_player_id()
    assert active_id in game.players

    # plansza powinna być pusta po start_round
    board_affinities = (RowAffinity.MELEE, RowAffinity.RANGED, RowAffinity.SIEGE)
    for pid in game.players.keys():
        for affinity in board_affinities:
            row = game.board.get_row(pid, affinity)
            assert len(row) == 0

    # stan rundy graczy zresetowany
    for player in game.players.values():
        assert player.has_passed is False


def test_start_round_alternates_starting_player_from_second_round(game_two_players: Game) -> None:
    game = game_two_players

    game.start_round()
    first_round_starter = game.starting_player_id

    # symulacja końca rundy
    game.end_round()

    game.start_round()
    second_round_starter = game.starting_player_id

    assert game.current_round == 2
    assert second_round_starter != first_round_starter
    assert game.get_active_player_id() == game.starting_player_id


# --- PLAY_CARD / PASS_TURN – PRZEPŁYW TURY -----------------------------------


def test_play_card_places_card_on_board_and_switches_active_player(game_two_players: Game) -> None:
    game = game_two_players
    game.start_round()

    active_id = game.get_active_player_id()
    opponent_id = game.get_opponent_id(active_id)

    active_player = game.players[active_id]
    assert active_player.hand_size() > 0

    # zapamiętujemy kartę z ręki
    card_in_hand = active_player.hand[0]

    game.play_card(active_id, card_index=0, row_affinity=RowAffinity.MELEE)

    # karta powinna zniknąć z ręki
    assert card_in_hand not in active_player.hand

    # karta powinna znaleźć się na planszy
    melee_row = game.board.get_row(active_id, RowAffinity.MELEE)
    assert card_in_hand in melee_row.cards

    # tura powinna przejść do przeciwnika
    assert game.get_active_player_id() == opponent_id


def test_inactive_player_cannot_play_card(game_two_players: Game) -> None:
    game = game_two_players
    game.start_round()

    active_id = game.get_active_player_id()
    inactive_id = game.get_opponent_id(active_id)

    with pytest.raises(ValueError):
        game.play_card(inactive_id, card_index=0, row_affinity=RowAffinity.MELEE)


def test_player_cannot_play_after_passing(game_two_players: Game) -> None:
    game = game_two_players
    game.start_round()

    player_id = game.get_active_player_id()
    player = game.players[player_id]

    # gracz pasuje (bez użycia Game, żeby nie przełączać tury)
    player.pass_round()
    assert player.has_passed is True

    with pytest.raises(ValueError):
        game.play_card(player_id, card_index=0, row_affinity=RowAffinity.MELEE)


def test_pass_turn_marks_player_passed_and_switches_active_player(game_two_players: Game, monkeypatch) -> None:
    game = game_two_players
    game.start_round()

    active_id = game.get_active_player_id()
    opponent_id = game.get_opponent_id(active_id)

    # chcemy, żeby runda się nie skończyła po pasowaniu
    monkeypatch.setattr(game.rules, "is_round_over", lambda players: False)

    game.pass_turn(active_id)

    assert game.players[active_id].has_passed is True
    assert game.get_active_player_id() == opponent_id
    assert game.is_round_active is True


def test_inactive_player_cannot_pass(game_two_players: Game) -> None:
    game = game_two_players
    game.start_round()

    active_id = game.get_active_player_id()
    inactive_id = game.get_opponent_id(active_id)

    with pytest.raises(ValueError):
        game.pass_turn(inactive_id)


def test_pass_turn_ends_round_when_rules_say_so(game_two_players: Game, monkeypatch) -> None:
    game = game_two_players
    game.start_round()

    active_id = game.get_active_player_id()

    # is_round_over zawsze True, get_round_winner_id zwraca aktywnego gracza
    monkeypatch.setattr(game.rules, "is_round_over", lambda players: True)
    monkeypatch.setattr(
        game.rules,
        "get_round_winner_id",
        lambda board, players: active_id,
    )

    game.pass_turn(active_id)

    assert game.is_round_active is False
    assert game.players[active_id].rounds_won == 1


# --- KONIEC RUNDY I MECZU ----------------------------------------------------


def test_end_round_increments_winner_rounds_won(game_two_players: Game, monkeypatch) -> None:
    game = game_two_players
    game.start_round()

    # wybieramy zwycięzcę "na sztywno"
    winner_id = game.player_order[0]

    monkeypatch.setattr(
        game.rules,
        "get_round_winner_id",
        lambda board, players: winner_id,
    )

    game.end_round()

    assert game.is_round_active is False
    assert game.players[winner_id].rounds_won == 1


def test_is_match_over_and_get_match_winner_id_use_rules(game_two_players: Game) -> None:
    game = game_two_players

    # symulujemy stan, w którym jeden gracz wygrał wymagane rundy
    winner_id = game.player_order[0]
    game.players[winner_id].rounds_won = game.rules.rounds_to_win

    assert game.is_match_over() is True
    assert game.get_match_winner_id() == winner_id
