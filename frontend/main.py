"""
author: Mohammad Rezaei
date: 08.08.2026
version: 1

Frontend entrypoint for SimZoo.
Initializes a Pygame window and runs the main loop.
Imports the `SimZooAPI` as the only interface to the backend.

This is a dashboard-only view: no map background, no player sprite/movement.
"""
import pygame
import time
import os
import sys
from typing import Tuple

# Add the project root to the Python path for package imports.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Normal imports follow.
from interface.simzoo_api import SimZooAPI
from frontend.ui_manager import UIManager

NATIVE_SIZE = (1260, 1000)


def _initial_window_size(native_size: "Tuple[int, int]") -> "Tuple[int, int]":
    """Compute a start window size that fits within the available screen area.

    Scales the native size to fit within a margin of the current display.
    If the display cannot be queried, returns the native size unchanged.
    """
    native_w, native_h = native_size
    try:
        info = pygame.display.Info()
        avail_w, avail_h = info.current_w, info.current_h
    except Exception:
        return native_size

    if avail_w <= 0 or avail_h <= 0:
        return native_size

    margin_w, margin_h = 0.9, 0.85
    scale = min(1.0, (avail_w * margin_w) / native_w, (avail_h * margin_h) / native_h)
    return (max(1, int(native_w * scale)), max(1, int(native_h * scale)))


def main() -> None:
    """Initialize Pygame, create the frontend subsystems, and run the main loop."""
    pygame.init()

    native_size = NATIVE_SIZE

    # Internal render surface in fixed native resolution; it is scaled each frame to
    # the current resizable window size.
    game_surface = pygame.Surface(native_size)

    screen = pygame.display.set_mode(_initial_window_size(native_size), pygame.RESIZABLE)
    pygame.display.set_caption("SimZoo")

    clock = pygame.time.Clock()
    api = SimZooAPI()
    ui_manager = UIManager()

    running = True
    last_time = time.time()

    while running:
        # Map the current window size back to the native surface's coordinate
        # space so mouse clicks line up with what's actually on screen.
        window_w, window_h = screen.get_size()
        scale = min(window_w / native_size[0], window_h / native_size[1])
        scaled_w = max(1, int(native_size[0] * scale))
        scaled_h = max(1, int(native_size[1] * scale))
        offset_x = (window_w - scaled_w) // 2
        offset_y = (window_h - scaled_h) // 2
        ui_manager.update_viewport(scale, (offset_x, offset_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            ui_manager.process_event(event, api)

        now = time.time()
        delta = now - last_time
        last_time = now

        # Call simulation tick (delta in seconds)
        api.tick(delta)

        # Draw UI (dashboard)
        ui_manager.draw(game_surface, api, native_size[0], native_size[1])

        # Scale the native render surface to the current window size
        # (maintaining aspect ratio; excess space is black).
        scaled_surface = pygame.transform.smoothscale(game_surface, (scaled_w, scaled_h))

        screen.fill((0, 0, 0))
        screen.blit(scaled_surface, (offset_x, offset_y))

        pygame.display.flip()

        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
