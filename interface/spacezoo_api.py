"""
Fassade (Facade-Pattern) für die SpaceZoo API.
Dient als einziger Schnittstellen- und Kommunikationskanal zwischen Frontend (Pygame) und Backend/Database.

Gemäß ARCHITECTURE.md:
- Das Frontend (frontend/) darf NIEMALS direkt Klassen aus backend/ oder database/ importieren.
- Die gesamte Kommunikation erfolgt über SpaceZooAPI.
- Alle Rückgabewerte und Parameter bestehen ausschließlich aus Python-Basisdatentypen (dict, list, int, float, str, bool, tuple).
"""

from typing import Any, Dict, List, Optional, Tuple
import uuid

# Backend / Database imports
from database.db_manager import DatabaseManager
from backend.simulation_engine_old import SimulationEngine
from backend.animal_old import Animal
from backend.staff import Caretaker, Vet, Cashier


class SpaceZooAPI:
    """
    Fassaden-Klasse zur Steuerung und Abfrage der Zoo-Simulation.
    Kapselt die Domänenlogik und Datenbankzugriffe und stellt entkoppelte
    Methoden für das Frontend bereit.
    """

    def __init__(self) -> None:
        """
        Initialisiert die API-Fassade und bereitet die Verbindung zu Backend
        und Datenbank vor.
        """
        # Instanziere DatabaseManager und SimulationEngine
        self.db = DatabaseManager()
        self.sim = SimulationEngine()

        # Lade persistenten Zustand aus der DB in die Simulation (sofern vorhanden)
        zoo_status = self.db.get_zoo_status()
        if zoo_status:
            try:
                self.sim.money = int(zoo_status.get("money", self.sim.money))
                self.sim.simulation_time = float(zoo_status.get("simulation_time", self.sim.simulation_time))
                self.sim.is_night = bool(zoo_status.get("is_night", self.sim.is_night))
                # Spielerposition
                px = int(zoo_status.get("player_x", self.sim.player.x))
                py = int(zoo_status.get("player_y", self.sim.player.y))
                self.sim.player.x = px
                self.sim.player.y = py
            except Exception:
                # Falls Parsing fehlschlägt, fahren wir mit Default-Werten fort
                pass

        # Lade Tiere + Personal aus DB
        try:
            creatures = self.db.get_all_creatures()
            self.sim.creatures = []
            for c in creatures:
                a = Animal(
                    id_=c["id"],
                    species=c["species"],
                    name=c["name"],
                    pos_x=int(c["pos_x"]),
                    pos_y=int(c["pos_y"]),
                    age_seconds=float(c.get("age_seconds", 0.0)),
                    hunger=float(c.get("hunger", 0.0)),
                    hunger_timer=float(c.get("hunger_timer", 10.0)),
                    is_sick=bool(c.get("is_sick", False)),
                    sick_timer=float(c.get("sick_timer", 15.0)),
                )
                self.sim.creatures.append(a)

            staff_rows = self.db.get_all_staff()
            self.sim.staff = []
            for s in staff_rows:
                stype = s.get("staff_type")
                if stype == "Caretaker":
                    member = Caretaker(s["id"], s["name"], int(s.get("pos_x", 10)), int(s.get("pos_y", 8)))
                elif stype == "Vet":
                    member = Vet(s["id"], s["name"], int(s.get("pos_x", 10)), int(s.get("pos_y", 8)))
                elif stype == "Cashier":
                    member = Cashier(s["id"], s["name"], int(s.get("pos_x", 10)), int(s.get("pos_y", 8)))
                else:
                    continue
                member.status = s.get("status", "Idle")
                self.sim.staff.append(member)
        except Exception:
            # Falls DB-Zugriff fehlschlägt, ignorieren wir beim Start
            pass

    def tick(self, delta_time: float) -> Dict[str, Any]:
        """
        Führt einen Simulationsschritt (Tick) aus und aktualisiert den Zoo-Zustand.

        Berechnet unter anderem:
        - Altersfortschritt der Tiere (15 min Lebenszyklus: Kind 0-5m, Erwachsen 5-10m, Alt 10-15m)
        - Kontinuierlich steigenden Hunger (10s Todes-Timer bei 100%)
        - Zufällige Krankheiten (15s Todes-Timer)
        - Autonome Aktionen des Personals (Caretaker füttert, Vet heilt, Cashier bedient)
        - Besucher-Spawns (alle 10s mit 45% Chance), Ticketkauf (15s Wartezeit, 1$ Eintritt),
          Aufenthalt (max. 10 Besucher zeitgleich im Zoo, Despawn nach 40s)
        - 2-Minuten Tag/Nacht-Zyklus

        :param delta_time: Vergangene Zeit seit dem letzten Tick in Sekunden.
        :return: Dictionary mit aufgetretenen Ereignissen und Statusänderungen im Tick.
        """
        result = self.sim.tick(delta_time)

        # Persistiere veränderte Creatures in die DB
        for creature in self.sim.creatures:
            try:
                self.db.update_creature({
                    "id": creature.id,
                    "age_seconds": creature.age_seconds,
                    "hunger": creature.hunger,
                    "hunger_timer": creature.hunger_timer,
                    "is_sick": creature.is_sick,
                    "sick_timer": creature.sick_timer,
                    "pos_x": creature.x,
                    "pos_y": creature.y,
                })
            except Exception:
                # Falls Update fehlschlägt, ignoriere es hier
                pass

        # Persistiere Zoo-Status
        try:
            self.db.update_zoo_status(
                money=self.sim.money,
                simulation_time=self.sim.simulation_time,
                is_night=self.sim.is_night,
                player_x=self.sim.player.x,
                player_y=self.sim.player.y,
            )
        except Exception:
            pass

        return result

    def get_zoo_state(self) -> Dict[str, Any]:
        """
        Liefert den vollständigen aktuellen Gesamtzustand der Zoo-Simulation.

        :return: Dictionary mit allen Kern-Informationen:
                 - 'money': Aktueller Kontostand (int)
                 - 'time': Simulationszeit & Tagesphase (dict)
                 - 'player': Spielerposition und Status (dict)
                 - 'creatures': Liste aller Tiere (List[dict])
                 - 'visitors': Liste aller Besucher (List[dict])
                 - 'staff': Liste aller Mitarbeiter (List[dict])
                 - 'map': Kachelraster & Objekte auf der Map (dict)
        """
        # Basisinformationen
        cycle_progress = self.sim.simulation_time % self.sim.day_duration
        day_phase = "Nacht" if self.sim.is_night else "Tag"
        # Zeit bis Ende der aktuellen Phase (Halbzyklus)
        half = self.sim.day_duration / 2.0
        if cycle_progress < half:
            time_remaining = half - cycle_progress
        else:
            time_remaining = self.sim.day_duration - cycle_progress

        state: Dict[str, Any] = {
            "money": int(self.sim.money),
            "time": {
                "simulation_time": float(self.sim.simulation_time),
                "day_phase": day_phase,
                "time_remaining": float(time_remaining),
            },
            "player": self.sim.player.to_dict(),
            "creatures": [c.to_dict() for c in self.sim.creatures],
            "visitors": [v.to_dict() for v in self.sim.visitors],
            "staff": [s.to_dict() for s in self.sim.staff],
            "map": {
                "grid_width": 21,
                "grid_height": 16,
                "tile_size": 60,
                # Minimal: leere Tiles-Map (Frontend kann sie erweitern)
                "tiles": [[{"type": "floor", "walkable": True} for _ in range(21)] for _ in range(16)],
            },
        }

        return state

    def move_player(self, dx: int, dy: int) -> Dict[str, Any]:
        """
        Bewegt die Spielfigur auf dem Grid (WASD-Steuerung).

        :param dx: Bewegungsrichtung auf der X-Achse (-1, 0, 1).
        :param dy: Bewegungsrichtung auf der Y-Achse (-1, 0, 1).
        :return: Dictionary mit 'success' (bool), 'position' (Tuple[int, int]) und 'message' (str).
        """
        new_pos = self.sim.player.move(dx, dy)
        # Persistiere Spielerposition
        try:
            self.db.update_zoo_status(
                money=self.sim.money,
                simulation_time=self.sim.simulation_time,
                is_night=self.sim.is_night,
                player_x=self.sim.player.x,
                player_y=self.sim.player.y,
            )
        except Exception:
            pass

        return {"success": True, "position": new_pos, "message": "Player moved"}

    def buy_creature(
        self,
        species: str,
        name: Optional[str] = None,
        position: Optional[Tuple[int, int]] = None,
    ) -> Dict[str, Any]:
        """
        Kauft ein neues Tier einer der 6 Arten (Birdy, Liz, Mal, Pinky, Rizzy, Sami).

        :param species: Tierart ('Birdy', 'Liz', 'Mal', 'Pinky', 'Rizzy', 'Sami').
        :param name: Optionaler individueller Name für das Tier.
        :param position: Optionale Grid-Position (x, y) auf der Karte.
        :return: Dictionary mit 'success' (bool), 'message' (str) und ggf. 'creature' (dict).
        """
        name = name or f"{species}_{str(uuid.uuid4())[:4]}"
        new_animal = self.sim.buy_animal(species, name)
        if new_animal:
            # Persistiert neues Tier
            try:
                self.db.add_creature({
                    "id": new_animal.id,
                    "species": new_animal.species,
                    "name": new_animal.name,
                    "age_seconds": new_animal.age_seconds,
                    "hunger": new_animal.hunger,
                    "hunger_timer": new_animal.hunger_timer,
                    "is_sick": new_animal.is_sick,
                    "sick_timer": new_animal.sick_timer,
                    "pos_x": new_animal.x,
                    "pos_y": new_animal.y,
                })
            except Exception:
                pass

            return {"success": True, "message": "Creature bought", "creature": new_animal.to_dict()}
        return {"success": False, "message": "Not enough money or invalid species"}

    def feed_creature(self, creature_id: str) -> Dict[str, Any]:
        """
        Füttert ein Tier manuell (setzt den Hungerwert zurück bzw. verringert ihn).

        :param creature_id: Eindeutige ID des Tiers.
        :return: Dictionary mit 'success' (bool) und 'message' (str).
        """
        for creature in self.sim.creatures:
            if creature.id == creature_id:
                creature.feed()
                try:
                    self.db.update_creature({
                        "id": creature.id,
                        "age_seconds": creature.age_seconds,
                        "hunger": creature.hunger,
                        "hunger_timer": creature.hunger_timer,
                        "is_sick": creature.is_sick,
                        "sick_timer": creature.sick_timer,
                        "pos_x": creature.x,
                        "pos_y": creature.y,
                    })
                except Exception:
                    pass
                return {"success": True, "message": "Creature fed"}
        return {"success": False, "message": "Creature not found"}

    def heal_creature(self, creature_id: str) -> Dict[str, Any]:
        """
        Heilt ein erkranktes Tier manuell (stoppt den 15s Krankheitstimer).

        :param creature_id: Eindeutige ID des Tiers.
        :return: Dictionary mit 'success' (bool) und 'message' (str).
        """
        for creature in self.sim.creatures:
            if creature.id == creature_id:
                creature.heal()
                try:
                    self.db.update_creature({
                        "id": creature.id,
                        "age_seconds": creature.age_seconds,
                        "hunger": creature.hunger,
                        "hunger_timer": creature.hunger_timer,
                        "is_sick": creature.is_sick,
                        "sick_timer": creature.sick_timer,
                        "pos_x": creature.x,
                        "pos_y": creature.y,
                    })
                except Exception:
                    pass
                return {"success": True, "message": "Creature healed"}
        return {"success": False, "message": "Creature not found"}

    def hire_staff(self, staff_type: str) -> Dict[str, Any]:
        """
        Stellt neues Personal ein (Kosten: 10$).

        Mögliche Rollen:
        - 'Caretaker': Füttert hungrige Tiere autonom.
        - 'Vet': Heilt kranke Tiere autonom.
        - 'Cashier': Bedient den Ticketschalter.

        :param staff_type: Rolle des Personals ('Caretaker', 'Vet', 'Cashier').
        :return: Dictionary mit 'success' (bool), 'message' (str) und 'staff' (dict).
        """
        # Generiere einen Default-Namen
        name = f"{staff_type}_{str(uuid.uuid4())[:4]}"
        member = self.sim.hire_staff(staff_type, name)
        if member:
            try:
                self.db.add_staff({
                    "id": member.id,
                    "staff_type": member.staff_type,
                    "name": member.name,
                    "salary": member.salary,
                    "status": member.status,
                    "pos_x": member.x,
                    "pos_y": member.y,
                })
            except Exception:
                pass
            return {"success": True, "message": "Staff hired", "staff": member.to_dict()}
        return {"success": False, "message": "Not enough money or invalid staff type"}

    def fire_staff(self, staff_id: str) -> Dict[str, Any]:
        """
        Entlässt ein Personalmitglied.

        :param staff_id: Eindeutige ID des Mitarbeiters.
        :return: Dictionary mit 'success' (bool) und 'message' (str).
        """
        for member in list(self.sim.staff):
            if member.id == staff_id:
                try:
                    self.sim.staff.remove(member)
                    self.db.delete_staff(staff_id)
                except Exception:
                    pass
                return {"success": True, "message": "Staff fired"}
        return {"success": False, "message": "Staff not found"}

    def get_quick_stats(self) -> Dict[str, Any]:
        """
        Liefert kompakte Statistiken für die eingeklappte Taskbar am unteren Bildschirmrand.

        :return: Dictionary mit Quick-Stats:
                 - 'money': int
                 - 'visitor_count': int
                 - 'creature_count': int
                 - 'day_phase': str ('Tag' / 'Nacht')
                 - 'time_remaining': float (Restzeit der aktuellen Phase in Sekunden)
        """
        visitor_count = sum(1 for v in self.sim.visitors if v.status in ["InZoo", "BuyingTicket", "Queuing"])
        creature_count = len(self.sim.creatures)
        cycle_progress = self.sim.simulation_time % self.sim.day_duration
        half = self.sim.day_duration / 2.0
        if cycle_progress < half:
            time_remaining = half - cycle_progress
            day_phase = "Tag"
        else:
            time_remaining = self.sim.day_duration - cycle_progress
            day_phase = "Nacht"

        return {
            "money": int(self.sim.money),
            "visitor_count": int(visitor_count),
            "creature_count": int(creature_count),
            "day_phase": day_phase,
            "time_remaining": float(time_remaining),
        }

    def get_detailed_dashboard(self) -> Dict[str, Any]:
        """
        Liefert detaillierte Informationen für das aufgeklappte Dashboard in der Taskbar.

        :return: Dictionary mit umfangreichen Statistiken:
                 - 'finances': Einnahmen, Ausgaben, Ticketverkäufe, Gehälter (dict)
                 - 'creatures_summary': Aufschlüsselung nach Arten, Alter, Hunger, Gesundheit (dict)
                 - 'visitors_summary': Wartezeiten, Gesamteintritte, Zufriedenheit (dict)
                 - 'staff_summary': Übersicht der aktiven Mitarbeiter (dict)
        """
        finances = {
            "money": int(self.sim.money),
        }

        creatures_summary: Dict[str, Dict[str, Any]] = {}
        for c in self.sim.creatures:
            spec = c.species
            entry = creatures_summary.setdefault(spec, {"count": 0, "avg_hunger": 0.0, "sick": 0})
            entry["count"] += 1
            entry["avg_hunger"] += c.hunger
            if c.is_sick:
                entry["sick"] += 1

        # finalize averages
        for spec, entry in creatures_summary.items():
            if entry["count"] > 0:
                entry["avg_hunger"] = entry["avg_hunger"] / entry["count"]

        visitors_summary = {
            "total": len(self.sim.visitors),
            "in_queue": sum(1 for v in self.sim.visitors if v.status == "Queuing"),
            "in_zoo": sum(1 for v in self.sim.visitors if v.status == "InZoo"),
        }

        staff_summary = {s.id: s.to_dict() for s in self.sim.staff}

        return {
            "finances": finances,
            "creatures_summary": creatures_summary,
            "visitors_summary": visitors_summary,
            "staff_summary": staff_summary,
        }

    def get_creatures(self) -> List[Dict[str, Any]]:
        """
        Liefert eine Liste aller Tiere im Zoo mit ihren aktuellen Attributen.

        :return: Liste von Dictionaries, jedes repräsentiert ein Tier:
                 - 'id': str
                 - 'species': str
                 - 'name': str
                 - 'age_seconds': float
                 - 'life_stage': str ('Kind', 'Erwachsen', 'Alt')
                 - 'hunger': float (0.0 bis 100.0)
                 - 'hunger_timer': float (Ablauftimer bei 100% Hunger)
                 - 'is_sick': bool
                 - 'sick_timer': float (Ablauftimer bei Krankheit)
                 - 'position': Tuple[int, int]
        """
        return [c.to_dict() for c in self.sim.creatures]

    def get_visitors(self) -> List[Dict[str, Any]]:
        """
        Liefert eine Liste aller aktuellen Besucher (Warteschlange & im Zoo).

        :return: Liste von Dictionaries, jedes repräsentiert einen Besucher:
                 - 'id': str
                 - 'status': str ('Queuing', 'BuyingTicket', 'InZoo', 'Leaving')
                 - 'wait_time': float
                 - 'time_in_zoo': float (max. 40s)
                 - 'position': Tuple[int, int]
        """
        return [v.to_dict() for v in self.sim.visitors]

    def get_staff(self) -> List[Dict[str, Any]]:
        """
        Liefert eine Liste aller angestellten Mitarbeiter.

        :return: Liste von Dictionaries, jedes repräsentiert ein Personalmitglied:
                 - 'id': str
                 - 'type': str ('Caretaker', 'Vet', 'Cashier')
                 - 'status': str ('Idle', 'Working')
                 - 'target_id': Optional[str]
                 - 'position': Tuple[int, int]
        """
        return [s.to_dict() for s in self.sim.staff]

    def get_map_state(self) -> Dict[str, Any]:
        """
        Liefert den Zustand der Spielkarte (Grid: 21x16, Karte: 1260x960 Pixel, Sprites: 60x60 Pixel).

        :return: Dictionary mit Map-Informationen:
                 - 'grid_width': int (21)
                 - 'grid_height': int (16)
                 - 'tile_size': int (60)
                 - 'tiles': List[List[dict]] (Raster-Kacheln mit Typ und Begehbarkeit)
        """
        return {
            "grid_width": 21,
            "grid_height": 16,
            "tile_size": 60,
            "tiles": [[{"type": "floor", "walkable": True} for _ in range(21)] for _ in range(16)],
        }

    def save_game(self, slot: str = "default") -> Dict[str, Any]:
        """
        Speichert den aktuellen Spielstand in der Datenbank.

        :param slot: Bezeichner/Name des Speicherstands.
        :return: Dictionary mit 'success' (bool) und 'message' (str).
        """
        try:
            # Persistiere Zoo-Status
            self.db.update_zoo_status(
                money=self.sim.money,
                simulation_time=self.sim.simulation_time,
                is_night=self.sim.is_night,
                player_x=self.sim.player.x,
                player_y=self.sim.player.y,
            )

            # Persistiere alle Tiere
            for c in self.sim.creatures:
                try:
                    self.db.add_creature({
                        "id": c.id,
                        "species": c.species,
                        "name": c.name,
                        "age_seconds": c.age_seconds,
                        "hunger": c.hunger,
                        "hunger_timer": c.hunger_timer,
                        "is_sick": c.is_sick,
                        "sick_timer": c.sick_timer,
                        "pos_x": c.x,
                        "pos_y": c.y,
                    })
                except Exception:
                    # Falls schon existiert, update
                    try:
                        self.db.update_creature({
                            "id": c.id,
                            "age_seconds": c.age_seconds,
                            "hunger": c.hunger,
                            "hunger_timer": c.hunger_timer,
                            "is_sick": c.is_sick,
                            "sick_timer": c.sick_timer,
                            "pos_x": c.x,
                            "pos_y": c.y,
                        })
                    except Exception:
                        pass

            # Persistiere Personal
            for s in self.sim.staff:
                try:
                    self.db.add_staff(s.to_dict())
                except Exception:
                    pass

            return {"success": True, "message": "Saved to DB (slot override)"}
        except Exception as e:
            return {"success": False, "message": f"Save failed: {e}"}

    def load_game(self, slot: str = "default") -> Dict[str, Any]:
        """
        Lädt einen gespeicherten Spielstand aus der Datenbank.

        :param slot: Bezeichner/Name des Speicherstands.
        :return: Dictionary mit 'success' (bool), 'message' (str) und 'state' (dict).
        """
        try:
            zoo_status = self.db.get_zoo_status() or {}
            self.sim.money = int(zoo_status.get("money", self.sim.money))
            self.sim.simulation_time = float(zoo_status.get("simulation_time", self.sim.simulation_time))
            self.sim.is_night = bool(zoo_status.get("is_night", self.sim.is_night))
            self.sim.player.x = int(zoo_status.get("player_x", self.sim.player.x))
            self.sim.player.y = int(zoo_status.get("player_y", self.sim.player.y))

            # Lade Tiere
            creatures = self.db.get_all_creatures()
            self.sim.creatures = []
            for c in creatures:
                a = Animal(
                    id_=c["id"],
                    species=c["species"],
                    name=c["name"],
                    pos_x=int(c["pos_x"]),
                    pos_y=int(c["pos_y"]),
                    age_seconds=float(c.get("age_seconds", 0.0)),
                    hunger=float(c.get("hunger", 0.0)),
                    hunger_timer=float(c.get("hunger_timer", 10.0)),
                    is_sick=bool(c.get("is_sick", False)),
                    sick_timer=float(c.get("sick_timer", 15.0)),
                )
                self.sim.creatures.append(a)

            # Lade Personal
            staff_rows = self.db.get_all_staff()
            self.sim.staff = []
            for s in staff_rows:
                stype = s.get("staff_type")
                if stype == "Caretaker":
                    member = Caretaker(s["id"], s["name"], int(s.get("pos_x", 10)), int(s.get("pos_y", 8)))
                elif stype == "Vet":
                    member = Vet(s["id"], s["name"], int(s.get("pos_x", 10)), int(s.get("pos_y", 8)))
                elif stype == "Cashier":
                    member = Cashier(s["id"], s["name"], int(s.get("pos_x", 10)), int(s.get("pos_y", 8)))
                else:
                    continue
                member.status = s.get("status", "Idle")
                self.sim.staff.append(member)

            return {"success": True, "message": "Loaded from DB", "state": self.get_zoo_state()}
        except Exception as e:
            return {"success": False, "message": f"Load failed: {e}"}
