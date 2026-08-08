from animalSimulation.habits import FoodPreference
from typing import List

class Food:
    """Food type defining which diets it suits, its shelf life, and price per kg."""

    def __init__(self, name: str, foodPreference: List[FoodPreference], shelfLife: int, pricePerKg: int):
        self.name = name
        self.foodPreference = foodPreference
        self.shelfLife = shelfLife
        self.pricePerKg = pricePerKg


class Meat(Food):
    """Food preset for carnivores and omnivores."""

    def __init__(self):
        super().__init__("Meat", [FoodPreference.CARNIVORE, FoodPreference.OMNIVORE], 10, 3)

class Hay(Food):
    """Food preset for herbivores and omnivores."""

    def __init__(self):
        super().__init__("Hay", [FoodPreference.HERBIVORE, FoodPreference.OMNIVORE], 25, 1)

class Fish(Food):
    """Food preset for carnivores and omnivores."""

    def __init__(self):
        super().__init__("Fish", [FoodPreference.CARNIVORE, FoodPreference.OMNIVORE], 7, 5)



class FoodItem:
    """A concrete stocked quantity of a Food type, tracked with weight, price, and expiry."""

    def __init__(self, type: Food, weight: int, elapsedDays: int):
        self.type = type
        self.weight = weight
        self.bestBefore = elapsedDays + self.type.shelfLife
        self.price = self.type.pricePerKg * self.weight

