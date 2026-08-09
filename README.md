# SpaceZoo — Digitaler Zwilling (Zoo-Simulation)

Kurzbeschreibung
-----------------
Dieses Projekt implementiert eine Zoo-Simulation in Python (Pygame) nach den Regeln in `ARCHITECTURE.md`.

Autor / Hinweise
-----------------
- Autor: <DEIN NAME HIER>
- Individueller Schwerpunkt: <DEINER INDIVIDUELLE SCHWERPUNKT HIER>

Voraussetzungen
-------------
- Python 3.14
- Ein Terminal auf Linux/macOS (Windows-Anweisungen analog)

Schnellstart
-----------
1. Virtuelle Umgebung anlegen und aktivieren:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Abhängigkeiten installieren:

```bash
pip install -r requirements.txt
```

3. Anwendung starten (Pygame-Fenster):

```bash
python frontend/main.py
```

Hinweise
-------
- Die Anwendung erwartet die Projektstruktur wie in `ARCHITECTURE.md` beschrieben.
- Die Persistenz nutzt SQLite unter `database/spacezoo.db`.
- Das Frontend darf nur die `SpaceZooAPI` aus `interface/spacezoo_api.py` nutzen.
- Bei fehlenden Assets erzeugt der `AssetLoader` Platzhaltergrafiken.

Beenden
------
- Schließe das Pygame-Fenster oder sende `Ctrl+C` im Terminal.

Weiterführende Aktionen
----------------------
- `python -m pytest` (falls Tests ergänzt wurden)
- Vor dem Commit: `pip freeze > requirements.txt` um exakte Versionen zu pinnen (optional)
- Headless render in Codespaces:
  ```bash
  python frontend/headless_screenshot.py
  ```
  This generates `codespaces_screenshot.png` in the project root.
