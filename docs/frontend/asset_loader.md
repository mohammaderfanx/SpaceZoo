# AssetLoader

```mermaid
classDiagram
    class AssetLoader {
        - _instance: Optional[AssetLoader]
        - assets_root: Path
        - cache: Dict[str, pygame.Surface]
        - map_size: Tuple[int,int]
        - tile_size: Tuple[int,int]
        - _initialized: bool
        + __new__(*args, **kwargs)
        + __init__(assets_root: Optional[Path] = None)
        + _placeholder_surface(size: Tuple[int,int], color: Tuple[int,int,int]) : pygame.Surface
        + load_image(path: Path, size: Optional[Tuple[int,int]] = None) : pygame.Surface
        + load_map() : pygame.Surface
        + load_creature(name: str) : pygame.Surface
        + _find_creature_folder(name: str) : Optional[Path]
        + _try_extract_stage(stem: str) : Optional[int]
        + load_creature_stage_images(name: str) : Dict[int, pygame.Surface]
        + load_creature_stage(name: str, stage: int) : pygame.Surface
        + load_animation(name: str, directions: Tuple[str,str] = ("right", "left")) : Dict[str, list]
        + load_all_creatures() : Dict[str, pygame.Surface]
    }
```

- `AssetLoader` is a singleton that loads and caches image assets for the frontend.
- It is responsible for image scaling, fallback placeholders, creature sprite loading, and animation frame retrieval.
