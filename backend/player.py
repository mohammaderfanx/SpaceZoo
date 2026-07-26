"""
Player-Klasse für SpaceZoo.
Repräsentiert den Spieler in der 2D-Welt auf dem Grid.
"""

from typing import Tuple


class Player:
    """
    Repräsentiert die Spielfigur, die sich auf dem 21x16 Grid bewegt.
    """

    def __init__(self, start_x: int = 10, start_y: int = 8) -> None:
        """
        Initialisiert den Spieler an einer bestimmten Grid-Position.

        :param start_x: Start-X-Koordinate (Standard: 10)
        :param start_y: Start-Y-Koordinate (Standard: 8)
        """
        self.x = start_x
        self.y = start_y

    def move(self, dx: int, dy: int, grid_width: int = 21, grid_height: int = 16) -> Tuple[int, int]:
        """
        Bewegt den Spieler relativ um dx, dy unter Einhaltung der Spielfeldgrenzen.

        :param dx: Änderung auf der X-Achse (-1, 0, 1)
        :param dy: Änderung auf der Y-Achse (-1, 0, 1)
        :param grid_width: Maximale Feldbreite des Grids (Standard: 21)
        :param grid_height: Maximale Feldhöhe des Grids (Standard: 16)
        :return: Neue Position als (x, y) Tuple.
        """
        new_x = max(0, min(grid_width - 1, self.x + dx))
        new_y = max(0, min(grid_height - 1, self.y + dy))
        self.x = new_x
        self.y = new_y
        return (self.x, self.y)

    def get_position(self) -> Tuple[int, int]:
        """
        Gibt die aktuelle Grid-Position des Spielers zurück.
        """
        return (self.x, self.y)

    def to_dict(self) -> dict:
        """
        Konvertiert die Spielerdaten in ein Dictionary für das Frontend.
        """
        return {
            "position": (self.x, self.y),
            "x": self.x,
            "y": self.y
        }
