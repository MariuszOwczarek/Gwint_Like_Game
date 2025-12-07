from src.card_duel.game import Game
from src.card_duel.player import Player
from src.card_duel.card import RowAffinity


class InputHandlerCLI:
    """Odpowiada wyłącznie za zbieranie decyzji od gracza (input())."""

    def choose_action(self, game: Game, player: Player) -> str:
        """
        Zwraca 'play' albo 'pass'.
        """
        while True:
            choice = input("Choose action: (p)lay card / (s)kip(pass): ").strip().lower()
            if choice == "p":
                return "play"
            if choice == "s":
                return "pass"
            print("Unknown action, please choose 'p' or 's'.")

    def choose_card_index(self, game: Game, player: Player) -> int:
        """
        Pyta o indeks karty z ręki, zwraca int.
        """
        if player.hand_size() == 0:
            raise ValueError("No cards in hand to play.")

        while True:
            idx_str = input("Enter card index to play: ").strip()
            try:
                card_index = int(idx_str)
            except ValueError:
                print("Invalid number, try again.")
                continue

            if 0 <= card_index < player.hand_size():
                return card_index

            print(f"Index out of range. Choose 0..{player.hand_size() - 1}.")

    def choose_row_affinity(self, game: Game, player: Player) -> RowAffinity:
        """
        Na razie uproszczenie: wszystkie karty gramy w MELEE.
        Interfejs zostawiamy gotowy na przyszłość.
        """
        # Możesz kiedyś zrobić input z wyborem MELEE/RANGED/SIEGE.
        return RowAffinity.MELEE
