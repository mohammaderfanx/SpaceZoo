"""
author: Mohammad Rezaei
date: 08.08.2026
version: 1

AssetLoader (Singleton) for the frontend.

This module provides image loading, caching, and scaling for the Pygame frontend.
It returns placeholder surfaces when asset files are missing or fail to load.

Note: According to ARCHITECTURE.md, frontend code must not import backend or database modules directly.
"""

from __future__ import annotations

import pygame
from pathlib import Path
from typing import Dict, Optional, Tuple


class AssetLoader:
    """Singleton asset manager that loads and caches images for the frontend."""
    _instance: Optional["AssetLoader"] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, assets_root: Optional[Path] = None) -> None:
        if getattr(self, "_initialized", False):
            return

        # Ensure pygame is initialized for image operations
        if not pygame.get_init():
            pygame.init()

        self.assets_root = Path(assets_root) if assets_root else Path(__file__).parent / "assets"
        self.cache: Dict[str, pygame.Surface] = {}

        # Default sizes from ARCHITECTURE.md
        self.map_size: Tuple[int, int] = (1260, 960)
        self.tile_size: Tuple[int, int] = (60, 60)

        self._initialized = True

    def _placeholder_surface(self, size: Tuple[int, int], color: Tuple[int, int, int]) -> pygame.Surface:
        surf = pygame.Surface(size)
        surf.fill(color)
        # draw border
        pygame.draw.rect(surf, (0, 0, 0), surf.get_rect(), 2)
        return surf

    def load_image(self, path: Path, size: Optional[Tuple[int, int]] = None) -> pygame.Surface:
        """
        Loads and scales an image, caching the result.

        :param path: The path to the image file
        :param size: Optional desired size (width, height)
        :return: Pygame Surface
        """
        key = f"{path}:{size}"
        if key in self.cache:
            return self.cache[key]

        try:
            # Load image
            surf = pygame.image.load(str(path)).convert_alpha()
            if size is not None:
                surf = pygame.transform.smoothscale(surf, size)
            self.cache[key] = surf
            return surf
        except Exception:
            # Return placeholder on error
            placeholder = self._placeholder_surface(size or (64, 64), (180, 50, 50))
            self.cache[key] = placeholder
            return placeholder

    def load_map(self) -> pygame.Surface:
        """Loads the zoo map image and scales it to the native screen size.

        Returns:
            pygame.Surface: The loaded and scaled map surface, or a placeholder if the file is missing.

        Tests:
            map file exists -> returns an image surface sized 1260x960
            map file missing -> returns a generated placeholder surface
        """
        map_dir = self.assets_root / "map"
        # try common extensions
        candidates = list(map_dir.glob("SimZooBase.*")) if map_dir.exists() else []
        if candidates:
            path = candidates[0]
            return self.load_image(path, self.map_size)

        # fallback placeholder
        return self._placeholder_surface(self.map_size, (100, 120, 140))

    def load_creature(self, name: str) -> pygame.Surface:
        """Loads a creature sprite image by name and scales it to tile size.

        Args:
            name: Creature asset name without file extension.

        Returns:
            pygame.Surface: The loaded creature sprite or a placeholder surface.

        Tests:
            exact file exists -> returns the expected sprite surface
            no matching file exists -> returns a placeholder surface
        """
        creatures_dir = self.assets_root / "creatures"
        # search for files matching name.*
        if creatures_dir.exists():
            candidates = list(creatures_dir.glob(f"{name}.*"))
            if candidates:
                return self.load_image(candidates[0], self.tile_size)

        # fallback: try lowercase name
        if creatures_dir.exists():
            candidates = list(creatures_dir.glob(f"{name.lower()}.*"))
            if candidates:
                return self.load_image(candidates[0], self.tile_size)

        # final fallback: colored square
        return self._placeholder_surface(self.tile_size, (200, 140, 40))

    def _find_creature_folder(self, name: str) -> Optional[Path]:
        creatures_dir = self.assets_root / "creatures"
        if not creatures_dir.exists():
            return None
        for candidate in creatures_dir.iterdir():
            if candidate.is_dir() and candidate.name.lower() == name.lower():
                return candidate
        return None

    def _try_extract_stage(self, stem: str) -> Optional[int]:
        import re
        match = re.search(r"(\d+)$", stem)
        if match:
            return int(match.group(1))
        return None

    def load_creature_stage_images(self, name: str) -> Dict[int, pygame.Surface]:
        """Loads lifecycle stage images for a creature.

        The method expects files named like 'name 1.png', 'name 2.png', 'name 3.png'
        inside the creature subfolder.

        Returns:
            Dict[int, pygame.Surface]: Mapping from stage index 1..3 to surfaces.

        Tests:
            all three stage files exist -> returns a dict with keys 1, 2, 3
            missing stage file -> missing stage is filled with closest existing image
        """
        folder = self._find_creature_folder(name)
        if not folder:
            return {}

        images: Dict[int, pygame.Surface] = {}
        for path in sorted(folder.iterdir()):
            if not path.is_file():
                continue
            stage = self._try_extract_stage(path.stem)
            if stage in (1, 2, 3):
                images[stage] = self.load_image(path, self.tile_size)

        if not images:
            return {}

        for stage in range(1, 4):
            if stage not in images:
                images[stage] = images[max(images.keys())]

        return images

    def load_creature_stage(self, name: str, stage: int) -> pygame.Surface:
        """Loads the sprite image for a creature at a given lifecycle stage.

        Args:
            name: creature folder name
            stage: stage number 1..3 representing early, middle, or late life

        Returns:
            pygame.Surface: corresponding stage sprite or fallback image

        Tests:
            valid stage with asset -> returns correct stage surface
            invalid stage number -> clamps to a valid stage and returns surface
        """
        stage = max(1, min(3, stage))
        images = self.load_creature_stage_images(name)
        if images:
            return images.get(stage, images.get(1))
        return self.load_creature(name)

    def load_animation(self, name: str, directions: Tuple[str, str] = ("right", "left")) -> Dict[str, list]:
        """
        Loads animation frames for an entity from a named folder or file prefix.

        Expected structures (in descending priority):
        - assets/creatures/{name}/ (contains files like right_1.png, right_2.png, left_1.png...)
        - assets/creatures/{name}_right_*.png and {name}_left_*.png
        - assets/creatures/{name}.* (fallback to a static image)

        Returns: Dict with one key per direction, each value is a list of Surfaces.
        """
        result: Dict[str, list] = {d: [] for d in directions}
        creatures_dir = self.assets_root / "creatures"

        # 1) Check for folder
        folder = creatures_dir / name
        if folder.exists() and folder.is_dir():
            # gather files and group by direction keyword
            imgs = sorted([p for p in folder.iterdir() if p.is_file()])
            for p in imgs:
                stem = p.stem.lower()
                for d in directions:
                    if d in stem:
                        result[d].append(self.load_image(p, self.tile_size))
            # if still empty, use any files sequentially split in half
            all_imgs = [self.load_image(p, self.tile_size) for p in imgs]
            if all_imgs and not any(result.values()):
                half = max(1, len(all_imgs) // 2)
                result[directions[0]] = all_imgs[:half]
                result[directions[1]] = all_imgs[half:half*2] or [all_imgs[0]]
            return result

        # 2) Look for prefixed files in creatures_dir
        if creatures_dir.exists():
            for d in directions:
                candidates = sorted(creatures_dir.glob(f"{name}*{d}*.*"))
                if candidates:
                    result[d] = [self.load_image(p, self.tile_size) for p in candidates]

        # 3) Try files named {name}_right.*, {name}_left.*
        if any(not v for v in result.values()) and creatures_dir.exists():
            for d in directions:
                candidates = sorted(creatures_dir.glob(f"{name}_{d}*.*"))
                if candidates:
                    result[d] = [self.load_image(p, self.tile_size) for p in candidates]

        # 4) Fallback to single static image for both directions
        if not any(result.values()):
            static = self.load_creature(name)
            for d in directions:
                result[d] = [static]

        # Ensure at least one frame per direction
        for d in directions:
            if not result[d]:
                result[d] = [self._placeholder_surface(self.tile_size, (150, 150, 150))]

        return result

    def load_all_creatures(self) -> Dict[str, pygame.Surface]:
        """
        Loads and caches all images under `assets/creatures/` and scales them.

        :return: Dict mapping basename (without extension) to Surface
        """
        result: Dict[str, pygame.Surface] = {}
        creatures_dir = self.assets_root / "creatures"
        if not creatures_dir.exists():
            return result

        for p in creatures_dir.iterdir():
            if p.is_file():
                name = p.stem
                result[name] = self.load_image(p, self.tile_size)

        return result
