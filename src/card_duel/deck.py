import random
from .card import Card
from typing import Optional, List, Dict


class Deck:
    def __init__(self,
                 name: str,
                 cards: List[Card],
                 meta: Optional[Dict] = None):

        self.name: str = name
        self.cards: List[Card] = list(cards)
        self.original_cards: List[Card] = list(cards)
        self.meta: Optional[Dict] = meta

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def draw_one(self) -> Card | None:
        if len(self.cards) > 0:
            card = self.cards.pop()
            return card
        else:
            return None

    def draw_many(self, n: int) -> list[Card]:
        draw_cards = []
        counter = 0

        if n < 0:
            raise ValueError

        while counter < n and not self.is_empty():
            card = self.draw_one()
            draw_cards.append(card)
            counter += 1
        return draw_cards

    def is_empty(self) -> bool:
        return not self.cards

    def __len__(self) -> int:
        return len(self.cards)

    def peek(self, n: int) -> list[Card]:
        if n < 0:
            raise ValueError

        top_n = self.cards[-n:]
        return top_n
