from src.card_duel.card import RowAffinity, Card
from typing import List, Optional


class Row:
    def __init__(self, name: RowAffinity, cards: Optional[List[Card]] = None):
        self.name: RowAffinity = name
        self.cards: List[Card] = list(cards) if cards is not None else []

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def remove_card(self, card: Card) -> None:
        if card in self.cards:
            self.cards.remove(card)

    def clear(self) -> None:
        self.cards.clear()

    def total_power(self) -> int:
        row_total_sum = 0
        for card in self.cards:
            row_total_sum += card.base_power
        return row_total_sum

    def __len__(self) -> int:
        return len(self.cards)

    def is_empty(self) -> bool:
        return not self.cards

    def serialize(self) -> dict:
        row_dict = {
                    "name": self.name.name,
                    "cards": [card.serialize() for card in self.cards]
                   }
        return row_dict
