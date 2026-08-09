"""
UI manager for SpaceZoo frontend.
Implements the main dashboard and sidebar controls.
All data is fetched from `SpaceZooAPI`.
"""

import pygame
from typing import Any, Callable, Dict, List, Optional, Tuple
from interface.spacezoo_api import SpaceZooAPI


class UIButton:
    """Represents a clickable dashboard button with an action callback.

    `group_key` marks a button as a group toggle (e.g. "Buy Animal"): clicking it
    expands/collapses the matching entry in `UIManager.group_children` instead of
    performing a zoo action directly.
    """

    def __init__(self, label: str, action: Callable[[], Dict[str, Any]], group_key: Optional[str] = None):
        self.label = label
        self.base_label = label
        self.action = action
        self.group_key = group_key
        self.rect = pygame.Rect(0, 0, 0, 0)


class UIManager:
    """Render and handle the SpaceZoo frontend dashboard UI."""

    def __init__(self) -> None:
        self.font: pygame.font.Font | None = None
        self.header_font: pygame.font.Font | None = None
        self.title_font: pygame.font.Font | None = None
        self.action_font: pygame.font.Font | None = None
        self.bg_color = (16, 20, 32)
        self.panel_color = (24, 34, 60)
        self.card_color = (34, 48, 82)
        self.accent_color = (86, 192, 255)
        self.text_color = (230, 230, 230)
        self.secondary_text = (180, 190, 210)
        self.sidebar_width = 280
        self.topbar_height = 110
        self.message: str = "Welcome to SpaceZoo UI Preview"
        self.message_timer = 0.0
        self.buttons: List[UIButton] = []
        self.weather_options = ["SUNNY", "CLOUDY", "RAINY"]
        self.current_weather_index = 0
        self.shift_options = [(6, 14), (8, 16), (8, 18), (14, 22), (22, 6)]
        self.current_shift_index = 2
        self.shift_button: UIButton | None = None
        self.group_children: Dict[str, List[UIButton]] = {}
        self.expanded_group: Optional[str] = None
        self._visible_buttons: List[UIButton] = []
        self._scale = 1.0
        self._offset = (0, 0)
        self._build_buttons()

    def update_viewport(self, scale: float, offset: Tuple[int, int]) -> None:
        """Records how the native render surface is currently scaled/offset onto the window.

        Mouse events arrive in window pixel coordinates, but button rects are laid out in
        native surface coordinates, so clicks must be mapped back through this transform
        before hit-testing.
        """
        self._scale = scale if scale else 1.0
        self._offset = offset

    def _ensure_fonts(self) -> None:
        if self.font is None:
            pygame.font.init()
            self.font = pygame.font.SysFont(None, 18)
            self.header_font = pygame.font.SysFont(None, 24, bold=True)
            self.title_font = pygame.font.SysFont(None, 30, bold=True)
            self.action_font = pygame.font.SysFont(None, 20, bold=True)

    def _build_buttons(self) -> None:
        self.shift_button = UIButton(self._shift_label(), self._action_cycle_shift)

        self.group_children = {
            "animal": [
                UIButton("Eagle", self._group_action(lambda: self._action_buy_animal("Eagle"))),
                UIButton("Wolf", self._group_action(lambda: self._action_buy_animal("Wolf"))),
                UIButton("Rabbit", self._group_action(lambda: self._action_buy_animal("Rabbit"))),
            ],
            "food": [
                UIButton("Meat", self._group_action(lambda: self._action_buy_food("Meat"))),
                UIButton("Hay", self._group_action(lambda: self._action_buy_food("Hay"))),
                UIButton("Fish", self._group_action(lambda: self._action_buy_food("Fish"))),
            ],
            "staff": [
                UIButton("Caretaker", self._group_action(lambda: self._action_hire_staff("Caretaker"))),
                UIButton("Vet", self._group_action(lambda: self._action_hire_staff("Vet"))),
                UIButton("Cashier", self._group_action(lambda: self._action_hire_staff("Cashier"))),
            ],
        }

        self.buttons = [
            UIButton("Advance Tick", self._action_advance_tick),
            UIButton("Buy Animal", lambda: self._action_toggle_group("animal"), group_key="animal"),
            UIButton("Sell Animal", self._action_sell_animal),
            UIButton("Buy Food", lambda: self._action_toggle_group("food"), group_key="food"),
            UIButton("Buy Medicine", self._action_buy_medicine),
            self.shift_button,
            UIButton("Hire Staff", lambda: self._action_toggle_group("staff"), group_key="staff"),
            UIButton("Fire Staff", self._action_fire_staff),
            UIButton("Feed Animal", self._action_feed_animal),
            UIButton("Heal Animal", self._action_heal_animal),
            UIButton("Clean Enclosure", self._action_clean_enclosure),
            UIButton("Toggle Weather", self._action_toggle_weather),
        ]
        self._visible_buttons = list(self.buttons)

    def _group_action(self, action: Callable[[], Dict[str, Any]]) -> Callable[[], Dict[str, Any]]:
        """Wraps a sub-menu action so picking it also collapses the menu back."""
        def wrapped() -> Dict[str, Any]:
            result = action()
            self.expanded_group = None
            return result
        return wrapped

    def _action_toggle_group(self, group_key: str) -> Dict[str, Any]:
        if self.expanded_group == group_key:
            self.expanded_group = None
            return {"success": True, "message": "Menu closed."}
        self.expanded_group = group_key
        return {"success": True, "message": "Choose an option below."}

    def _shift_label(self) -> str:
        start, end = self.shift_options[self.current_shift_index]
        return f"Shift: {start:02d}:00-{end:02d}:00"

    def _action_cycle_shift(self) -> Dict[str, Any]:
        self.current_shift_index = (self.current_shift_index + 1) % len(self.shift_options)
        self.shift_button.label = self._shift_label()
        start, end = self.shift_options[self.current_shift_index]
        return {"success": True, "message": f"New hires will work {start:02d}:00-{end:02d}:00."}

    def _action_advance_tick(self) -> Dict[str, Any]:
        return self._api_action(lambda api: api.advance_tick())

    def _action_buy_animal(self, species: str) -> Dict[str, Any]:
        return self._api_action(lambda api: api.buy_animal(species))

    def _action_buy_food(self, food_type: str) -> Dict[str, Any]:
        return self._api_action(lambda api: api.buy_food(food_type, 5))

    def _action_hire_staff(self, staff_type: str) -> Dict[str, Any]:
        start, end = self.shift_options[self.current_shift_index]
        return self._api_action(lambda api: api.hire_staff(staff_type, start, end))

    def _action_sell_animal(self) -> Dict[str, Any]:
        return self._api_action(lambda api: api.sell_animal())

    def _action_buy_medicine(self) -> Dict[str, Any]:
        return self._api_action(lambda api: api.buy_medicine("Antibiotic", 1))

    def _action_fire_staff(self) -> Dict[str, Any]:
        return self._api_action(lambda api: api.fire_staff())

    def _action_feed_animal(self) -> Dict[str, Any]:
        return self._api_action(lambda api: api.feed_animal())

    def _action_heal_animal(self) -> Dict[str, Any]:
        return self._api_action(lambda api: api.heal_animal())

    def _action_clean_enclosure(self) -> Dict[str, Any]:
        return self._api_action(lambda api: api.clean_enclosure())

    def _action_toggle_weather(self) -> Dict[str, Any]:
        return self._api_action(lambda api: api.change_weather(self.weather_options[self.current_weather_index]))

    def _api_action(self, callback: Callable[[SpaceZooAPI], Dict[str, Any]]) -> Dict[str, Any]:
        try:
            result = callback(self._api_reference)
            return {
                "success": result.get("success", False),
                "message": result.get("message", "Action completed."),
            }
        except Exception as exc:
            return {"success": False, "message": f"Action failed: {exc}"}

    def process_event(self, event: "pygame.event.Event", api: SpaceZooAPI) -> None:
        """Handle user input events for dashboard buttons and UI interactions."""
        self._ensure_fonts()
        self._api_reference = api
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            native_pos = (
                (event.pos[0] - self._offset[0]) / self._scale,
                (event.pos[1] - self._offset[1]) / self._scale,
            )
            for button in self._visible_buttons:
                if button.rect.collidepoint(native_pos):
                    result = button.action()
                    self.message = result.get("message", "Action executed.")
                    self.message_timer = 3.0
                    if button.label == "Toggle Weather" and result.get("success", False):
                        self.current_weather_index = (self.current_weather_index + 1) % len(self.weather_options)
                    break
        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            self.message = "Press buttons to control the zoo."
            self.message_timer = 2.0

    def draw(self, screen: "pygame.Surface", api: SpaceZooAPI, screen_width: int, screen_height: int) -> None:
        """Render the dashboard overlay and its panels on the game screen."""
        self._ensure_fonts()
        panel_state = api.get_panel_state()
        self._draw_background(screen, screen_width, screen_height)
        self._draw_topbar(screen, panel_state, screen_width)
        self._draw_sidebar(screen)
        self._draw_right_panel(screen, panel_state, screen_width, screen_height)
        self._draw_message_bar(screen, screen_width, screen_height)

    def _draw_background(self, screen: "pygame.Surface", width: int, height: int) -> None:
        screen.fill(self.bg_color)

    def _draw_topbar(self, screen: "pygame.Surface", state: Dict[str, Any], width: int) -> None:
        rect = pygame.Rect(0, 0, width, self.topbar_height)
        pygame.draw.rect(screen, self.panel_color, rect)
        pygame.draw.line(screen, self.accent_color, (0, self.topbar_height - 2), (width, self.topbar_height - 2), 2)

        self._draw_card(screen, 16, 16, 280, 76, "Day", f"{state['elapsed_days']} · {state['elapsed_hours']:02d}:00")
        self._draw_card(screen, 316, 16, 280, 76, "Budget", f"${state['money']}")
        self._draw_card(screen, 616, 16, 280, 76, "Score", f"{state['score']:.1f}")
        self._draw_card(screen, 916, 16, 280, 76, "Visitors", f"{state['visitors']}")

    def _draw_card(self, screen: "pygame.Surface", x: int, y: int, w: int, h: int, title: str, value: str) -> None:
        card = pygame.Rect(x, y, w, h)
        pygame.draw.rect(screen, self.card_color, card, border_radius=8)
        pygame.draw.rect(screen, self.accent_color, card, 2, border_radius=8)
        screen.blit(self.font.render(title, True, self.secondary_text), (x + 12, y + 10))
        screen.blit(self.header_font.render(value, True, self.text_color), (x + 12, y + 36))

    def _draw_sidebar(self, screen: "pygame.Surface") -> None:
        x = 0
        y = self.topbar_height
        rect = pygame.Rect(x, y, self.sidebar_width, screen.get_height() - y)
        pygame.draw.rect(screen, self.panel_color, rect)

        title = self.title_font.render("Space Zoo", True, self.accent_color)
        screen.blit(title, (x + 16, y + 16))
        subtitle = self.font.render("Dashboard", True, self.secondary_text)
        screen.blit(subtitle, (x + 16, y + 16 + 34))

        button_y = y + 78
        button_height = 42
        child_height = 36
        button_width = self.sidebar_width - 32
        child_width = button_width - 20
        self._visible_buttons = []

        for button in self.buttons:
            if button.group_key is not None:
                marker = "-" if self.expanded_group == button.group_key else "+"
                button.label = f"{marker} {button.base_label}"

            button.rect = pygame.Rect(x + 16, button_y, button_width, button_height)
            pygame.draw.rect(screen, self.card_color, button.rect, border_radius=10)
            pygame.draw.rect(screen, self.accent_color, button.rect, 1, border_radius=10)
            label = self.action_font.render(button.label, True, self.text_color)
            screen.blit(label, (button.rect.x + 16, button.rect.y + 10))
            self._visible_buttons.append(button)
            button_y += button_height + 8

            if button.group_key is not None and self.expanded_group == button.group_key:
                for child in self.group_children[button.group_key]:
                    child.rect = pygame.Rect(x + 36, button_y, child_width, child_height)
                    pygame.draw.rect(screen, (28, 40, 68), child.rect, border_radius=8)
                    pygame.draw.rect(screen, self.accent_color, child.rect, 1, border_radius=8)
                    child_label = self.font.render(child.label, True, self.text_color)
                    screen.blit(child_label, (child.rect.x + 14, child.rect.y + 9))
                    self._visible_buttons.append(child)
                    button_y += child_height + 6
                button_y += 4

    def _draw_right_panel(self, screen: "pygame.Surface", state: Dict[str, Any], screen_width: int, screen_height: int) -> None:
        panel_x = self.sidebar_width + 16
        panel_y = self.topbar_height + 16
        panel_w = screen_width - panel_x - 16
        panel_h = screen_height - panel_y - 80
        panel = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
        pygame.draw.rect(screen, self.panel_color, panel, border_radius=12)
        pygame.draw.rect(screen, self.accent_color, panel, 2, border_radius=12)

        title = self.header_font.render("Zoo Overview", True, self.text_color)
        screen.blit(title, (panel_x + 18, panel_y + 14))

        content_x = panel_x + 18
        content_y = panel_y + 52
        content_w = panel_w - 36

        left_w = int(content_w * 0.62)
        right_w = content_w - left_w - 16

        animals_box_h = 220
        self._draw_data_table(
            screen,
            content_x,
            content_y,
            left_w,
            animals_box_h,
            "Animals",
            ["Name", "Age", "Hunger", "Health", "Energy", "Status", "Sex"],
            [
                [
                    a["name"],
                    str(a["age_days"]),
                    f"{a['hunger']:.0f}%",
                    f"{a['health'] * 100:.0f}%",
                    f"{a['energy'] * 100:.0f}%",
                    a["illness"] if a["is_sick"] else ("Hungry" if a["hunger"] >= 50 else "Healthy"),
                    a["gender"].capitalize(),
                ]
                for a in state["animals"][:5]
            ],
        )

        self._draw_data_table(
            screen,
            content_x + left_w + 16,
            content_y,
            right_w,
            animals_box_h,
            "Enclosures",
            ["#", "Capacity", "Cleanliness", "Animals", "Diet"],
            [
                [
                    str(e["number"]),
                    f"{e['capacity']}",
                    f"{e['cleanliness'] * 100:.0f}%",
                    f"{e['animal_count']}",
                    e["diet"],
                ]
                for e in state["enclosures"][:5]
            ],
        )

        staff_box_y = content_y + animals_box_h + 16
        staff_box_h = 170
        self._draw_data_table(
            screen,
            content_x,
            staff_box_y,
            left_w,
            staff_box_h,
            "Personnel",
            ["Type", "Status", "Working hours"],
            [
                [
                    s["type"],
                    s["status"],
                    f"{s['working_hours'][0]:02d}:00-{s['working_hours'][1]:02d}:00",
                ]
                for s in state["staff"][:5]
            ],
        )

        self._draw_data_table(
            screen,
            content_x + left_w + 16,
            staff_box_y,
            right_w,
            staff_box_h,
            "Inventory",
            ["Item", "Amount"],
            [[key, str(value)] for key, value in list(state["inventory"].items())[:8]],
        )

        bottom_y = staff_box_y + staff_box_h + 16
        card_w = int((content_w - 16) / 2)
        self._draw_info_block(screen, content_x, bottom_y, "Environment", [
            f"Weather: {state['environment']['weather']}",
            f"Temp: {state['environment']['temperature']}°C",
            f"Wind: {state['environment']['windSpeed']} km/h",
            f"Attraction: {state['environment']['attractiveness']:.2f}",
        ], card_w, 120)

        self._draw_info_block(screen, content_x + card_w + 16, bottom_y, "System Info", [
            f"Visitors: {state['visitors']}",
            "Next Tick: +10s",
        ], card_w, 120)

    def _fit_text(self, text: str, max_width: int) -> str:
        """Truncates text with an ellipsis so it never overflows into the next column."""
        if self.font.size(text)[0] <= max_width:
            return text
        trimmed = text
        while trimmed and self.font.size(trimmed + "...")[0] > max_width:
            trimmed = trimmed[:-1]
        return f"{trimmed}..." if trimmed else "..."

    def _draw_data_table(
        self,
        screen: "pygame.Surface",
        x: int,
        y: int,
        width: int,
        height: int,
        title: str,
        headers: List[str],
        rows: List[List[str]],
    ) -> None:
        block = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, self.card_color, block, border_radius=10)
        pygame.draw.rect(screen, self.accent_color, block, 1, border_radius=10)
        screen.blit(self.font.render(title, True, self.text_color), (x + 12, y + 10))

        header_y = y + 34
        header_height = 26
        header_rect = pygame.Rect(x + 12, header_y, width - 24, header_height)
        pygame.draw.rect(screen, (20, 34, 70), header_rect, border_radius=6)
        col_count = len(headers)
        col_width = (width - 24) // col_count if col_count else width - 24
        for index, header in enumerate(headers):
            screen.blit(self.font.render(header, True, self.secondary_text), (x + 12 + index * col_width, header_y + 4))

        row_y = header_y + header_height + 8
        max_rows = min(len(rows), max(1, (height - 68) // 24))
        for row_index in range(max_rows):
            row = rows[row_index]
            row_rect = pygame.Rect(x + 12, row_y - 2, width - 24, 24)
            if row_index % 2 == 0:
                pygame.draw.rect(screen, (24, 40, 78), row_rect)
            for col_index, cell in enumerate(row[:col_count]):
                is_last_col = col_index == col_count - 1
                available = (width - 24 - col_index * col_width) if is_last_col else col_width
                fitted = self._fit_text(cell, available - 8)
                screen.blit(self.font.render(fitted, True, self.text_color), (x + 12 + col_index * col_width, row_y))
            row_y += 24

    def _draw_info_block(self, screen: "pygame.Surface", x: int, y: int, title: str, lines: List[str], width: int = 240, height: int = 100) -> None:
        block = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, self.card_color, block, border_radius=10)
        pygame.draw.rect(screen, self.accent_color, block, 1, border_radius=10)
        screen.blit(self.font.render(title, True, self.text_color), (x + 12, y + 10))
        text_y = y + 34
        for line in lines:
            screen.blit(self.font.render(line, True, self.secondary_text), (x + 12, text_y))
            text_y += 20

    def _draw_message_bar(self, screen: "pygame.Surface", width: int, height: int) -> None:
        if self.message_timer > 0:
            self.message_timer -= 1 / 30
        bar_height = 36
        rect = pygame.Rect(0, height - bar_height, width, bar_height)
        pygame.draw.rect(screen, (20, 28, 46), rect)
        msg = self.font.render(self.message, True, self.text_color)
        screen.blit(msg, (16, height - bar_height + 8))
