"""
Frontend entrypoint for SpaceZoo.
Initialisiert ein Pygame-Fenster (1260x960) und führt die Game-Loop aus.
Importiert die `SpaceZooAPI` als einzige Schnittstelle zum Backend.
"""
import pygame
import time
import os
import sys

# Fügt das Projekt-Hauptverzeichnis zum Python-Pfad hinzu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Ab hier folgen deine normalen Imports:
from interface.spacezoo_api import SpaceZooAPI
from frontend.map_renderer import MapRenderer
from frontend.input_handler import InputHandler
from frontend.sprite_manager import SpriteManager
from frontend.ui_manager import UIManager


def main() -> None:
    pygame.init()

    renderer = MapRenderer()
    screen_size = renderer.screen_size()

    screen = pygame.display.set_mode(screen_size)
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
        renderer.draw_background(screen)

        # Get full state and render sprites
        try:
            state = api.get_zoo_state()
            sprite_manager.draw_entities(screen, state, renderer.tile_size)
        except Exception:
            state = None

        # Draw UI (taskbar)
        try:
            ui_manager.draw(screen, api, screen_size[0], screen_size[1])
        except Exception:
            pass

        pygame.display.flip()

        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
