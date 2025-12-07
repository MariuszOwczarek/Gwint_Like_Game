from src.card_duel.controller import GameController
from src.card_duel.cli.input_handler import InputHandlerCLI
from src.card_duel.cli.renderer_cli import RendererCLI
from src.card_duel.card import Card, RowAffinity
from src.card_duel.deck import Deck
from src.card_duel.player import Player
from src.card_duel.board import Board
from src.card_duel.rules import Rules
from src.card_duel.game import Game


def main() -> None:
    deck_1_cards = [
        # MELEE
        Card(1, "Redanian Footman", 5, RowAffinity.MELEE, []),
        Card(2, "Kaedweni Sergeant", 6, RowAffinity.MELEE, []),
        Card(3, "Temerian Pikeman", 4, RowAffinity.MELEE, []),
        Card(4, "Order Knight", 8, RowAffinity.MELEE, []),
        Card(5, "Blue Stripes Commando", 7, RowAffinity.MELEE, []),
        Card(6, "Royal Guard", 9, RowAffinity.MELEE, []),
        Card(7, "Northern Swordsman", 6, RowAffinity.MELEE, []),
        Card(8, "Radovid’s Enforcer", 7, RowAffinity.MELEE, []),
        Card(9, "Shield Bearer", 5, RowAffinity.MELEE, []),

        # RANGED
        Card(10, "Redanian Archer", 5, RowAffinity.RANGED, []),
        Card(11, "Kaedweni Crossbowman", 6, RowAffinity.RANGED, []),
        Card(12, "Temerian Sharpshooter", 7, RowAffinity.RANGED, []),
        Card(13, "Royal Ballista Crew", 6, RowAffinity.RANGED, []),
        Card(14, "Scout of the North", 4, RowAffinity.RANGED, []),
        Card(15, "Highland Bowman", 5, RowAffinity.RANGED, []),
        Card(16, "Siege Spotter", 6, RowAffinity.RANGED, []),
        Card(17, "Border Ranger", 7, RowAffinity.RANGED, []),

        # SIEGE
        Card(18, "Trebuchet", 7, RowAffinity.SIEGE, []),
        Card(19, "Heavy Catapult", 8, RowAffinity.SIEGE, []),
        Card(20, "Field Mortar", 6, RowAffinity.SIEGE, []),
        Card(21, "Siege Tower", 5, RowAffinity.SIEGE, []),
        Card(22, "Bombard Cannon", 9, RowAffinity.SIEGE, []),
        Card(23, "Light Catapult", 4, RowAffinity.SIEGE, []),
        Card(24, "Fortification Engine", 8, RowAffinity.SIEGE, []),
        Card(25, "Northern Ballista", 6, RowAffinity.SIEGE, []),
    ]

    deck_2_cards = [
        # MELEE
        Card(101, "Clan Drummond Raider", 6, RowAffinity.MELEE, []),
        Card(102, "Sea Wolf Berserker", 7, RowAffinity.MELEE, []),
        Card(103, "An Craite Warrior", 5, RowAffinity.MELEE, []),
        Card(104, "Skellige Champion", 9, RowAffinity.MELEE, []),
        Card(105, "Isles Reaver", 6, RowAffinity.MELEE, []),
        Card(106, "Stormaxe Veteran", 8, RowAffinity.MELEE, []),
        Card(107, "Shieldbreaker", 5, RowAffinity.MELEE, []),
        Card(108, "Wave-Crusher", 7, RowAffinity.MELEE, []),
        Card(109, "Bloodax Marauder", 6, RowAffinity.MELEE, []),

        # RANGED
        Card(110, "Skellige Javeliner", 5, RowAffinity.RANGED, []),
        Card(111, "Harpoon Thrower", 6, RowAffinity.RANGED, []),
        Card(112, "Storm Coast Archer", 7, RowAffinity.RANGED, []),
        Card(113, "Longboat Sniper", 6, RowAffinity.RANGED, []),
        Card(114, "Islander Scout", 4, RowAffinity.RANGED, []),
        Card(115, "Cliff Watcher", 5, RowAffinity.RANGED, []),
        Card(116, "Skerry Pathfinder", 6, RowAffinity.RANGED, []),
        Card(117, "Windcaller Marksman", 7, RowAffinity.RANGED, []),

        # SIEGE
        Card(118, "War Longship", 7, RowAffinity.SIEGE, []),
        Card(119, "Harbor Ram", 8, RowAffinity.SIEGE, []),
        Card(120, "Siege Drakar", 6, RowAffinity.SIEGE, []),
        Card(121, "Hull Breaker", 5, RowAffinity.SIEGE, []),
        Card(122, "Storm Ram", 9, RowAffinity.SIEGE, []),
        Card(123, "Deck Ballista", 4, RowAffinity.SIEGE, []),
        Card(124, "Iron Longship", 8, RowAffinity.SIEGE, []),
        Card(125, "Shipboard Catapult", 6, RowAffinity.SIEGE, []),
    ]

    deck1 = Deck("Northern Alliance", deck_1_cards)
    deck2 = Deck("Skellige Raiders", deck_2_cards)

    player1 = Player(1, deck1)
    player2 = Player(2, deck2)

    board = Board([1, 2])
    rules = Rules(rounds_to_win=2)

    game = Game([player1, player2], board, rules)
    input_handler = InputHandlerCLI()
    renderer = RendererCLI()

    controller = GameController(game, input_handler, renderer)
    controller.run_match()


if __name__ == "__main__":
    main()
