"""Headless renderer for SpaceZoo.

This script runs the frontend rendering pipeline without opening a window and saves
one screenshot to the project root. It is intended for Codespaces or other headless
environments.

Usage:
    python frontend/headless_screenshot.py
"""

import os
import sys
from pathlib import Path

# Ensure the repository root is on sys.path for imports.
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(REPO_ROOT))

os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
from interface.spacezoo_api import SpaceZooAPI
from frontend.map_renderer import MapRenderer
from frontend.sprite_manager import SpriteManager
from frontend.ui_manager import UIManager


def main() -> None:
    pygame.init()

    renderer = MapRenderer()
    native_size = renderer.screen_size()
    game_surface = pygame.Surface(native_size)

    api = SpaceZooAPI()
    sprite_manager = SpriteManager()
    ui_manager = UIManager()

    renderer.draw_background(game_surface)

    state = api.get_zoo_state()
    sprite_manager.draw_entities(game_surface, state, renderer.tile_size)
    ui_manager.draw(game_surface, api, native_size[0], native_size[1])

    screenshot_path = REPO_ROOT / "codespaces_screenshot.png"
    pygame.image.save(game_surface, screenshot_path)
    print(f"Saved headless screenshot to: {screenshot_path}")

    pygame.quit()


if __name__ == "__main__":
    main()
