# SimZoo

SimZoo is a zoo-management simulation written in Python. A backend simulation
engine models animals, enclosures, staff, feeding, illness, and breeding; a
Pygame frontend renders the state as a dashboard and lets you manage the zoo
in real time. Zoo state is persisted to a local SQLite database, so a session
survives a restart.

## Features

- Animal simulation: species (`Eagle`, `Wolf`, `Rabbit`), lifecycle, eggs,
  illness, and environmental factors
- Zoo management: enclosures, staff (`Caretaker`, `Vet`, `Cashier`), food and
  medicine inventory
- A `SimZooAPI` facade (`interface/simzoo_api.py`) that is the sole bridge
  between the frontend and backend logic
- Pygame dashboard UI with buy/hire menus, illness and day-count indicators
- SQLite persistence via `database/db_manager.py`

## Project structure

```
backend/            Simulation engine, animal simulation, zoo management
database/            SQLite persistence (db_manager.py, schema.sql)
interface/           SimZooAPI facade — the only frontend/backend bridge
frontend/            Pygame UI (entry point, renderer, input handling, assets)
docs/backend/        Class diagram and design notes
docs/frontend/       Frontend class diagrams and UI design notes
```

## Prerequisites

- Python 3.12+
- A terminal on Linux/macOS/Windows

## Installation

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Running the app

Start the Pygame frontend:

```bash
python frontend/main.py
```

This opens a resizable window with the zoo dashboard. Close the window or
press `Ctrl+C` in the terminal to quit.

## Data & persistence

Zoo state is stored in `database/simzoo.db` (SQLite), created automatically
on first run from `database/schema.sql`. Delete this file to reset the zoo to
a fresh state.

## Documentation

Further design notes and a class diagram live under [`docs/`]

## Contribution Focus
Backend simulation and animal systems implemented by Jasmin
Frontend, interface and database support implemented by Mohammed
