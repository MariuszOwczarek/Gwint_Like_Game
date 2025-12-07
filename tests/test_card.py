from src.card_duel.card import Card, RowAffinity
import json
import pytest


@pytest.fixture
def warrior_card():
    return Card(1, "Warrior", 10, RowAffinity.MELEE, tags=['Stun', 'Stress'])


class TestCard:
    def test_card_init_and_attrs(self, warrior_card):

        card = warrior_card

        assert card.id == 1
        assert card.name == 'Warrior'
        assert card.base_power == 10
        assert card.row_affinity is RowAffinity.MELEE
        assert card.tags == ['Stun', 'Stress']

    def test_card_default_tags(self):
        card = Card(1, "Warrior", 10, RowAffinity.MELEE, tags=None)
        assert card.tags == []

    def test_card_eq_and_hash(self):
        card1 = Card(1, "Warrior", 10, RowAffinity.MELEE, tags=[])
        card2 = Card(1, "Warrior", 10, RowAffinity.MELEE, tags=[])
        card3 = Card(2, "Warrior", 10, RowAffinity.MELEE, tags=[])

        assert card1 == card2
        assert card1 != card3
        assert hash(card1) == hash(card2)
        assert hash(card2) != hash(card3)

    def test_card_serialize(self, warrior_card):
        card = warrior_card

        data = card.serialize()
        assert data["id"] == card.id
        assert data["name"] == card.name
        assert data["base_power"] == card.base_power
        assert data["row_affinity"] == card.row_affinity.name
        assert data["tags"] == card.tags

    def test_card_serialize_to_json(self, warrior_card):
        card = warrior_card

        json_str = json.dumps(card.serialize())
        data = json.loads(json_str)
        assert data["id"] == card.id
        assert data["name"] == card.name
        assert data["base_power"] == card.base_power
        assert data["row_affinity"] == card.row_affinity.name
        assert data["tags"] == card.tags

    def test_display_repr_and_repr(self, warrior_card):
        card = warrior_card

        text = repr(card)
        assert "Card(" in text
        assert "id= 1" in text
        assert "name= Warrior" in text
        assert "base_power= 10" in text
        assert "row_affinity= MELEE" in text
        assert "['Stun', 'Stress']" in text

        assert card.display_repr() == "Warrior (10) | Row: MELEE"
