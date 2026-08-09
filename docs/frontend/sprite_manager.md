# SpriteManager

```mermaid
classDiagram
    class SpriteManager {
        - creature_color: Tuple[int,int,int]
        - staff_color: Tuple[int,int,int]
        - visitor_color: Tuple[int,int,int]
        - loader: AssetLoader
        - player_anim: Dict[str, list]
        - visitor_anim: Dict[str, list]
        - creature_anims: Dict[str, Dict[str, list]]
        - entity_state: Dict[str, Dict[str, Any]]
        - frame_duration_ms: int
        + __init__()
        - _get_entity_state(eid: str) : Dict[str,Any]
        - _get_creature_animation(name: str) : Dict[str,list]
        - _draw_animated(screen: pygame.Surface, surf_list: list, eid: str, pos: tuple, moving: bool, direction: str, tile_size: int) : None
        + draw_entities(screen: pygame.Surface, state: Dict[str,Any], tile_size: int) : None
    }

    SpriteManager --> AssetLoader
```

- `SpriteManager` draws creatures, staff, visitors, and the player based on the frontend state.
- It uses `AssetLoader` for sprite and animation frame loading, with fallback shapes for missing assets.
