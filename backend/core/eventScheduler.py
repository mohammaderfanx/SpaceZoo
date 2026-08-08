from core.zoo import Zoo
from zooManagement.employee import Caretaker, WorkingHours, Employee
from animalSimulation.animal import Animal
from zooManagement.food import FoodItem
from typing import List

class EventScheduler:
    """Triggers time-based zoo events such as feeding, aging, and visitor arrivals/departures."""

    def __init__(self, zoo: Zoo):
        self.zoo = zoo

    def scheduleEvents(self, elapsedDays: int, elapsedHours: int):
        """Dispatches time-based events for the current hour.

        Args:
            self
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
        self.feedAnimals(elapsedHours)
        self.animalsSleep(elapsedHours)



    def feedAnimals(self, elapsedHours: int):
        """Feeds all animals due for feeding using available caretakers.

        Args:
            self
            elapsedHours: current hour of the simulation day

        Tests:
            animals due for feeding and caretakers available -> caretakers feed them
            no animals due for feeding -> method returns without feeding
            animals due for feeding but no caretakers available -> method returns without feeding
        """

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
            """Calculates the percentage of the animal's hunger satisfied by available food.

            Args:
                self
                currentAnimal: the animal being fed

            Returns:
                float: fraction of the required food that could be supplied, capped at 1

            Tests:
                enough matching food in inventory -> returns 1
                no matching food in inventory -> returns 0
                partial matching food in inventory -> returns a value between 0 and 1
            """
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
        for animal in animalsToPutToSleep:
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
            if age == animal.getLifecyclePhase().endOfPhaseAge:
                animal.age()


    def visitorsArrive(self):
        """Lets visitors into the zoo for cashiers to sell tickets to.

        Args:
            self

        Tests:
            cashiers available -> visitors are let in and tickets get sold
            no cashiers available -> visitors cannot buy tickets
        """

    def visitorsLeave(self):
        """Sends visitors home.

        Args:
            self

        Tests:
            visitors present -> visitor count drops to 0
            no visitors present -> no-op
        """
    #,,,,,äääh nein mein kind ich hab dir diesen roten apfel mitgebracht weil dun soo lieeeeb bist <3
