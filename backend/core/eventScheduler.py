"""
author: Jasmin Romeyke
date: 08.08.2026
version: 1
"""

import random
from typing import List

from backend.animalSimulation.animal import Animal
from backend.animalSimulation.habits import FoodPreference
from backend.animalSimulation.illness import ExampleIllness
from backend.core.zoo import Zoo
from backend.zooManagement.employee import Caretaker, WorkingHours, Employee
from backend.zooManagement.food import FoodItem, Meat, Hay, Fish

class EventScheduler:
    """Triggers time-based zoo events such as feeding, aging, and visitor arrivals/departures."""

    def __init__(self, zoo: Zoo):
        self.zoo = zoo

    def scheduleEvents(self, elapsedDays: int, elapsedHours: int):
        """Dispatches time-based events for the current hour.

        Args:
            elapsedDays: number of full days elapsed in the simulation
            elapsedHours: current hour of the simulation day

        Tests:
            elapsedHours is 0 -> animals are aged up
            elapsedHours is 8 -> visitors arrive
            elapsedHours is 17 -> visitors leave
            any elapsedHours value -> animals due for feeding get fed
        """
        if elapsedHours == 0:
            self.ageUpAnimals(elapsedDays)
        if elapsedHours == 8:
            self.visitorsArrive()
        if elapsedHours == 17:
            self.visitorsLeave()
        self.feedAnimals(elapsedHours, elapsedDays)
        self.animalsSleep(elapsedHours)



    def feedAnimals(self, elapsedHours: int, elapsedDays: int):
        """Feeds all animals due for feeding using available caretakers."""

        animalsToFeed: List[Animal] = []
        for animal in self.zoo.animals:
            if elapsedHours in animal.habits.eatingHabit.feedingTimes:
                animalsToFeed.append(animal)

        if len(animalsToFeed) == 0:
            return

        availableCaretakers = self.zoo.getCaretakers()
        if len(availableCaretakers) == 0:
            return

        for indexAnimal, currentAnimal in enumerate(animalsToFeed):
            currentCaretaker = availableCaretakers[indexAnimal % len(availableCaretakers)]
            percent = self.__determineHungerQuelled(currentAnimal, elapsedDays)
            currentCaretaker.feedAnimal(currentAnimal, percent)
         
        
    def __determineHungerQuelled(self, currentAnimal: Animal, elapsedDays: int) -> float:
        """Calculates the fraction of required feeding that available food can cover."""
        preference = currentAnimal.habits.eatingHabit.foodPreference
        if preference == FoodPreference.CARNIVORE:
            food_categories = [Meat]
        elif preference == FoodPreference.HERBIVORE:
            food_categories = [Hay]
        else:
            food_categories = [Meat, Hay, Fish]

        requiredFood = currentAnimal.getLifecyclePhase(elapsedDays).requiredFoodPerFeeding
        additionalFoodNeeded = requiredFood
        possibleFoodForAnimal: List[FoodItem] = []
        for food_cls in food_categories:
            possibleFoodForAnimal.extend(self.zoo.inventory.listOfFoodInCategory(food_cls))

        for currentFoodItem in list(possibleFoodForAnimal):
            if additionalFoodNeeded <= 0:
                break
            amount = min(additionalFoodNeeded, currentFoodItem.weight)
            currentFoodItem.weight -= amount
            additionalFoodNeeded -= amount
            if currentFoodItem.weight <= 0 and currentFoodItem in self.zoo.inventory.food:
                self.zoo.inventory.food.remove(currentFoodItem)

        if requiredFood <= 0:
            return 1.0
        return max(0.0, min(1.0, (requiredFood - additionalFoodNeeded) / requiredFood))


    def animalsSleep(self, elapsedHours: int):
        """Checks which animals to put to sleep or wake up at the current time.
        
        Args: 
            self
            elapsedHours: current time of day in hours
              
        Returns: 
            None
        
        Tests:
            animals due for sleeping -> animals sleep
            no animals due for sleeping -> method returns without any animal sleeping
            animals due for waking -> animals wake
            no animals due for waking -> method returns without any animal waking
            """
        animalsToPutToSleep = [animal for animal in self.zoo.animals if animal.habits.sleepingHabit.hourOfFallingAsleep == elapsedHours]
        for animal in animalsToPutToSleep:
            animal.sleep()

        animalsToPutWake = [animal for animal in self.zoo.animals if animal.habits.sleepingHabit.hourOfWaking == elapsedHours]
        for animal in animalsToPutWake:
            animal.wake()
                

        
    def ageUpAnimals(self, elapsedDays: int):
        """Advances animals to their next lifecycle phase when due.

        Args:
            self
            elapsedDays: number of full days elapsed in the simulation

        Tests:
            animal's age matches the end of its current phase -> animal ages up
            animal younger than its phase boundary -> animal stays in its current phase
        """
        for animal in self.zoo.animals:
            age = elapsedDays - animal.birthdate
            if age == animal.getLifecyclePhase(elapsedDays).endOfPhaseAge:
                animal.age(elapsedDays)


    def visitorsArrive(self):
        """Lets visitors into the zoo for cashiers to sell tickets to.

        Args:
            self

        Tests:
            cashiers available -> visitors are let in and tickets get sold
            no cashiers available -> visitors cannot buy tickets
        """
        availableCashiers = self.zoo.getCashiers()
        if len(availableCashiers) == 0:
            return
        ticketPrice = 5
        newVisitors = int(self.zoo.score)
        for index in range(newVisitors):
            cashier = availableCashiers[index % len(availableCashiers)]
            cashier.sellTicket()
            self.zoo.visitors += 1
            self.zoo.budget += ticketPrice

    def visitorsLeave(self):
        """Sends visitors home.

        Args:
            self

        Tests:
            visitors present -> visitor count drops to 0
            no visitors present -> no-op
        """
        self.zoo.visitors = 0
   
