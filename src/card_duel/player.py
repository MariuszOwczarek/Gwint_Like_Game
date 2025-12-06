from src.card_duel.deck import Deck
from src.card_duel.card import Card, RowAffinity
from src.card_duel.board import Board


class Player:
    def __init__(self, id: int, deck: Deck):
        self.id = id
        self.deck = deck
        self.hand: list[Card] = []
        self.rounds_won: int = 0
        self.has_passed: bool = False

    def draw_from_deck(self, n: int = 1) -> list[Card]:
        draw_cards = self.deck.draw_many(n)
        for card in draw_cards:
            self.hand.append(card)
        return draw_cards

    def draw_starting_hand(self, hand_size: int) -> list[Card]:
        return self.draw_from_deck(hand_size)

    def play_card(self,
                  card: Card,
                  board: Board,
                  row_affinity: RowAffinity) -> None:

        if card not in self.hand:
            raise ValueError("Card not in hand")
        self.hand.remove(card)
        board.place_card(self.id, card, row_affinity)

    def hand_size(self) -> int:
        return len(self.hand)

    def pass_round(self) -> None:
        self.has_passed = True

    def reset_for_new_round(self) -> None:
        self.has_passed = False

    def increment_rounds_won(self) -> None:
        self.rounds_won += 1

    def serialize(self) -> dict:
        player_dict = {
                    "id": self.id,
                    "deck": self.deck.name,
                    "hand": [card.serialize() for card in self.hand],
                    "rounds_won": self.rounds_won,
                    "has_passed": self.has_passed
                    }
        return player_dict
