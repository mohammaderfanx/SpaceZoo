# MapRenderer

```mermaid
classDiagram
    class MapRenderer {
        - grid_width: int
        - grid_height: int
        - tile_size: int
        - bg_color: Tuple[int,int,int]
        - line_color: Tuple[int,int,int]
        - tile_color: Tuple[int,int,int]
        + __init__(grid_width: int = 21, grid_height: int = 16, tile_size: int = 60)
        + draw_grid(screen: pygame.Surface) : None
        + draw_background(screen: pygame.Surface) : None
        + screen_size() : Tuple[int,int]
    }

    MapRenderer --> AssetLoader
```

- `MapRenderer` renders the grid and optional background map for the game world.
- It delegates background image loading to `AssetLoader` and falls back to procedural rendering if loading fails.
