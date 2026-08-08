from zoo import Zoo
from employee import Caretaker, WorkingHours, Employee
from animal import Animal
from food import FoodItem
from typing import List

class EventScheduler:

    def __init__(self, zoo: Zoo):
        self.zoo = zoo

    def scheduleEvents(self, elapsedDays: int, elapsedHours: int):
        if elapsedHours == 0:
            self.ageUpAnimals(elapsedDays)
        if elapsedHours == 8:
            self.visitorsArrive()
        if elapsedHours == 17:
            self.visitorsLeave()
        self.feedAnimals(elapsedHours)



    def feedAnimals(self, elapsedHours: int):

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
            currentCaretaker.feedAnimal(currentAnimal, self.determineHungerQuelled(currentAnimal))
         
        
    def determineHungerQuelled(self, currentAnimal: Animal):
            foodPreference = currentAnimal.habits.eatingHabit.foodPreference.name
            requiredFood = currentAnimal.getLifecyclePhase().requiredFoodPerFeeding
            additionalFoodNeeded = requiredFood
            possibleFoodForAnimal: List[FoodItem] = []
            for foodItem in self.zoo.inventory.food:
                if foodItem.type.foodPreference.__contains__(foodPreference):
                    possibleFoodForAnimal.append(foodItem)
            possibleFoodForAnimal.sort(foodItem.bestBefore) # ka ob so richtig
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
        for animal in self.zoo.animals:
            age = elapsedDays - animal.birthdate
            if age == animal.getLifecyclePhase().endOfPhaseAge:
                animal.age()


    def visitorsArrive(self):
        """Kommen halt so ein paar Visitors, Cashiers machen ihr Ding"""

    def visitorsLeave(self):
        """gehen wieder"""
    #,,,,,äääh nein mein kind ich hab dir diesen roten apfel mitgebracht weil dun soo lieeeeb bist <3
