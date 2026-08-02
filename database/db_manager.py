"""
DatabaseManager für SpaceZoo.
Verwaltet die SQLite-Datenbankverbindung, initialisiert das Schema (database/schema.sql)
und stellt Repository-Methoden (CRUD) für Zoo-Status, Tiere, Personal und Inventar bereit.
"""

import os
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class DatabaseManager:
    """
    Klasse zur Verwaltung der SQLite-Datenbankverbindung und Durchführung
    von CRUD-Operationen gemäß dem Repository-Pattern.
    """

    def __init__(self, db_path: Optional[str] = None) -> None:
        """
        Initialisiert den DatabaseManager und stellt sicher, dass die Datenbank
        samt Schema existiert.

        :param db_path: Optionaler Pfad zur SQLite-Datenbankdatei. Standartmäßig 'database/spacezoo.db'.
        """
        if db_path is None:
            base_dir = Path(__file__).parent.resolve()
            db_path = str(base_dir / "spacezoo.db")

        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        """
        Erstellt eine neue SQLite-Verbindung und setzt den row_factory für Dict-ähnlichen Zugriff.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        """
        Initialisiert das Datenbank-Schema aus 'database/schema.sql', falls nicht vorhanden.
        """
        schema_path = Path(__file__).parent / "schema.sql"
        if not schema_path.exists():
            raise FileNotFoundError(f"Schema-Datei nicht gefunden: {schema_path}")

        with open(schema_path, "r", encoding="utf-8") as f:
            schema_script = f.read()

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.executescript(schema_script)
            conn.commit()

    # --- Zoo Status CRUD ---

    def get_zoo_status(self) -> Optional[Dict[str, Any]]:
        """
        Liest den aktuellen Singleton-Zoo-Status aus der Datenbank.

        :return: Dictionary mit Geld, Zeit, Tag/Nacht-Status und Spielerposition.
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
        Aktualisiert den Singleton-Zoo-Status in der Datenbank.
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
        Fügt ein neues Tier in die Datenbank ein.

        :param creature: Dict mit keys: 'id', 'species', 'name', 'age_seconds', 'hunger', 'hunger_timer', 'is_sick', 'sick_timer', 'pos_x', 'pos_y'
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
        Liest alle registrierten Tiere aus der Datenbank.

        :return: Liste von Tier-Dictionaries.
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
        Aktualisiert den Zustand eines Tieres in der Datenbank.
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
        Löscht ein Tier aus der Datenbank (z.B. nach Versterben).
        """
        query = "DELETE FROM creatures WHERE id = ?"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (creature_id,))
            conn.commit()

    # --- Staff CRUD ---

    def add_staff(self, staff_member: Dict[str, Any]) -> None:
        """
        Fügt ein neues Personalmitglied in die Datenbank ein.

        :param staff_member: Dict mit keys: 'id', 'staff_type', 'name', 'salary', 'status', 'pos_x', 'pos_y'
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
        Liest alle Mitarbeiter aus der Datenbank.

        :return: Liste von Personal-Dictionaries.
        """
        query = "SELECT * FROM staff"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]

    def update_staff(self, staff_member: Dict[str, Any]) -> None:
        """
        Aktualisiert den Zustand eines Mitarbeiters.
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
        Entlässt ein Personalmitglied aus der Datenbank.
        """
        query = "DELETE FROM staff WHERE id = ?"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (staff_id,))
            conn.commit()

    # --- Inventory CRUD ---

    def get_all_inventory(self) -> List[Dict[str, Any]]:
        """
        Liest das gesamte Inventar aus.
        """
        query = "SELECT * FROM inventory"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]

    def update_inventory_item(self, item_id: str, item_name: str, quantity: int) -> None:
        """
        Erstellt oder aktualisiert einen Inventar-Eintrag.
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
