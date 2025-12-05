from enum import Enum
from typing import List, Optional


class RowAffinity(Enum):
    MELEE = 1
    RANGED = 2
    SIEGE = 3
    ANY = 4


class Card:
    def __init__(self,
                 id: int,
                 name: str,
                 base_power: int,
                 row_affinity: RowAffinity,
                 tags: Optional[List[str]]):

        self.id = id
        self.name = name
        self.base_power = base_power
        self.row_affinity: RowAffinity = row_affinity  # RowAffinity(Enum)
        self.tags: Optional[List[str]] = list(tags) if tags is not None else []

    def __repr__(self):
        return (f'Card(id= {self.id}, '
                f'name= {self.name}, '
                f'base_power= {self.base_power}, '
                f'row_affinity= {self.row_affinity.name}, '
                f'tags= {self.tags})')

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.id == other.id
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.id)

    def serialize(self) -> dict:
        card_dict = {
                    "id": int(self.id),
                    "name": str(self.name),
                    "base_power": int(self.base_power),
                    "row_affinity": self.row_affinity.name,
                    "tags": [str(t) for t in (self.tags or [])]
                    }
        return card_dict

    def display_repr(self):
        card_repr = (f'{self.name} ({self.base_power}) '
                     f'| Row: {self.row_affinity.name}')
        return card_repr

    def to_dict(self):
        pass

    @classmethod
    def from_dict(cls, data):
        pass

    def clone(self):
        pass

    def on_play(self, game, owner, row):
        pass

    def validate(self):
        pass
