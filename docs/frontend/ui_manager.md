# UIManager and UIButton

```mermaid
classDiagram
    class UIButton {
        - label: str
        - base_label: str
        - action: Callable[[], Dict[str, Any]]
        - group_key: Optional[str]
        - rect: pygame.Rect
        + __init__(label: str, action: Callable[[], Dict[str, Any]], group_key: Optional[str] = None)
    }

    class UIManager {
        - font: pygame.font.Font|None
        - header_font: pygame.font.Font|None
        - title_font: pygame.font.Font|None
        - action_font: pygame.font.Font|None
        - bg_color: Tuple[int,int,int]
        - panel_color: Tuple[int,int,int]
        - card_color: Tuple[int,int,int]
        - accent_color: Tuple[int,int,int]
        - text_color: Tuple[int,int,int]
        - secondary_text: Tuple[int,int,int]
        - sidebar_width: int
        - topbar_height: int
        - message: str
        - message_timer: float
        - buttons: List[UIButton]
        - weather_options: List[str]
        - current_weather_index: int
        - shift_options: List[Tuple[int,int]]
        - current_shift_index: int
        - shift_button: UIButton|None
        - group_children: Dict[str, List[UIButton]]
        - expanded_group: Optional[str]
        - _visible_buttons: List[UIButton]
        - _scale: float
        - _offset: Tuple[int,int]
        + __init__()
        + update_viewport(scale: float, offset: Tuple[int,int]) : None
        + process_event(event: pygame.event.Event, api: SimZooAPI) : None
        + draw(screen: pygame.Surface, api: SimZooAPI, screen_width: int, screen_height: int) : None
        - _ensure_fonts() : None
        - _build_buttons() : None
        - _group_action(action: Callable[[], Dict[str, Any]]) : Callable[[], Dict[str, Any]]
        - _action_toggle_group(group_key: str) : Dict[str, Any]
        - _shift_label() : str
        - _action_cycle_shift() : Dict[str, Any]
        - _api_action(callback: Callable[[SimZooAPI], Dict[str, Any]]) : Dict[str, Any]
        - _draw_background(screen: pygame.Surface, width: int, height: int) : None
        - _draw_topbar(screen: pygame.Surface, state: Dict[str, Any], width: int) : None
        - _draw_sidebar(screen: pygame.Surface) : None
        - _draw_right_panel(screen: pygame.Surface, state: Dict[str, Any], screen_width: int, screen_height: int) : None
        - _draw_message_bar(screen: pygame.Surface, width: int, height: int) : None
    }

    UIManager --> UIButton
```

- `UIButton` represents a clickable sidebar button with an optional grouped sub-menu.
- `UIManager` builds the dashboard, handles input, and renders the UI panels for the frontend.
