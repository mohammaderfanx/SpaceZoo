
from datetime import date, timedelta
from illness import Illness
from typing import List


class Medicine:
    def __init__(self, name: str, shelfLife: int, price: int, illness: Illness):
        self.name = name
        self.shelfLife = shelfLife
        self.price = price
        self.illness = illness

class ExampleMedicine:
    def __init__(self):
        super().__init__("Medicine against ExampleIllness", 30, 12, ExampleMedicine)


class MedicineItem:
    def __init__(self, type: Medicine, weight: int):
        self.type = type
        self.weight = weight
        self.bestBefore = date.today() + timedelta(days = self.type.shelfLife)


