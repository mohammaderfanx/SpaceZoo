"""
DatabaseManager for DinoZoo / SpaceZoo.
Manages the SQLite database connection, initializes the schema (database/schema.sql),
and persists/restores the full backend simulation state so a session survives a restart.
"""

import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional


class DatabaseManager:
    """Manages the SQLite database connection and persists the full zoo save state."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        """
        Initialize the DatabaseManager and ensure the database file and schema exist.

        :param db_path: Optional path to the SQLite database file. Defaults to 'database/spacezoo.db'.
        """
        if db_path is None:
            base_dir = Path(__file__).parent.resolve()
            db_path = str(base_dir / "spacezoo.db")

        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        schema_path = Path(__file__).parent / "schema.sql"
        if not schema_path.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_path}")

        with open(schema_path, "r", encoding="utf-8") as f:
            schema_script = f.read()

        with self._get_connection() as conn:
            conn.executescript(schema_script)
            conn.commit()

    def has_save(self) -> bool:
        """Returns whether a previously saved game exists."""
        with self._get_connection() as conn:
            row = conn.execute("SELECT has_save FROM zoo_status WHERE id = 1").fetchone()
            return bool(row and row["has_save"])

    def save_full_state(self, state: Dict[str, Any]) -> None:
        """Persists the full zoo state, replacing whatever was previously saved.

        :param state: dict shaped like SpaceZooAPI._serialize_state_for_save()'s output.
        """
        with self._get_connection() as conn:
            conn.execute(
                """
                UPDATE zoo_status
                SET has_save = 1, budget = ?, elapsed_days = ?, elapsed_hours = ?,
                    visitors = ?, score = ?, weather = ?, temperature = ?, wind_speed = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = 1
                """,
                (
                    state["budget"],
                    state["elapsed_days"],
                    state["elapsed_hours"],
                    state["visitors"],
                    state["score"],
                    state["weather"],
                    state["temperature"],
                    state["wind_speed"],
                ),
            )

            conn.execute("DELETE FROM animals")
            conn.execute("DELETE FROM enclosures")
            conn.execute("DELETE FROM staff")
            conn.execute("DELETE FROM food_items")
            conn.execute("DELETE FROM medicine_items")
            conn.execute("DELETE FROM eggs")

            conn.executemany(
                "INSERT INTO enclosures (number, capacity, diet, cleanliness) VALUES (?, ?, ?, ?)",
                [(e["number"], e["capacity"], e["diet"], e["cleanliness"]) for e in state["enclosures"]],
            )
            conn.executemany(
                """
                INSERT INTO animals (id, species, name, birthdate, gender, health, saturation,
                                      energy, awake, illness_name, enclosure_number)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        a["id"], a["species"], a["name"], a["birthdate"], a["gender"],
                        a["health"], a["saturation"], a["energy"], 1 if a["awake"] else 0,
                        a["illness_name"], a["enclosure_number"],
                    )
                    for a in state["animals"]
                ],
            )
            conn.executemany(
                """
                INSERT INTO staff (id, type, name, shift_start, shift_end, salary, busy_for, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        s["id"], s["type"], s["name"], s["shift_start"], s["shift_end"],
                        s["salary"], s["busy_for"], s["status"],
                    )
                    for s in state["staff"]
                ],
            )
            conn.executemany(
                "INSERT INTO food_items (food_type, weight, best_before) VALUES (?, ?, ?)",
                [(f["food_type"], f["weight"], f["best_before"]) for f in state["food_items"]],
            )
            conn.executemany(
                "INSERT INTO medicine_items (medicine_type, quantity) VALUES (?, ?)",
                [(m["medicine_type"], m["quantity"]) for m in state["medicine_items"]],
            )
            conn.executemany(
                "INSERT INTO eggs (species, day_of_hatching) VALUES (?, ?)",
                [(e["species"], e["day_of_hatching"]) for e in state["eggs"]],
            )
            conn.commit()

    def load_full_state(self) -> Optional[Dict[str, Any]]:
        """Reads the full saved zoo state, or None if no save exists yet."""
        if not self.has_save():
            return None

        with self._get_connection() as conn:
            status_row = conn.execute(
                """
                SELECT budget, elapsed_days, elapsed_hours, visitors, score,
                       weather, temperature, wind_speed
                FROM zoo_status WHERE id = 1
                """
            ).fetchone()
            enclosures = [dict(row) for row in conn.execute("SELECT * FROM enclosures ORDER BY number")]
            animals = [dict(row) for row in conn.execute("SELECT * FROM animals")]
            staff = [dict(row) for row in conn.execute("SELECT * FROM staff")]
            food_items = [dict(row) for row in conn.execute("SELECT * FROM food_items")]
            medicine_items = [dict(row) for row in conn.execute("SELECT * FROM medicine_items")]
            eggs = [dict(row) for row in conn.execute("SELECT * FROM eggs")]

        for animal in animals:
            animal["awake"] = bool(animal["awake"])

        state = dict(status_row)
        state.update({
            "enclosures": enclosures,
            "animals": animals,
            "staff": staff,
            "food_items": food_items,
            "medicine_items": medicine_items,
            "eggs": eggs,
        })
        return state
