import os
from pathlib import Path

# Ordnerstruktur basierend auf ARCHITECTURE.md
DIRECTORIES = [
    "backend",
    "database",
    "interface",
    "frontend"
]


def setup_workspace():
    base_dir = Path(__file__).parent.resolve()

    for folder in DIRECTORIES:
        dir_path = base_dir / folder
        dir_path.mkdir(parents=True, exist_ok=True)

        init_file = dir_path / "__init__.py"
        if not init_file.exists():
            init_file.touch()
            print(f"Erstellt: {init_file.relative_to(base_dir)}")
        else:
            print(f"Bereits vorhanden: {init_file.relative_to(base_dir)}")


if __name__ == "__main__":
    setup_workspace()
