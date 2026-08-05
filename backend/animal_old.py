"""
Animal-Klasse für SpaceZoo.
Verwaltet den Zustand, Lebenszyklus, Hunger und Krankheiten eines einzelnen Tieres.
"""
from enum import Enum
import random
from typing import Optional, Tuple

class AnimalType(Enum):
    CARNIVORE = "carnivore"
    HERBIVORE = "herbivore"


class Animal:
    """
    Klasse zur Repräsentation eines Tiers der Simulation.
    """

    # Die 6 erlaubten Tierarten laut Spezifikation
    SPECIES_LIST = ["Birdy", "Liz", "Mal", "Pinky", "Rizzy", "Sami"]

    def __init__(
        self,
        id_: str,
        type: AnimalType, 
        species: str,
        name: str,
        pos_x: int,
        pos_y: int,
        age_seconds: float = 0.0,
        hunger: float = 0.0,
        hunger_timer: float = 10.0,
        is_sick: bool = False,
        sick_timer: float = 15.0,
    ) -> None:
        """
        Initialisiert ein Tier.

        :param id_: Eindeutige ID des Tieres.
        :param species: Art des Tieres (muss in SPECIES_LIST sein).
        :param name: Name des Tieres.
        :param pos_x: X-Koordinate auf dem Grid.
        :param pos_y: Y-Koordinate auf dem Grid.
        :param age_seconds: Alter in Sekunden (15 min Lebenszyklus = 900s).
        :param hunger: Hungergrad (0.0 bis 100.0).
        :param hunger_timer: Countdown-Sekunden bis zum Tod bei 100% Hunger (Standard: 10s).
        :param is_sick: Krankheitsstatus.
        :param sick_timer: Countdown-Sekunden bis zum Tod bei Krankheit (Standard: 15s).
        """
        if species not in self.SPECIES_LIST:
            raise ValueError(
                f"Ungültige Tierart: {species}. Erlaubt sind: {self.SPECIES_LIST}"
            )

        self.id = id_
        self.species = species
        self.name = name
        self.x = pos_x
        self.y = pos_y

        # Lebenszyklus (15 min insgesamt = 900 Sekunden)
        # Kind: 0-300s (0-5 min), Erwachsen: 300-600s (5-10 min), Alt: 600-900s (10-15 min)
        self.age_seconds = age_seconds

        # Hunger-System
        self.hunger = hunger
        self.hunger_timer = hunger_timer

        # Krankheits-System
        self.is_sick = is_sick
        self.sick_timer = sick_timer

    @property
    def life_stage(self) -> str:
        """
        Berechnet die aktuelle Lebensphase basierend auf dem Alter in Sekunden.
        """
        if self.age_seconds < 300.0:
            return "Kind"
        elif self.age_seconds < 600.0:
            return "Erwachsen"
        else:
            return "Alt"

    @property
    def is_dead(self) -> bool:
        """
        Gibt an, ob das Tier gestorben ist (Alter überschritten, Hunger oder Krankheit abgelaufen).
        """
        if self.age_seconds >= 900.0:
            return True
        if self.hunger >= 100.0 and self.hunger_timer <= 0.0:
            return True
        if self.is_sick and self.sick_timer <= 0.0:
            return True
        return False

    def tick(self, delta_time: float) -> None:
        """
        Aktualisiert den Zustand des Tieres basierend auf der vergangenen Zeit.

        :param delta_time: Vergangene Zeit in Sekunden.
        """
        if self.is_dead:
            return

        # Alter erhöhen
        self.age_seconds += delta_time

        # Hunger steigt kontinuierlich (z.B. 1% pro Sekunde)
        if self.hunger < 100.0:
            self.hunger = min(100.0, self.hunger + 1.0 * delta_time)

        # Hunger-Todes-Timer herunterzählen, wenn Hunger bei 100% ist
        if self.hunger >= 100.0:
            self.hunger_timer = max(0.0, self.hunger_timer - delta_time)

        # Krankheitstimer herunterzählen, wenn krank
        if self.is_sick:
            self.sick_timer = max(0.0, self.sick_timer - delta_time)
        else:
            # Zufällige Chance zu erkranken, falls noch gesund (z.B. 0.1% Chance pro Sekunde)
            if random.random() < 0.001 * delta_time:
                self.is_sick = True
                self.sick_timer = 15.0

    def feed(self) -> None:
        """
        Füttert das Tier. Setzt den Hunger auf 0% und den Hunger-Timer zurück.
        """
        self.hunger = 0.0
        self.hunger_timer = 10.0

    def heal(self) -> None:
        """
        Heilt das Tier von einer Krankheit. Setzt den Krankheitsstatus und den Timer zurück.
        """
        self.is_sick = False
        self.sick_timer = 15.0

    def to_dict(self) -> dict:
        """
        Serialisiert das Tier in ein Dictionary zur Kommunikation mit dem Frontend.
        """
        return {
            "id": self.id,
            "species": self.species,
            "name": self.name,
            "age_seconds": self.age_seconds,
            "life_stage": self.life_stage,
            "hunger": self.hunger,
            "hunger_timer": self.hunger_timer,
            "is_sick": self.is_sick,
            "sick_timer": self.sick_timer,
            "position": (self.x, self.y),
        }
