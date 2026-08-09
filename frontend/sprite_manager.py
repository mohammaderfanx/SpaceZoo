"""
Sprite manager for SpaceZoo frontend.
Renders placeholder rectangles for creatures, staff and visitors using the API state.
"""

import pygame
from typing import Dict, Any

from frontend.asset_loader import AssetLoader


class SpriteManager:
    """Manages sprite rendering for creatures, staff, visitors, and the player."""

    def __init__(self) -> None:
        # Colors as fallback
        self.creature_color = (200, 140, 40)
        self.staff_color = (40, 120, 200)
        self.visitor_color = (80, 200, 100)

        # Asset loader and animations cache
        self.loader = AssetLoader()
        self.player_anim = self.loader.load_animation("Ben(main)")
        self.visitor_anim = self.loader.load_animation("Visitor")
        self.creature_anims: Dict[str, Dict[str, list]] = {}

        # Per-entity animation state: id -> {dir, frame_idx, last_tick, last_pos}
        self.entity_state: Dict[str, Dict[str, Any]] = {}
        self.frame_duration_ms = 120

    def _get_entity_state(self, eid: str) -> Dict[str, Any]:
        st = self.entity_state.get(eid)
        if not st:
            st = {"dir": "right", "frame_idx": 0, "last_tick": pygame.time.get_ticks(), "last_pos": None}
            self.entity_state[eid] = st
        return st

    def _get_creature_animation(self, name: str) -> Dict[str, list]:
        if name not in self.creature_anims:
            self.creature_anims[name] = self.loader.load_animation(name)
        return self.creature_anims[name]

    def _draw_animated(self, screen: "pygame.Surface", surf_list: list, eid: str, pos: tuple, moving: bool, direction: str, tile_size: int) -> None:
        st = self._get_entity_state(eid)
        now = pygame.time.get_ticks()

        if direction:
            st["dir"] = direction

        frames = surf_list
        if moving:
            if now - st["last_tick"] >= self.frame_duration_ms:
                st["frame_idx"] = (st["frame_idx"] + 1) % len(frames)
                st["last_tick"] = now
        else:
            st["frame_idx"] = 0

        screen.blit(frames[st["frame_idx"]], (pos[0] * tile_size, pos[1] * tile_size))

    def draw_entities(self, screen: "pygame.Surface", state: Dict[str, Any], tile_size: int) -> None:
        """Draw creatures, staff, visitors and player from `state` onto the screen.

        Uses `AssetLoader` animation frames for named creatures and player sprites.
        """
        # Draw animals with their proper creature assets.
        for c in state.get("animals", []):
            pos = c.get("position", (0, 0))
            name = c.get("name", "")
            age_stage = c.get("age_stage", 1)
            eid = c.get("id", name)
            stage_sprite = self.loader.load_creature_stage(name, age_stage)
            st = self._get_entity_state(eid)
            last_pos = st.get("last_pos")
            moving = False
            direction = st.get("dir", "right")
            if last_pos:
                dx = pos[0] - last_pos[0]
                if dx < 0:
                    direction = "left"
                    moving = True
                elif dx > 0:
                    direction = "right"
                    moving = True
            st["last_pos"] = pos

            if moving:
                rect = pygame.Rect(pos[0] * tile_size, pos[1] * tile_size, tile_size, tile_size)
                screen.blit(stage_sprite, rect)
            else:
                screen.blit(stage_sprite, (pos[0] * tile_size, pos[1] * tile_size))

        # Draw staff (non-animated)
        for s in state.get("staff", []):
            pos = s.get("position", (0, 0))
            x, y = pos
            rect = pygame.Rect(x * tile_size + 6, y * tile_size + 6, tile_size - 12, tile_size - 12)
            pygame.draw.rect(screen, self.staff_color, rect)

        # Draw player (animated)
        player = state.get("player", {})
        pos = player.get("position")
        if pos:
            pressed = pygame.key.get_pressed()
            moving = False
            direction = self.entity_state.get("player", {}).get("dir", "right")
            if pressed[pygame.K_a]:
                direction = "left"
                moving = True
            elif pressed[pygame.K_d]:
                direction = "right"
                moving = True

            frames = self.player_anim.get(direction, self.player_anim.get("right"))
            if frames:
                self._draw_animated(screen, frames, "player", pos, moving, direction, tile_size)
            else:
                px, py = pos
                rect = pygame.Rect(px * tile_size, py * tile_size, tile_size, tile_size)
                pygame.draw.rect(screen, (255, 100, 100), rect)
