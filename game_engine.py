
import math
from array import array

import pygame
from .round import Round

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (90, 90, 90)
GREEN = (40, 180, 90)
BLUE = (50, 90, 170)
RED = (190, 55, 55)
DARK = (30, 35, 45)
YELLOW = (245, 205, 80)


class GameEngine:
    def __init__(
        self, width, height, rounds_total=5,
        min_wait_ms=1000, max_wait_ms=3000
    ):
        self.width = width
        self.height = height
        self.rounds_total = rounds_total
        self.min_wait_ms = min_wait_ms
        self.max_wait_ms = max_wait_ms

        self.reaction_times = []
        self.rounds_completed = 0
        self.result_shown_at = None
        self.result_pause_ms = 1000

        self.difficulty = "Medium"
        self.game_over = False
        self.exited = False
        self._game_over_logged = False
        self._last_go_time = None

        self.font = pygame.font.SysFont("Arial", 23)
        self.big_font = pygame.font.SysFont("Arial", 38)
        self.small_font = pygame.font.SysFont("Arial", 18)

        self.round = Round(self.min_wait_ms, self.max_wait_ms)

        # Keep the existing sound effects.
        self.sounds = {}
        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init()
            self.sounds["go"] = self._make_sound(880, 120)
            self.sounds["false"] = self._make_sound(220, 250)
            self.sounds["end"] = self._make_sound(660, 300)
        except pygame.error:
            self.sounds = {}

    def _make_sound(self, frequency, duration_ms):
        sample_rate = 22050
        count = int(sample_rate * duration_ms / 1000)
        samples = array("h")

        for i in range(count):
            envelope = min(1.0, (count - i) / (sample_rate * 0.02))
            value = int(
                10000
                * envelope
                * math.sin(2 * math.pi * frequency * i / sample_rate)
            )
            samples.append(value)

        return pygame.mixer.Sound(buffer=samples.tobytes())

    def _play_sound(self, name):
        try:
            sound = self.sounds.get(name)
            if sound:
                sound.play()
        except pygame.error:
            pass

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.exited = True
            return

        if self.game_over:
            self._handle_game_over_event(event)
            return

        is_click = event.type == pygame.MOUSEBUTTONDOWN
        is_space = (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_SPACE
        )

        if not (is_click or is_space):
            return

        # Task 1: Update the state before classifying input.
        # An input after the wait deadline should not be marked
        # as a false start just because update() has not run yet.
        self.round.update()

        if self.round.state not in ("waiting", "go"):
            return

        was_waiting = self.round.state == "waiting"

        if was_waiting:
            # Input during the grey phase is a false start.
            self.round.register_input()
            self._play_sound("false")
        else:
            # Input after the green transition is a valid reaction.
            reaction_ms = self.round.register_input()

            if reaction_ms is not None:
                self.reaction_times.append(reaction_ms)

        self.rounds_completed += 1
        self.result_shown_at = pygame.time.get_ticks()

    def _handle_game_over_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.exited = True
            elif event.key == pygame.K_r:
                self._restart(self.difficulty)
            elif event.key == pygame.K_1:
                self._restart("Easy")
            elif event.key == pygame.K_2:
                self._restart("Medium")
            elif event.key == pygame.K_3:
                self._restart("Hard")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if 90 <= y <= 145:
                self._restart("Easy")
            elif 155 <= y <= 210:
                self._restart("Medium")
            elif 220 <= y <= 275:
                self._restart("Hard")
            elif 285 <= y <= 340:
                self.exited = True

    def _restart(self, difficulty):
        settings = {
            "Easy": (1500, 3500, 5),
            "Medium": (1000, 3000, 5),
            "Hard": (500, 2000, 10),
        }

        self.difficulty = difficulty
        self.min_wait_ms, self.max_wait_ms, self.rounds_total = (
            settings[difficulty]
        )

        self.reaction_times = []
        self.rounds_completed = 0
        self.result_shown_at = None
        self.game_over = False
        self._game_over_logged = False
        self._last_go_time = None
        self.round = Round(self.min_wait_ms, self.max_wait_ms)

    def handle_input(self):
        pass

    def update(self):
        if self.game_over or self.exited:
            return

        self.round.update()

        # Play the go sound once when the round transitions to green.
        if (
            self.round.state == "go"
            and self._last_go_time != self.round.go_time
        ):
            self._last_go_time = self.round.go_time
            self._play_sound("go")

        if (
            self.round.state == "result"
            and self.result_shown_at is not None
        ):
            now = pygame.time.get_ticks()

            if now - self.result_shown_at >= self.result_pause_ms:
                if self.rounds_completed >= self.rounds_total:
                    self.game_over = True
                    self._play_sound("end")
                else:
                    self.round = Round(
                        self.min_wait_ms, self.max_wait_ms
                    )
                    self.result_shown_at = None

    def average_reaction_ms(self):
        if not self.reaction_times:
            return 0

        return round(
            sum(self.reaction_times) / len(self.reaction_times)
        )

    def _draw_centered(self, screen, message, y, color=WHITE, font=None):
        font = font or self.font
        surface = font.render(message, True, color)
        rect = surface.get_rect(center=(self.width // 2, y))
        screen.blit(surface, rect)

    def render(self, screen):
        if self.game_over:
            self._render_game_over(screen)
            return

        if self.round.state == "waiting":
            screen.fill(GRAY)
            message = "Wait for green..."
        elif self.round.state == "go":
            screen.fill(GREEN)
            message = "Click now!"
        else:
            screen.fill(RED if self.round.false_start else BLUE)
            message = (
                "FALSE START!"
                if self.round.false_start
                else f"{self.round.reaction_ms} ms"
            )

        self._draw_centered(
            screen, message, self.height // 2, WHITE, self.big_font
        )

        current_round = min(
            self.rounds_completed + 1, self.rounds_total
        )
        screen.blit(
            self.font.render(
                f"Round {current_round}/{self.rounds_total}",
                True, WHITE
            ),
            (10, 10),
        )
        screen.blit(
            self.font.render(
                f"Avg: {self.average_reaction_ms()} ms",
                True, WHITE
            ),
            (self.width - 190, 10),
        )
        screen.blit(
            self.small_font.render(
                f"Difficulty: {self.difficulty}", True, WHITE
            ),
            (10, self.height - 30),
        )

    def _render_game_over(self, screen):
        screen.fill(DARK)

        self._draw_centered(
            screen, "SESSION COMPLETE", 30, YELLOW, self.big_font
        )

        valid_times = ", ".join(
            f"{time} ms" for time in self.reaction_times
        )
        if not valid_times:
            valid_times = "No valid reactions recorded"

        self._draw_centered(
            screen, f"Times: {valid_times}", 72, WHITE, self.small_font
        )
        self._draw_centered(
            screen,
            f"Average: {self.average_reaction_ms()} ms",
            108, YELLOW, self.font
        )
        self._draw_centered(
            screen, "Choose a difficulty to play again", 137,
            WHITE, self.small_font
        )

        options = [
            ("1 - EASY", 175),
            ("2 - MEDIUM", 230),
            ("3 - HARD", 285),
            ("EXIT (Esc)", 340),
        ]

        for label, y in options:
            self._draw_centered(screen, label, y, WHITE, self.font)

        if not self._game_over_logged:
            print("Session complete! Reaction times:", self.reaction_times)
            print("Average:", self.average_reaction_ms(), "ms")
            self._game_over_logged = True
