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
        """Returns whether the inventory holds medicine for the given illness.

        Args:
            self
            illness: the illness type to check stock for

        Returns:
            bool: True if at least one matching medicine item is in stock

        Tests:
            matching medicine in stock -> returns True
            no matching medicine in stock -> returns False
        """
        medicineForIllness = [medicine for medicine in self.medicine if type[medicine.illness] == illness]
        return len(medicineForIllness) > 0

    def listOfFoodInCategory(self, category: type[Food]) -> List[FoodItem]:
        """Returns the inventory's food items in the given category, sorted by expiry.

        Args:
            self
            category: the food category to filter by

        Returns:
            List[FoodItem]: matching food items ordered by soonest expiry first

        Tests:
            multiple matching items -> returns them sorted by bestBefore ascending
            no matching items -> returns an empty list
        """
        listOfFood = [food for food in self.food if type[self.food] == category]
        return listOfFood.sort(lambda food: food.bestBefore)
