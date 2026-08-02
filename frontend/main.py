"""
Frontend entrypoint for SpaceZoo.
Initialisiert ein Pygame-Fenster (1260x960) und führt die Game-Loop aus.
Importiert die `SpaceZooAPI` als einzige Schnittstelle zum Backend.
"""
import pygame
import time
import os
import sys
from typing import Tuple

# Fügt das Projekt-Hauptverzeichnis zum Python-Pfad hinzu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Ab hier folgen deine normalen Imports:
from interface.spacezoo_api import SpaceZooAPI
from frontend.map_renderer import MapRenderer
from frontend.input_handler import InputHandler
from frontend.sprite_manager import SpriteManager
from frontend.ui_manager import UIManager


def _initial_window_size(native_size: "Tuple[int, int]") -> "Tuple[int, int]":
    """Bestimmt eine Startfenstergröße, die auf den verfügbaren Bildschirm passt.

    Skaliert `native_size` (1260x960) so weit herunter, dass es innerhalb eines
    Bereichs des aktuellen Bildschirms (abzüglich Menüleiste/Dock) passt.
    Wird der Bildschirm nicht ermittelt, bleibt die native Größe erhalten.
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
    pygame.init()

    renderer = MapRenderer()
    native_size = renderer.screen_size()

    # Interne Zeichenfläche in fester nativer Auflösung; wird pro Frame auf die
    # tatsächliche (frei skalierbare) Fenstergröße herunter-/hochskaliert.
    game_surface = pygame.Surface(native_size)

    screen = pygame.display.set_mode(_initial_window_size(native_size), pygame.RESIZABLE)
    pygame.display.set_caption("SpaceZoo")

    clock = pygame.time.Clock()
    api = SpaceZooAPI()
    input_handler = InputHandler()
    sprite_manager = SpriteManager()
    ui_manager = UIManager()

    running = True
    last_time = time.time()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            # Let input handler process keydown events
            input_handler.process_event(event, api)
            ui_manager.process_event(event)

        now = time.time()
        delta = now - last_time
        last_time = now

        # Call simulation tick (delta in seconds)
        api.tick(delta)

        # Handle held keys for smooth movement
        input_handler.handle_held_keys(delta, api)

        # Render background map (fallbacks to grid if map missing)
        renderer.draw_background(game_surface)

        # Get full state and render sprites
        try:
            state = api.get_zoo_state()
            sprite_manager.draw_entities(game_surface, state, renderer.tile_size)
        except Exception:
            state = None

        # Draw UI (taskbar)
        try:
            ui_manager.draw(game_surface, api, native_size[0], native_size[1])
        except Exception:
            pass

        # Skaliere die native Zeichenfläche auf die aktuelle Fenstergröße
        # (Seitenverhältnis bleibt erhalten, überschüssiger Platz wird schwarz).
        window_w, window_h = screen.get_size()
        scale = min(window_w / native_size[0], window_h / native_size[1])
        scaled_w = max(1, int(native_size[0] * scale))
        scaled_h = max(1, int(native_size[1] * scale))
        scaled_surface = pygame.transform.smoothscale(game_surface, (scaled_w, scaled_h))

        screen.fill((0, 0, 0))
        screen.blit(scaled_surface, ((window_w - scaled_w) // 2, (window_h - scaled_h) // 2))

        pygame.display.flip()

        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
