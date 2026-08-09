import os
from pathlib import Path

# Directory structure based on ARCHITECTURE.md
DIRECTORIES = [
    "backend",
    "database",
    "interface",
    "frontend"
]


def setup_workspace():
    """Create the required project folder structure for SpaceZoo.

    This helper generates the backend, database, interface, and frontend
    package directories along with __init__.py files if they do not already exist.

    Tests:
        first run in an empty project -> creates all required directories and init files
        repeated run -> preserves existing directories without error
    """
    base_dir = Path(__file__).parent.resolve()

    for folder in DIRECTORIES:
        dir_path = base_dir / folder
        dir_path.mkdir(parents=True, exist_ok=True)

        init_file = dir_path / "__init__.py"
        if not init_file.exists():
            init_file.touch()
            print(f"Created: {init_file.relative_to(base_dir)}")
        else:
            print(f"Already exists: {init_file.relative_to(base_dir)}")


if __name__ == "__main__":
    setup_workspace()
