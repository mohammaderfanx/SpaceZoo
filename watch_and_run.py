"""
Entwickler-Watcher für SpaceZoo.

Beobachtet Quellcode- (.py) und Asset-Dateien im Projekt und startet
`frontend/main.py` automatisch neu, sobald sich eine davon ändert.

Nutzung:
    python watch_and_run.py
"""

import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
MAIN_SCRIPT = PROJECT_ROOT / "frontend" / "main.py"

WATCH_SOURCE_DIRS = ["backend", "database", "interface", "frontend"]
WATCH_ASSET_DIR = PROJECT_ROOT / "frontend" / "assets"
ASSET_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp"}

POLL_INTERVAL_SECONDS = 0.5


def _snapshot() -> dict:
    """Erfasst Pfad -> Änderungszeitpunkt für alle beobachteten Dateien."""
    state = {}

    for dir_name in WATCH_SOURCE_DIRS:
        for path in (PROJECT_ROOT / dir_name).rglob("*.py"):
            if "__pycache__" in path.parts:
                continue
            try:
                state[path] = path.stat().st_mtime
            except FileNotFoundError:
                pass

    if WATCH_ASSET_DIR.exists():
        for path in WATCH_ASSET_DIR.rglob("*"):
            if path.is_file() and path.suffix.lower() in ASSET_EXTENSIONS:
                try:
                    state[path] = path.stat().st_mtime
                except FileNotFoundError:
                    pass

    return state


def _launch() -> subprocess.Popen:
    return subprocess.Popen([sys.executable, str(MAIN_SCRIPT)], cwd=PROJECT_ROOT)


def _stop(process: subprocess.Popen) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=3)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()


def main() -> None:
    process = _launch()
    last_state = _snapshot()
    print("Watcher aktiv – beobachte .py- und Asset-Änderungen (Ctrl+C zum Beenden).")

    try:
        while True:
            time.sleep(POLL_INTERVAL_SECONDS)

            # Neu starten, falls das Spiel manuell geschlossen wurde.
            if process.poll() is not None:
                current_state = _snapshot()
                last_state = current_state
                process = _launch()
                continue

            current_state = _snapshot()
            if current_state != last_state:
                print("Änderung erkannt – starte SpaceZoo neu ...")
                last_state = current_state
                _stop(process)
                process = _launch()
    except KeyboardInterrupt:
        print("Watcher wird beendet ...")
    finally:
        _stop(process)


if __name__ == "__main__":
    main()
