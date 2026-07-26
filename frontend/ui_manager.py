"""
UI manager for SpaceZoo frontend.
Implements a collapsible taskbar at the bottom of the screen.
All data is fetched from `SpaceZooAPI`.
"""

import pygame
from typing import Any, Dict
from interface.spacezoo_api import SpaceZooAPI


class UIManager:
    """
    Verwaltet die einklappbare Taskbar. Wenn eingeklappt werden Quick-Stats gezeigt,
    wenn aufgeklappt das detaillierte Dashboard. Holt alle Daten ausschließlich über die API.
    """

    def __init__(self) -> None:
        self.collapsed = True
        self.font = None
        self.bg_color = (30, 30, 30)
        self.text_color = (230, 230, 230)
        self.quick_height = 48
        self.expanded_height = 220

    def _ensure_font(self) -> None:
        if self.font is None:
            try:
                self.font = pygame.font.SysFont(None, 20)
            except Exception:
                pygame.font.init()
                self.font = pygame.font.SysFont(None, 20)

    def process_event(self, event: "pygame.event.Event") -> None:
        """Toggle taskbar on TAB or 't' key.

        :param event: Pygame event
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB or event.key == pygame.K_t:
                self.collapsed = not self.collapsed

    def draw(self, screen: "pygame.Surface", api: SpaceZooAPI, screen_width: int, screen_height: int) -> None:
        """
        Draw the taskbar using data from the API.

        :param screen: Pygame surface
        :param api: SpaceZooAPI instance
        :param screen_width: width of screen in pixels
        :param screen_height: height of screen in pixels
        """
        self._ensure_font()

        if self.collapsed:
            rect = pygame.Rect(0, screen_height - self.quick_height, screen_width, self.quick_height)
            pygame.draw.rect(screen, self.bg_color, rect)

            # Get quick stats
            try:
                qs = api.get_quick_stats()
            except Exception:
                qs = {}

            money = qs.get("money", "-")
            phase = qs.get("day_phase", "-")
            time_rem = qs.get("time_remaining", "-")

            txt = f"Money: {money}   Phase: {phase}   Time left: {time_rem:.1f}s" if isinstance(time_rem, (int, float)) else f"Money: {money}   Phase: {phase}"
            surf = self.font.render(txt, True, self.text_color)
            screen.blit(surf, (8, screen_height - self.quick_height + 12))

        else:
            rect = pygame.Rect(0, screen_height - self.expanded_height, screen_width, self.expanded_height)
            pygame.draw.rect(screen, self.bg_color, rect)

            # Get detailed dashboard
            try:
                details = api.get_detailed_dashboard()
            except Exception:
                details = {}

            # Render top-left block of details
            x = 8
            y = screen_height - self.expanded_height + 8

            # Finances
            finances = details.get("finances", {})
            money = finances.get("money", "-")
            line = f"Money: {money}"
            screen.blit(self.font.render(line, True, self.text_color), (x, y))
            y += 22

            # Creatures summary
            screen.blit(self.font.render("Creatures:", True, self.text_color), (x, y))
            y += 18
            cs = details.get("creatures_summary", {})
            for species, info in cs.items():
                line = f"  {species}: {info.get('count',0)} count, avg hunger {info.get('avg_hunger',0):.1f}, sick {info.get('sick',0)}"
                screen.blit(self.font.render(line, True, self.text_color), (x, y))
                y += 18

            # Visitors summary
            y2 = screen_height - self.expanded_height + 8
            x2 = screen_width // 2
            screen.blit(self.font.render("Visitors:", True, self.text_color), (x2, y2))
            y2 += 18
            vs = details.get("visitors_summary", {})
            for k, v in vs.items():
                line = f"  {k}: {v}"
                screen.blit(self.font.render(line, True, self.text_color), (x2, y2))
                y2 += 18

            # Staff summary
            y3 = screen_height - self.expanded_height + 8
            x3 = (screen_width // 2) + 220
            screen.blit(self.font.render("Staff:", True, self.text_color), (x3, y3))
            y3 += 18
            ss = details.get("staff_summary", {})
            for sid, info in ss.items():
                line = f"  {info.get('type','?')}: {info.get('status','?')}"
                screen.blit(self.font.render(line, True, self.text_color), (x3, y3))
                y3 += 18
