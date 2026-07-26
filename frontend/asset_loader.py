"""
AssetLoader (Singleton) für das Frontend.

Funktionen:
- Lädt Bilder mit Pygame
- Cacht geladene Surfaces im RAM
- Skaliert die Map auf 1260x960
- Skaliert Kreaturen/Charaktere auf 60x60
- Gibt bei Ladefehlern ein farbiges Ersatz-Surface zurück

Beachte: Frontend darf laut ARCHITECTURE.md NICHT direkt Backend- oder Database-Module importieren.
"""

from __future__ import annotations

import pygame
from pathlib import Path
from typing import Dict, Optional, Tuple


class AssetLoader:
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
        Lädt und skaliert ein Bild. Cacht das Ergebnis.

        :param path: Pfad zur Bilddatei
        :param size: Optional gewünschte Größe (width, height)
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
        """
        Sucht die Map-Datei unter `assets/map/SpaceZooBase.*` und skaliert sie auf 1260x960.
        Falls nicht vorhanden, wird ein Ersatz-Surface zurückgegeben.
        """
        map_dir = self.assets_root / "map"
        # try common extensions
        candidates = list(map_dir.glob("SpaceZooBase.*")) if map_dir.exists() else []
        if candidates:
            path = candidates[0]
            return self.load_image(path, self.map_size)

        # fallback placeholder
        return self._placeholder_surface(self.map_size, (100, 120, 140))

    def load_creature(self, name: str) -> pygame.Surface:
        """
        Lädt ein Creature-Sprite aus `assets/creatures/` mit dem gegebenen Namen (ohne Erweiterung)
        und skaliert es auf 60x60. Bei Fehlern wird ein Platzhalter zurückgegeben.
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

    def load_animation(self, name: str, directions: Tuple[str, str] = ("right", "left")) -> Dict[str, list]:
        """
        Lädt Animationsframes für ein Entity mit Namensordner oder Namenspräfix.

        Erwartete Strukturen (in Reihenfolge der Priorität):
        - assets/creatures/{name}/ (enthält files, z.B. right_1.png, right_2.png, left_1.png...)
        - assets/creatures/{name}_right_*.png und {name}_left_*.png
        - assets/creatures/{name}.* (Fallback zu statischem Bild)

        Rückgabe: Dict mit Keys für jede Richtung, Wert ist Liste von Surfaces (mindestens 1).
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
        Lädt und cached alle Bilder unter `assets/creatures/` und skaliert sie.
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
