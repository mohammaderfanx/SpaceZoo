"""
Visitor-Klasse für SpaceZoo.
Verwaltet den Lebenszyklus, Status und die Aktionen eines Zoo-Besuchers.
"""

from typing import Any, Dict, Tuple


class Visitor:
    """
    Repräsentiert einen Besucher des Zoos.
    """

    def __init__(
        self,
        id_: str,
        pos_x: int,
        pos_y: int,
    ) -> None:
        """
        Initialisiert einen Besucher.

        :param id_: Eindeutige ID des Besuchers.
        :param pos_x: X-Position auf dem Grid.
        :param pos_y: Y-Position auf dem Grid.
        """
        self.id = id_
        self.x = pos_x
        self.y = pos_y

        # Statusübersicht:
        # 'Queuing' (In der Warteschlange vor dem Kassenbereich)
        # 'BuyingTicket' (Direkt am Schalter, wartet 15s)
        # 'InZoo' (Bewegt sich frei im Zoo, despawnt nach 40s)
        # 'Leaving' (Auf dem Weg zum Ausgang)
        self.status = "Queuing"

        # Timer-Tracking
        self.ticket_wait_timer = 15.0  # Wartet max/genau 15s am Ticketschalter
        self.zoo_stay_timer = 40.0     # Bleibt max. 40s im Zoo

    def wait_in_line(self, delta_time: float) -> bool:
        """
        Wartet in der Schlange oder am Schalter und zieht die verbleibende Zeit ab.

        :param delta_time: Vergangene Zeit in Sekunden.
        :return: True, wenn die Wartezeit am Ticketschalter abgelaufen ist.
        """
        if self.status == "BuyingTicket":
            self.ticket_wait_timer = max(0.0, self.ticket_wait_timer - delta_time)
            if self.ticket_wait_timer <= 0.0:
                return True
        return False

    def explore_zoo(self, delta_time: float) -> bool:
        """
        Erkundet den Zoo und verringert die verbleibende Besuchszeit.

        :param delta_time: Vergangene Zeit in Sekunden.
        :return: True, wenn die Besuchszeit abgelaufen ist und der Besucher gehen will.
        """
        if self.status == "InZoo":
            self.zoo_stay_timer = max(0.0, self.zoo_stay_timer - delta_time)
            if self.zoo_stay_timer <= 0.0:
                self.status = "Leaving"
                return True
        return False

    def move_to(self, target_x: int, target_y: int) -> Tuple[int, int]:
        """
        Bewegt den Besucher einen Schritt in Richtung des Ziels.

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
        Serialisiert die Besucherdaten in ein Dictionary zur Kommunikation mit dem Frontend.
        """
        return {
            "id": self.id,
            "status": self.status,
            "ticket_wait_timer": self.ticket_wait_timer,
            "zoo_stay_timer": self.zoo_stay_timer,
            "position": (self.x, self.y),
        }
