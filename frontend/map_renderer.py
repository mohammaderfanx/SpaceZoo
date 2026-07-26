"""
Map renderer for SpaceZoo frontend.
Draws a simple 21x16 grid using Pygame. No backend imports here.
"""

import pygame
from typing import Tuple

from frontend.asset_loader import AssetLoader


class MapRenderer:
    def __init__(self, grid_width: int = 21, grid_height: int = 16, tile_size: int = 60) -> None:
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.tile_size = tile_size

        # Colors
        self.bg_color = (200, 230, 200)
        self.line_color = (50, 50, 50)
        self.tile_color = (180, 200, 180)

    def draw_grid(self, screen: "pygame.Surface") -> None:
        """Draws the grid to the provided Pygame surface."""
        screen.fill(self.bg_color)

        for y in range(self.grid_height):
            for x in range(self.grid_width):
                rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                pygame.draw.rect(screen, self.tile_color, rect)
                pygame.draw.rect(screen, self.line_color, rect, 1)

    def draw_background(self, screen: "pygame.Surface") -> None:
        """Draws the background map using AssetLoader. Falls Laden fehlschlägt, wird das Grid gezeichnet."""
        try:
            loader = AssetLoader()
            map_surf = loader.load_map()
            # Blit the map at (0,0)
            screen.blit(map_surf, (0, 0))
        except Exception:
            # Fallback to grid
            self.draw_grid(screen)

    def screen_size(self) -> Tuple[int, int]:
        return (self.grid_width * self.tile_size, self.grid_height * self.tile_size)
