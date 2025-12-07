import pygame
from typing import Optional

from src.card_duel.game import Game
from src.card_duel.player import Player
from src.card_duel.card import RowAffinity


# Proste kolory
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (60, 60, 60)
DARK_GREY = (30, 30, 30)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 120, 200)
YELLOW = (220, 220, 0)


class RendererPygame:
    """
    Renderer Pygame – odpowiednik RendererCLI.
    Rysuje:
      - planszę (3 rzędy na gracza),
      - rękę aktywnego gracza,
      - podstawowe informacje o meczu.
    """

    def __init__(self, width: int = 1024, height: int = 768) -> None:
        pygame.init()
        pygame.display.set_caption("GWINT-like (Pygame)")
        self.screen = pygame.display.set_mode((width, height))
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("consolas", 18)
        self.big_font = pygame.font.SysFont("consolas", 24, bold=True)

        # do zapamiętania aktualnego gracza dla nagłówków itp.
        self._active_player: Optional[Player] = None
        self._last_round_msg: Optional[str] = None
        self._last_match_msg: Optional[str] = None

    # --- API kompatybilne z RendererCLI ---

    def render_game_state(self, game: Game) -> None:
        """Rysuje pełny stan gry."""
        self._draw(game)

    def render_player_turn_header(self, player: Player) -> None:
        """Zapamiętuje, czyj jest ruch, i odrysowuje."""
        self._active_player = player

    def render_player_hand(self, player: Player) -> None:
        """Ręka jest rysowana jako część ogólnego stanu – tu nic nie trzeba robić."""
        # nic – ręka jest rysowana w _draw() na podstawie self._active_player
        pass

    def render_round_start(self, round_number: int) -> None:
        self._last_round_msg = f"START ROUND {round_number}"

    def render_round_end(self, game: Game) -> None:
        # prosty komunikat, kto wygrał rundę
        board = game.board
        player_ids = list(game.players.keys())
        if len(player_ids) == 2:
            p1, p2 = player_ids
            p1_power = board.get_total_power(p1)
            p2_power = board.get_total_power(p2)
            if p1_power > p2_power:
                msg = f"ROUND OVER – Player {p1} wins ({p1_power} vs {p2_power})"
            elif p2_power > p1_power:
                msg = f"ROUND OVER – Player {p2} wins ({p2_power} vs {p1_power})"
            else:
                msg = f"ROUND OVER – draw ({p1_power} vs {p2_power})"
        else:
            msg = "ROUND OVER"
        self._last_round_msg = msg

    def render_match_result(self, game: Game) -> None:
        if game.is_match_over():
            winner_id = game.get_match_winner_id()
            if winner_id is not None:
                self._last_match_msg = f"MATCH OVER – Winner: Player {winner_id}"
            else:
                self._last_match_msg = "MATCH OVER – draw"
        else:
            self._last_match_msg = "MATCH ENDED"

        # końcowy ekran – odrysuj i poczekaj na zamknięcie okna
        self._draw(game)
        self._wait_for_exit()

    # --- Rysowanie właściwe ---

    def _draw(self, game: Game) -> None:
        self.screen.fill(DARK_GREY)

        # Górny pasek info
        self._draw_header(game)

        # Plansza – 3 rzędy na gracza
        self._draw_board(game)

        # Ręka aktywnego gracza
        if self._active_player is not None:
            self._draw_hand(self._active_player)

        pygame.display.flip()

    def _draw_header(self, game: Game) -> None:
        y = 10
        x = 10

        # aktywny gracz
        if self._active_player is not None:
            text = self.big_font.render(
                f"Player {self._active_player.id}'s turn (P=play, S=pass, 0-9=card index)",
                True,
                YELLOW,
            )
            self.screen.blit(text, (x, y))
            y += 30

        # rundy wygrane
        for pid, player in game.players.items():
            text = self.font.render(
                f"Player {pid}: rounds_won={player.rounds_won}, hand={player.hand_size()}, passed={player.has_passed}",
                True,
                WHITE,
            )
            self.screen.blit(text, (x, y))
            y += 20

        # komunikaty rundy / meczu
        if self._last_round_msg:
            text = self.font.render(self._last_round_msg, True, GREEN)
            self.screen.blit(text, (x, y))
            y += 20

        if self._last_match_msg:
            text = self.font.render(self._last_match_msg, True, RED)
            self.screen.blit(text, (x, y+200))
            

    def _draw_board(self, game: Game) -> None:
        board = game.board
        player_ids = list(game.players.keys())

        # jeśli dwóch graczy – przeciwnik na górze, my na dole
        if len(player_ids) == 2:
            top_id, bottom_id = player_ids[1], player_ids[0]
        else:
            top_id = bottom_id = player_ids[0]

        row_order = [RowAffinity.MELEE, RowAffinity.RANGED, RowAffinity.SIEGE]
        row_labels = {
            RowAffinity.MELEE: "MELEE",
            RowAffinity.RANGED: "RANGED",
            RowAffinity.SIEGE: "SIEGE",
        }

        # obszar na board (środek ekranu)
        board_top = 100
        board_height = self.height - 250
        mid_y = board_top + board_height // 2

        # Każdy rząd będzie pasem o wysokości ~40px
        row_height = 40
        padding = 5

        # --- Gracz na górze ---
        y = board_top
        total_top = board.get_total_power(top_id)
        text = self.font.render(f"Player {top_id} (total: {total_top})", True, WHITE)
        self.screen.blit(text, (10, y))
        y += 25

        for affinity in row_order:
            row = board.get_row(top_id, affinity)
            powers = [card.base_power for card in row.cards]
            row_total = sum(powers) if powers else 0

            label_text = self.font.render(f"{row_labels[affinity]} ({row_total})", True, WHITE)
            self.screen.blit(label_text, (10, y))

            # Karty jako prostokąty
            card_x = 200
            for p in powers:
                rect = pygame.Rect(card_x, y, 30, row_height - padding)
                pygame.draw.rect(self.screen, BLUE, rect)
                power_surf = self.font.render(str(p), True, WHITE)
                self.screen.blit(power_surf, (card_x + 8, y + 10))
                card_x += 35

            y += row_height

        # --- Gracz na dole ---
        y = mid_y + 20
        total_bottom = board.get_total_power(bottom_id)
        text = self.font.render(f"Player {bottom_id} (total: {total_bottom})", True, WHITE)
        self.screen.blit(text, (10, y))
        y += 25

        for affinity in row_order:
            row = board.get_row(bottom_id, affinity)
            powers = [card.base_power for card in row.cards]
            row_total = sum(powers) if powers else 0

            label_text = self.font.render(f"{row_labels[affinity]} ({row_total})", True, WHITE)
            self.screen.blit(label_text, (10, y))

            card_x = 200
            for p in powers:
                rect = pygame.Rect(card_x, y, 30, row_height - padding)
                pygame.draw.rect(self.screen, GREEN, rect)
                power_surf = self.font.render(str(p), True, WHITE)
                self.screen.blit(power_surf, (card_x + 8, y + 10))
                card_x += 35

            y += row_height

    def _draw_hand(self, player: Player) -> None:
        """Rysuje rękę aktywnego gracza na dole ekranu."""
        y = self.height - 120
        x = 10

        label = self.font.render(f"Player {player.id} hand:", True, WHITE)
        self.screen.blit(label, (x, y))
        y += 25

        card_width = 70
        card_height = 80
        gap = 10

        for idx, card in enumerate(player.hand):
            rect = pygame.Rect(x, y, card_width, card_height)
            pygame.draw.rect(self.screen, GREY, rect)
            pygame.draw.rect(self.screen, WHITE, rect, 2)

            idx_text = self.font.render(str(idx), True, YELLOW)
            name_text = self.font.render(card.name[:10], True, WHITE)
            power_text = self.font.render(str(card.base_power), True, WHITE)

            self.screen.blit(idx_text, (x + 4, y + 4))
            self.screen.blit(name_text, (x + 4, y + 24))
            self.screen.blit(power_text, (x + 4, y + 44))

            x += card_width + gap

    def _wait_for_exit(self) -> None:
        """Czeka aż użytkownik zamknie okno po zakończeniu meczu."""
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
            pygame.time.delay(50)

        pygame.quit()


class InputHandlerPygame:
    """
    Input handler oparty o Pygame – odpowiednik InputHandlerCLI.
    Używa klawiatury:
      - P -> play
      - S -> pass
      - 0-9 -> indeks karty z ręki
    """

    def __init__(self) -> None:
        # nic specjalnego na start
        pass

    def choose_action(self, game: Game, player: Player) -> str:
        """
        Czeka na decyzję: 'play' lub 'pass'.
        P -> 'play'
        S -> 'pass'
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit("Window closed")

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        return "play"
                    if event.key == pygame.K_s:
                        return "pass"

            pygame.time.delay(50)

    def choose_card_index(self, game: Game, player: Player) -> int:
        """
        Czeka na naciśnięcie cyfry 0-9 i zwraca ją jako indeks karty.
        """
        if player.hand_size() == 0:
            raise ValueError("No cards in hand to play.")

        max_idx = player.hand_size() - 1

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit("Window closed")

                if event.type == pygame.KEYDOWN:
                    # cyfry 0-9
                    if pygame.K_0 <= event.key <= pygame.K_9:
                        idx = event.key - pygame.K_0
                        if 0 <= idx <= max_idx:
                            return idx
                        # poza zakresem – ignorujemy
            pygame.time.delay(50)

    def choose_row_affinity(self, game: Game, player: Player) -> RowAffinity:
        """
        Na razie uproszczenie: wszystkie karty gramy w MELEE.
        Można to potem rozbudować o klawisze:
          - 1 -> MELEE
          - 2 -> RANGED
          - 3 -> SIEGE
        """
        return RowAffinity.MELEE
