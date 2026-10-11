
import random
import pygame


class Round:
    def __init__(self, min_wait_ms=1000, max_wait_ms=3000):
        self.wait_delay_ms = random.randint(min_wait_ms, max_wait_ms)
        self.state = "waiting"

        # Time when the waiting phase begins.
        self.start_time = pygame.time.get_ticks()

        # Time when the screen changes to green.
        self.go_time = None

        # Result for this round.
        self.reaction_ms = None
        self.false_start = False

    def update(self):
        if self.state != "waiting":
            return

        now = pygame.time.get_ticks()

        if now - self.start_time >= self.wait_delay_ms:
            self.state = "go"
            self.go_time = now

    def register_input(self):
        # Click or Space during the grey screen.
        if self.state == "waiting":
            self.false_start = True
            self.state = "result"
            self.reaction_ms = None
            return None

        # Ignore input after the round has finished.
        if self.state != "go":
            return None

        # Measure only from the green signal.
        now = pygame.time.get_ticks()
        self.reaction_ms = now - self.go_time
        self.state = "result"

        return self.reaction_ms
