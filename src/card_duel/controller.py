from src.card_duel.game import Game
from src.card_duel.cli.input_handler import InputHandlerCLI
from src.card_duel.cli.renderer_cli import RendererCLI
from src.card_duel.card import RowAffinity


INITIAL_HAND_SIZE = 10
CARDS_BETWEEN_ROUNDS = 2
MAX_ROUNDS = 3


class GameController:
    """
    Orkiestruje przebieg meczu:
    - start meczu,
    - pętla rund,
    - pętla tur,
    - dobieranie kart wg zasad Gwinta.
    Nie używa print/input bezpośrednio – deleguje do RendererCLI / InputHandlerCLI.
    """

    def __init__(
        self,
        game: Game,
        input_handler: InputHandlerCLI,
        renderer: RendererCLI,
    ) -> None:
        self.game = game
        self.input = input_handler
        self.renderer = renderer

    def _initial_draw(self) -> None:
        """
        Start gry wg Gwinta:
        - każdy gracz dobiera 10 kart do ręki (o ile są w talii).
        """
        for player in self.game.players.values():
            player.draw_from_deck(INITIAL_HAND_SIZE)

    def _draw_between_rounds(self) -> None:
        """
        Gwintowa zasada:
        - po każdej zakończonej rundzie dobierz 2 karty do ręki (o ile są w talii).
        """
        for player in self.game.players.values():
            player.draw_from_deck(CARDS_BETWEEN_ROUNDS)

    def run_match(self) -> None:
        """
        Główna pętla meczu:
        - startuje mecz,
        - wykonuje initial draw,
        - uruchamia kolejne rundy,
        - w każdej rundzie naprzemienne tury graczy,
        - po rundzie dobiera karty,
        - kończy, gdy Rules.is_match_over() lub po 3 rundach.
        """
        self.game.start_match()
        self._initial_draw()

        while not self.game.is_match_over() and self.game.current_round < MAX_ROUNDS:
            # start nowej rundy
            self.game.start_round()
            self.renderer.render_round_start(self.game.current_round)

            # pętla tur w ramach rundy
            while not self.game.is_round_over():
                active_id = self.game.get_active_player_id()
                if active_id is None:
                    # sytuacja awaryjna – nie powinno się zdarzyć przy poprawnym Game
                    break

                active_player = self.game.players[active_id]

                # CLI
                #self.renderer.render_game_state(self.game)
                #self.renderer.render_player_turn_header(active_player)
                #self.renderer.render_player_hand(active_player)

                #PYGAME
                self.renderer.render_player_turn_header(active_player)
                self.renderer.render_player_hand(active_player)
                self.renderer.render_game_state(self.game)


                action = self.input.choose_action(self.game, active_player)

                if action == "play":
                    # jeśli gracz nie ma kart – musi pasować
                    if active_player.hand_size() == 0:
                        try:
                            self.game.pass_turn(active_id)
                        except Exception:
                            # wyjątków nie obsługujemy tutaj szczegółowo – to logika Game/Rules
                            break
                        continue

                    try:
                        card_index = self.input.choose_card_index(self.game, active_player)
                        row_affinity = self.input.choose_row_affinity(self.game, active_player)
                        self.game.play_card(active_id, card_index, row_affinity)
                    except Exception:
                        # błąd logiki/akcji – w prostym CLI po prostu przerywamy turę
                        continue

                elif action == "pass":
                    try:
                        self.game.pass_turn(active_id)
                    except Exception:
                        # błąd logiki – przerywamy pętlę dla bezpieczeństwa
                        break

                else:
                    # teoretycznie nie powinno się zdarzyć, jeśli InputHandler działa poprawnie
                    continue

            # koniec rundy
            self.renderer.render_round_end(self.game)

            if self.game.is_match_over() or self.game.current_round >= MAX_ROUNDS:
                break

            # dobieranie kart między rundami wg zasad Gwinta
            self._draw_between_rounds()

        # koniec meczu – wynik końcowy
        self.renderer.render_match_result(self.game)
