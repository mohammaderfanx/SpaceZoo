from zoo import Zoo
from backend.zooManagement.employee import Caretaker, WorkingHours, Employee
from backend.animalSimulation.animal import Animal
from backend.zooManagement.food import FoodItem
from typing import List

class EventScheduler:
    """Triggers time-based zoo events such as feeding, aging, and visitor arrivals/departures."""

    def __init__(self, zoo: Zoo):
        self.zoo = zoo

    def scheduleEvents(self, elapsedDays: int, elapsedHours: int):
        """Dispatches time-based events for the current hour."""
        if elapsedHours == 0:
            self.ageUpAnimals(elapsedDays)
        if elapsedHours == 8:
            self.visitorsArrive()
        if elapsedHours == 17:
            self.visitorsLeave()
        self.feedAnimals(elapsedHours)



    def feedAnimals(self, elapsedHours: int):
        """Feeds all animals due for feeding using available caretakers."""

        animalsToFeed: List[Animal] = []
        for animal in self.zoo.animals:
            if animal.habits.eatingHabit.feedingTimes.__contains__(elapsedHours):
                animalsToFeed.append(animal)

        if len(animalsToFeed) == 0:
            return # no animal needs feeding
        
        availableCaretakers = self.zoo.getCaretakers()

        if len(availableCaretakers) == 0:
            return # no caretaker to feed animals

        for indexAnimal in range(len(animalsToFeed)):
            currentAnimal = animalsToFeed[indexAnimal]
            # check if enough food
            currentCaretaker = availableCaretakers[indexAnimal % len(availableCaretakers)]
            currentCaretaker.feedAnimal(currentAnimal, self.__determineHungerQuelled(currentAnimal))
         
        
    def __determineHungerQuelled(self, currentAnimal: Animal):
            """Calculates the percentage of the animal's hunger satisfied by available food."""
            foodPreference = currentAnimal.habits.eatingHabit.foodPreference.name
            requiredFood = currentAnimal.getLifecyclePhase().requiredFoodPerFeeding
            additionalFoodNeeded = requiredFood
            possibleFoodForAnimal = self.zoo.inventory.listOfFoodInCategory(type[foodPreference])
            assignedFood = 0
            while additionalFoodNeeded > assignedFood and len(possibleFoodForAnimal) != 0:
                currentFoodItem = possibleFoodForAnimal.pop(0)
                currentFoodItem.weight -= additionalFoodNeeded
                additionalFoodNeeded = -currentFoodItem.weight
                if currentFoodItem.weight <= 0:
                    self.zoo.inventory.food.remove(currentFoodItem)
            if additionalFoodNeeded < 0:
                additionalFoodNeeded = 0
            percentHungerQuelled = (requiredFood - additionalFoodNeeded) / requiredFood # is 1 if enough food
            return percentHungerQuelled

    
    def ageUpAnimals(self, elapsedDays: int):
        """Advances animals to their next lifecycle phase when due."""
        for animal in self.zoo.animals:
            age = elapsedDays - animal.birthdate
            if age == animal.getLifecyclePhase().endOfPhaseAge:
                animal.age()


    def visitorsArrive(self):
        """Lets visitors into the zoo for cashiers to sell tickets to."""

    def visitorsLeave(self):
        """Sends visitors home."""
    #,,,,,äääh nein mein kind ich hab dir diesen roten apfel mitgebracht weil dun soo lieeeeb bist <3
