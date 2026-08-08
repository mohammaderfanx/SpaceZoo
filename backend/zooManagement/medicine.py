
from datetime import date, timedelta
from animalSimulation.illness import Illness
from typing import List


class Medicine:
    """Medicine type that treats a specific illness."""

    def __init__(self, name: str, shelfLife: int, price: int, illness: Illness):
        self.name = name
        self.shelfLife = shelfLife
        self.price = price
        self.illness = illness

class ExampleMedicine:
    """Sample Medicine preset used for testing/demo purposes."""

    def __init__(self):
        super().__init__("Medicine against ExampleIllness", 30, 12, ExampleMedicine)


class MedicineItem:
    """A concrete stocked quantity of a Medicine type, tracked with an expiry date."""

    def __init__(self, type: Medicine, weight: int):
        self.type = type
        self.weight = weight
        self.bestBefore = date.today() + timedelta(days = self.type.shelfLife)


