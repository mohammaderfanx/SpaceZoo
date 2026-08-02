"""
Staff-Modul für SpaceZoo.
Enthält die Basisklasse Staff sowie die spezialisierten Unterklassen Caretaker, Vet und Cashier.
Laut ARCHITECTURE.md gilt die Regel: Eine Klasse = Eine Datei.
Da das Modul jedoch zusammenhängende Personalrollen abbildet, definieren wir hier die Hierarchie.
"""

from typing import Any, Dict, Optional, Tuple


class Staff:
    """
    Abstrakte bzw. Basisklasse für alle Mitarbeiter im Zoo.
    """

    def __init__(
        self,
        id_: str,
        name: str,
        staff_type: str,
        pos_x: int,
        pos_y: int,
        salary: int = 10,
    ) -> None:
        """
        Initialisiert einen Mitarbeiter.

        :param id_: Eindeutige ID des Mitarbeiters.
        :param name: Name des Mitarbeiters.
        :param staff_type: Typ des Mitarbeiters ('Caretaker', 'Vet', 'Cashier').
        :param pos_x: X-Position auf dem Grid.
        :param pos_y: Y-Position auf dem Grid.
        :param salary: Tägliche/Periodische Gehaltskosten (Standard: 10$).
        """
        self.id = id_
        self.name = name
        self.staff_type = staff_type
        self.x = pos_x
        self.y = pos_y
        self.salary = salary
        self.status = "Idle"  # 'Idle', 'Working'
        self.target_id = None  # Ziel-ID für eine anstehende Aufgabe (z.B. Tier-ID oder Kassen-ID)

    def move_to(self, target_x: int, target_y: int) -> Tuple[int, int]:
        """
        Bewegt den Mitarbeiter einen Schritt in Richtung des Ziels.

        :return: Neue Position als (x, y) Tuple.
        """
        if self.x < target_x:
            self.x += 1
        elif self.x > target_x:
            self.x -= 1

        if self.y < target_y:
            self.y += 1
        elif self.y > target_y:
            self.y -= 1

        return (self.x, self.y)

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialisiert die Mitarbeiterdaten in ein Dictionary zur Kommunikation mit dem Frontend.
        """
        return {
            "id": self.id,
            "name": self.name,
            "type": self.staff_type,
            "salary": self.salary,
            "status": self.status,
            "target_id": self.target_id,
            "position": (self.x, self.y),
        }


class Caretaker(Staff):
    """
    Tierpfleger. Füttert autonom hungrige Tiere.
    """

    def __init__(self, id_: str, name: str, pos_x: int, pos_y: int) -> None:
        super().__init__(id_, name, "Caretaker", pos_x, pos_y, salary=10)

    def feed_animal(self, animal: Any) -> bool:
        """
        Füttert das zugewiesene Tier, wenn es in Reichweite ist (z.B. Abstand <= 1 Kachel).

        :param animal: Das Animal-Objekt.
        :return: True, wenn die Fütterung erfolgreich war, andernfalls False.
        """
        # Distanz prüfen
        distance = abs(self.x - animal.x) + abs(self.y - animal.y)
        if distance <= 1:
            animal.feed()
            self.status = "Idle"
            self.target_id = None
            return True
        return False


class Vet(Staff):
    """
    Tierarzt. Heilt autonom erkrankte Tiere.
    """

    def __init__(self, id_: str, name: str, pos_x: int, pos_y: int) -> None:
        super().__init__(id_, name, "Vet", pos_x, pos_y, salary=10)

    def heal_animal(self, animal: Any) -> bool:
        """
        Heilt das zugewiesene Tier, wenn es in Reichweite ist (Abstand <= 1 Kachel).

        :param animal: Das Animal-Objekt.
        :return: True, wenn die Heilung erfolgreich war, andernfalls False.
        """
        distance = abs(self.x - animal.x) + abs(self.y - animal.y)
        if distance <= 1:
            animal.heal()
            self.status = "Idle"
            self.target_id = None
            return True
        return False


class Cashier(Staff):
    """
    Kassierer. Bedient den Ticketschalter und nimmt Eintrittsgelder von Besuchern entgegen.
    """

    def __init__(self, id_: str, name: str, pos_x: int, pos_y: int) -> None:
        super().__init__(id_, name, "Cashier", pos_x, pos_y, salary=10)

    def process_ticket(self, visitor: Any) -> bool:
        """
        Bedient einen Besucher am Ticketschalter.

        :param visitor: Das Visitor-Objekt.
        :return: True, wenn das Ticket erfolgreich abgerechnet wurde, andernfalls False.
        """
        # Ist der Besucher an der Kasse (Ticketschalter)?
        # Wenn der Cashier am Schalter steht und der Besucher ebenfalls am Counter ist.
        distance = abs(self.x - visitor.x) + abs(self.y - visitor.y)
        if distance <= 1:
            self.status = "Working"
            return True
        return False
