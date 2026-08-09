"""
DatabaseManager for SpaceZoo.
Manages the SQLite database connection, initializes the schema (database/schema.sql),
and exposes repository-style CRUD methods for zoo status, animals, staff, and inventory.
"""

import os
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class DatabaseManager:
    """
    Class to manage the SQLite database connection and perform CRUD operations
    following the repository pattern.
    """

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
        """
        Create a new SQLite connection and configure row_factory for dict-like row access.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        """
        Initialize the database schema from 'database/schema.sql' if it is missing.
        """
        schema_path = Path(__file__).parent / "schema.sql"
        if not schema_path.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_path}")

        with open(schema_path, "r", encoding="utf-8") as f:
            schema_script = f.read()

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.executescript(schema_script)
            conn.commit()

    # --- Zoo Status CRUD ---

    def get_zoo_status(self) -> Optional[Dict[str, Any]]:
        """
        Read the current singleton zoo status from the database.

        :return: Dictionary containing money, simulation time, day/night flag, and player position.
        """
        query = "SELECT money, simulation_time, is_night, player_x, player_y FROM zoo_status WHERE id = 1"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            row = cursor.fetchone()
            if row:
                return dict(row)
        return None

    def update_zoo_status(
        self,
        money: int,
        simulation_time: float,
        is_night: bool,
        player_x: int,
        player_y: int,
    ) -> None:
        """
        Update the singleton zoo status record in the database.
        """
        query = """
            UPDATE zoo_status
            SET money = ?, simulation_time = ?, is_night = ?, player_x = ?, player_y = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = 1
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                query, (money, simulation_time, 1 if is_night else 0, player_x, player_y)
            )
            conn.commit()

    # --- Creatures CRUD ---

    def add_creature(self, creature: Dict[str, Any]) -> None:
        """
        Insert a new creature into the database.

        :param creature: Dict with keys: 'id', 'species', 'name', 'age_seconds', 'hunger', 'hunger_timer', 'is_sick', 'sick_timer', 'pos_x', 'pos_y'
        """
        query = """
            INSERT INTO creatures (id, species, name, age_seconds, hunger, hunger_timer, is_sick, sick_timer, pos_x, pos_y)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                query,
                (
                    creature["id"],
                    creature["species"],
                    creature["name"],
                    creature.get("age_seconds", 0.0),
                    creature.get("hunger", 0.0),
                    creature.get("hunger_timer", 10.0),
                    1 if creature.get("is_sick", False) else 0,
                    creature.get("sick_timer", 15.0),
                    creature["pos_x"],
                    creature["pos_y"],
                ),
            )
            conn.commit()

    def get_all_creatures(self) -> List[Dict[str, Any]]:
        """
        Read all registered creatures from the database.

        :return: List of creature dictionaries.
        """
        query = "SELECT * FROM creatures"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            results = []
            for row in rows:
                item = dict(row)
                item["is_sick"] = bool(item["is_sick"])
                results.append(item)
            return results

    def update_creature(self, creature: Dict[str, Any]) -> None:
        """
        Update the state of a creature record in the database.
        """
        query = """
            UPDATE creatures
            SET age_seconds = ?, hunger = ?, hunger_timer = ?, is_sick = ?, sick_timer = ?, pos_x = ?, pos_y = ?
            WHERE id = ?
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                query,
                (
                    creature["age_seconds"],
                    creature["hunger"],
                    creature["hunger_timer"],
                    1 if creature["is_sick"] else 0,
                    creature["sick_timer"],
                    creature["pos_x"],
                    creature["pos_y"],
                    creature["id"],
                ),
            )
            conn.commit()

    def delete_creature(self, creature_id: str) -> None:
        """
        Delete a creature from the database (for example, after it has died).
        """
        query = "DELETE FROM creatures WHERE id = ?"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (creature_id,))
            conn.commit()

    # --- Staff CRUD ---

    def add_staff(self, staff_member: Dict[str, Any]) -> None:
        """
        Insert a new staff member into the database.

        :param staff_member: Dict with keys: 'id', 'staff_type', 'name', 'salary', 'status', 'pos_x', 'pos_y'
        """
        query = """
            INSERT INTO staff (id, staff_type, name, salary, status, pos_x, pos_y)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                query,
                (
                    staff_member["id"],
                    staff_member["staff_type"],
                    staff_member["name"],
                    staff_member.get("salary", 10),
                    staff_member.get("status", "Idle"),
                    staff_member["pos_x"],
                    staff_member["pos_y"],
                ),
            )
            conn.commit()

    def get_all_staff(self) -> List[Dict[str, Any]]:
        """
        Read all staff records from the database.

        :return: List of staff dictionaries.
        """
        query = "SELECT * FROM staff"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]

    def update_staff(self, staff_member: Dict[str, Any]) -> None:
        """
        Update the state of a staff record.
        """
        query = """
            UPDATE staff
            SET status = ?, pos_x = ?, pos_y = ?
            WHERE id = ?
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                query,
                (
                    staff_member["status"],
                    staff_member["pos_x"],
                    staff_member["pos_y"],
                    staff_member["id"],
                ),
            )
            conn.commit()

    def delete_staff(self, staff_id: str) -> None:
        """
        Remove a staff member from the database.
        """
        query = "DELETE FROM staff WHERE id = ?"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (staff_id,))
            conn.commit()

    # --- Inventory CRUD ---

    def get_all_inventory(self) -> List[Dict[str, Any]]:
        """
        Read the full inventory from the database.
        """
        query = "SELECT * FROM inventory"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]

    def update_inventory_item(self, item_id: str, item_name: str, quantity: int) -> None:
        """
        Create or update an inventory item record.
        """
        query = """
            INSERT INTO inventory (item_id, item_name, quantity, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(item_id) DO UPDATE SET
                quantity = excluded.quantity,
                updated_at = CURRENT_TIMESTAMP
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (item_id, item_name, quantity))
            conn.commit()
