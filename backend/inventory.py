from typing import List
from food import FoodItem
from medicine import Medicine

class Inventory:
    def __init__(self):
        self.food: List[FoodItem] = []
        self.medicine: List[Medicine] = []