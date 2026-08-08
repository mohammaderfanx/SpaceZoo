from typing import List
from backend.zooManagement.food import FoodItem, Food
from backend.zooManagement.medicine import Medicine
from backend.animalSimulation.illness import Illness

class Inventory:
    """Tracks the zoo's stock of food and medicine."""

    def __init__(self):
        self.food: List[FoodItem] = []
        self.medicine: List[Medicine] = []

    def checkForMedicineForSpecificIllness(self, illness: type[Illness]) -> bool:
        """Returns whether the inventory holds medicine for the given illness."""
        medicineForIllness = [medicine for medicine in self.medicine if type[medicine.illness] == illness]
        return len(medicineForIllness) > 0

    def listOfFoodInCategory(self, category: type[Food]) -> List[FoodItem]:
        """Returns the inventory's food items in the given category, sorted by expiry."""
        listOfFood = [food for food in self.food if type[self.food] == category]
        return listOfFood.sort(lambda food: food.bestBefore)
