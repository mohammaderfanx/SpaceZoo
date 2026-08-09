"""
author: Jasmin Romeyke
date: 08.08.2026
version: 1
"""

from datetime import date, timedelta
from backend.animalSimulation.illness import ExampleIllness, Illness
from typing import List


class Medicine:
    """Medicine type that treats a specific illness."""

    def __init__(self, name: str, shelfLife: int, price: int, illness: Illness):
        self.name = name
        self.shelfLife = shelfLife
        self.price = price
        self.illness = illness


class Antibiotic(Medicine):
    """Antibiotic medicine used to treat generic infections."""

    def __init__(self):
        super().__init__("Antibiotic", 30, 12, ExampleIllness())


class MedicineItem:
    """A concrete stocked quantity of a Medicine type, tracked with an expiry date."""

    def __init__(self, type: Medicine, weight: int):
        self.type = type
        self.weight = weight
        self.bestBefore = date.today() + timedelta(days=self.type.shelfLife)


