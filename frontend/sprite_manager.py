"""
Sprite manager for SpaceZoo frontend.
Renders placeholder rectangles for creatures, staff and visitors using the API state.
"""

import pygame
from typing import Dict, Any

from frontend.asset_loader import AssetLoader


class SpriteManager:
    def __init__(self) -> None:
        # Colors as fallback
        self.creature_color = (200, 140, 40)
        self.staff_color = (40, 120, 200)
        self.visitor_color = (80, 200, 100)

        # Asset loader and animations cache
        self.loader = AssetLoader()
        # Load animations for main player (Ben) and Visitor
        self.player_anim = self.loader.load_animation("Ben(main)")
        self.visitor_anim = self.loader.load_animation("Visitor")

        # Per-entity animation state: id -> {dir, frame_idx, last_tick, last_pos}
        self.entity_state: Dict[str, Dict[str, Any]] = {}
        # Frame duration in ms
        self.frame_duration_ms = 120

    def _get_entity_state(self, eid: str) -> Dict[str, Any]:
        st = self.entity_state.get(eid)
        if not st:
            st = {"dir": "right", "frame_idx": 0, "last_tick": pygame.time.get_ticks(), "last_pos": None}
            self.entity_state[eid] = st
        return st

    def _draw_animated(self, screen: "pygame.Surface", surf_list: list, eid: str, pos: tuple, moving: bool, direction: str, tile_size: int) -> None:
        st = self._get_entity_state(eid)
        now = pygame.time.get_ticks()

        # Update direction
        if direction:
            st["dir"] = direction

        frames = surf_list
        # If moving, advance frames over time
        if moving:
            if now - st["last_tick"] >= self.frame_duration_ms:
                st["frame_idx"] = (st["frame_idx"] + 1) % len(frames)
                st["last_tick"] = now
        else:
            # standing: show first frame
            st["frame_idx"] = 0

        frame = frames[st["frame_idx"]]
        x, y = pos
        screen.blit(frame, (x * tile_size, y * tile_size))

    def draw_entities(self, screen: "pygame.Surface", state: Dict[str, Any], tile_size: int) -> None:
        """Draw creatures, staff, visitors and player from `state` onto the screen.

        Uses `AssetLoader` animation frames for `Ben(main)` (player) and `Visitor`.
        """
        # Draw creatures (non-animated)
        for c in state.get("creatures", []):
            pos = c.get("position", (0, 0))
            x, y = pos
            rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
            pygame.draw.rect(screen, self.creature_color, rect)

        # Draw staff (non-animated)
        for s in state.get("staff", []):
            pos = s.get("position", (0, 0))
            x, y = pos
            rect = pygame.Rect(x * tile_size + 6, y * tile_size + 6, tile_size - 12, tile_size - 12)
            pygame.draw.rect(screen, self.staff_color, rect)

        # Draw visitors (animated)
        for v in state.get("visitors", []):
            eid = v.get("id") or f"visitor_{id(v)}"
            pos = v.get("position", (0, 0))
            last_pos = self.entity_state.get(eid, {}).get("last_pos")
            moving = False
            direction = "right"
            if last_pos:
                dx = pos[0] - last_pos[0]
                if dx < 0:
                    direction = "left"
                    moving = dx != 0
                elif dx > 0:
                    direction = "right"
                    moving = dx != 0
                else:
                    moving = False
            else:
                # If we have no history but status suggests movement, treat as standing
                moving = False

            # update last_pos
            st = self._get_entity_state(eid)
            st["last_pos"] = pos

            # pick animation frames
            frames = self.visitor_anim.get(direction, self.visitor_anim.get("right"))
            if not frames:
                # fallback rectangle
                x, y = pos
                rect = pygame.Rect(x * tile_size + 12, y * tile_size + 12, tile_size - 24, tile_size - 24)
                pygame.draw.rect(screen, self.visitor_color, rect)
            else:
                self._draw_animated(screen, frames, eid, pos, moving, direction, tile_size)

        # Draw player (animated)
        player = state.get("player", {})
        pos = player.get("position")
        if pos:
            # Determine movement/direction from pressed keys
            pressed = pygame.key.get_pressed()
            moving = False
            direction = self.entity_state.get("player", {}).get("dir", "right")
            if pressed[pygame.K_a]:
                direction = "left"
                moving = True
            elif pressed[pygame.K_d]:
                direction = "right"
                moving = True
            else:
                moving = False

            # Use player_anim frames based on direction
            frames = self.player_anim.get(direction, self.player_anim.get("right"))
            if not frames:
                px, py = pos
                rect = pygame.Rect(px * tile_size, py * tile_size, tile_size, tile_size)
                pygame.draw.rect(screen, (255, 100, 100), rect)
            else:
                self._draw_animated(screen, frames, "player", pos, moving, direction, tile_size)
