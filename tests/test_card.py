from src.card_duel.card import Card, RowAffinity
import json


class TestCard:
    def test_card_init_and_attrs(self):
        card = Card(1,
                    "Warrior",
                    10,
                    RowAffinity.MELEE,
                    tags=['Stun', 'Stress'])

        assert card.id == 1
        assert card.name == 'Warrior'
        assert card.base_power == 10
        assert card.row_affinity.name == 'MELEE'
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

    def test_card_serialize(self):
        card = Card(1,
                    "Warrior",
                    10,
                    RowAffinity.MELEE,
                    tags=['Stun', 'Stress'])

        data = card.serialize()
        assert data["id"] == card.id
        assert data["name"] == card.name
        assert data["base_power"] == card.base_power
        assert data["row_affinity"] == card.row_affinity.name
        assert data["tags"] == card.tags

    def test_card_serialize_to_json(self):
        card = Card(1,
                    "Warrior",
                    10,
                    RowAffinity.MELEE,
                    tags=['Stun', 'Stress'])

        json_str = json.dumps(card.serialize())
        data = json.loads(json_str)
        assert data["id"] == card.id
        assert data["name"] == card.name
        assert data["base_power"] == card.base_power
        assert data["row_affinity"] == card.row_affinity.name
        assert data["tags"] == card.tags

    def test_display_repr_and_repr(self):
        card = Card(1,
                    "Warrior",
                    10,
                    RowAffinity.MELEE,
                    tags=['Stun', 'Stress'])

        assert repr(card) == ("Card(id= 1, "
                              "name= Warrior, "
                              "base_power= 10, "
                              "row_affinity= MELEE, "
                              "tags= ['Stun', 'Stress'])")

        assert card.display_repr() == "Warrior (10) | Row: MELEE"
