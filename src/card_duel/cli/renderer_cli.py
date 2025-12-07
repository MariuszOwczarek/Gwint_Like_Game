from src.card_duel.game import Game
from src.card_duel.player import Player
from src.card_duel.card import RowAffinity


class RendererCLI:
    """Odpowiada wyłącznie za wypisywanie stanu gry w konsoli."""

    def render_game_state(self, game: Game) -> None:
        print("\n=== GAME STATE ===")
        for pid, player in game.players.items():
            print(f"Player {pid}:")
            print(f"  Rounds won: {player.rounds_won}")
            print(f"  Hand size: {player.hand_size()}")
            print(f"  Has passed: {player.has_passed}")
            total_power = game.board.get_total_power(pid)
            print(f"  Board power: {total_power}")
        print("==================\n")
        self.render_board(game)

    def render_board(self, game: Game) -> None:
        """
        Wyświetla aktualny układ kart na planszy:
        - dla każdego gracza:
          - całkowita moc na planszy,
          - dla każdego rzędu: lista mocy kart i suma rzędu.
        """
        board = game.board

        # Kolejność graczy: przeciwnik u góry, my na dole (jeśli są dwaj)
        player_ids = list(game.players.keys())
        if len(player_ids) == 2:
            ordered_ids = [player_ids[1], player_ids[0]]
        else:
            ordered_ids = player_ids

        row_order = [RowAffinity.MELEE, RowAffinity.RANGED, RowAffinity.SIEGE]
        row_names = {
            RowAffinity.MELEE: "MELEE ",
            RowAffinity.RANGED: "RANGED",
            RowAffinity.SIEGE: "SIEGE ",
        }

        print("============== BOARD ==============")
        for pid in ordered_ids:
            player = game.players[pid]
            total_power = board.get_total_power(pid)
            print(f"Player {pid} (total: {total_power})")

            for affinity in row_order:
                row = board.get_row(pid, affinity)
                powers = [card.base_power for card in row.cards]
                row_total = sum(powers) if powers else 0

                # prosta reprezentacja: [ 5 7 3 ]
                if powers:
                    powers_str = " ".join(f"{p:2d}" for p in powers)
                    row_repr = f"[ {powers_str} ]"
                else:
                    row_repr = "[    ]"

                print(f"  {row_names[affinity]}: {row_repr} = {row_total}")
            print()  # pusta linia między graczami

        print("===================================\n")



    def render_player_turn_header(self, player: Player) -> None:
        print(f"--- Player {player.id}'s turn ---")

    def render_player_hand(self, player: Player) -> None:
        print(f"\nPlayer {player.id} hand:")
        if not player.hand:
            print("  (no cards in hand)")
            return
        for idx, card in enumerate(player.hand):
            print(f"  [{idx}] {card.name} (power={card.base_power}, row={card.row_affinity.name})")
        print()

    def render_round_start(self, round_number: int) -> None:
        print(f"\n=== START ROUND {round_number} ===")

    def render_round_end(self, game: Game) -> None:
        board = game.board
        print("\n=== ROUND OVER ===")
        for pid in game.players.keys():
            total_power = board.get_total_power(pid)
            print(f"Player {pid} total power: {total_power}")
        for pid, player in game.players.items():
            print(f"Rounds won P{pid}: {player.rounds_won}")

    def render_match_result(self, game: Game) -> None:
        print("\n=== MATCH RESULT ===")
        self.render_game_state(game)
        if game.is_match_over():
            winner_id = game.get_match_winner_id()
            if winner_id is not None:
                print(f"Winner: Player {winner_id}")
            else:
                print("Match over, but no winner (draw).")
        else:
            print("Match ended without reaching required rounds_to_win.")
