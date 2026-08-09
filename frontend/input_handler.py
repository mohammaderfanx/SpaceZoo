"""
Input handler for SpaceZoo frontend.
References ARCHITECTURE.md: frontend must communicate with backend only via SpaceZooAPI.

This module captures WASD input and sends movement commands to the API.
"""

import pygame
from typing import Tuple
from interface.spacezoo_api import SpaceZooAPI


class InputHandler:
    """Handles keyboard input and dispatches movement commands to the API."""

    def __init__(self) -> None:
        # movement cooldown to avoid overly fast repeated moves when holding a key
        self.move_cooldown = 0.08  # seconds between auto-moves when holding
        self._time_since_move = 0.0

    def process_event(self, event: "pygame.event.Event", api: SpaceZooAPI) -> None:
        """Process discrete keydown events.

        :param event: Pygame event
        :param api: SpaceZooAPI instance
        """
        if event.type == pygame.KEYDOWN:
            dx, dy = 0, 0
            if event.key == pygame.K_w:
                dx, dy = 0, -1
            elif event.key == pygame.K_s:
                dx, dy = 0, 1
            elif event.key == pygame.K_a:
                dx, dy = -1, 0
            elif event.key == pygame.K_d:
                dx, dy = 1, 0

            if dx != 0 or dy != 0:
                api.move_player(dx, dy)

    def handle_held_keys(self, delta: float, api: SpaceZooAPI) -> None:
        """Handle movement when keys are held down (auto-repeat).

        :param delta: Time since last frame in seconds
        :param api: SpaceZooAPI instance
        """
        self._time_since_move += delta
        pressed = pygame.key.get_pressed()
        if self._time_since_move >= self.move_cooldown:
            dx, dy = 0, 0
            if pressed[pygame.K_w]:
                dx, dy = 0, -1
            elif pressed[pygame.K_s]:
                dx, dy = 0, 1
            elif pressed[pygame.K_a]:
                dx, dy = -1, 0
            elif pressed[pygame.K_d]:
                dx, dy = 1, 0

            if dx != 0 or dy != 0:
                api.move_player(dx, dy)
                self._time_since_move = 0.0
