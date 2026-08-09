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
from frontend.ui_manager import UIManager

NATIVE_SIZE = (1260, 960)


def main() -> None:
    pygame.init()

    native_size = NATIVE_SIZE
    game_surface = pygame.Surface(native_size)

    api = SpaceZooAPI()
    ui_manager = UIManager()

    ui_manager.draw(game_surface, api, native_size[0], native_size[1])

    screenshot_path = REPO_ROOT / "codespaces_screenshot.png"
    pygame.image.save(game_surface, screenshot_path)
    print(f"Saved headless screenshot to: {screenshot_path}")

    pygame.quit()


if __name__ == "__main__":
    main()
