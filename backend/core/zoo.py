"""
author: Jasmin Romeyke
date: 08.08.2026
version: 1
"""


from typing import List
import statistics

from backend.animalSimulation.animal import Animal, Gender
from backend.zooManagement.employee import Employee, Caretaker, Vet, Cashier, WorkingHours
from backend.zooManagement.inventory import Inventory
from backend.zooManagement.enclosure import Enclosure
from backend.zooManagement.food import Food, FoodItem
from backend.zooManagement.medicine import Medicine
from backend.animalSimulation.egg import Egg
from backend.animalSimulation.environmentalFactors import EnvironmentalFactors

class Zoo:
    """Central aggregate holding the zoo's animals, staff, enclosures, inventory, and budget, as well as environmental factors and the current visitor score."""

    def __init__(self):
        self.budget = 100
        self.animals: List[Animal] = []
        self.staff: List[Employee] = []
        self.enclosures: List[Enclosure] = []
        self.visitors: int = 0
        self.inventory: Inventory = Inventory()
        self.eggs: List[Egg] = []
        self.environment: EnvironmentalFactors = EnvironmentalFactors()
        self.score: float = 0

    def __getEmployeesByType(self, typeOfEmployee: type[Employee]):
            """Returns staff of the given type who are on shift and not busy.

            Args:
                self
                typeOfEmployee: the Employee subclass to filter by

            Returns:
                list: matching employees currently on shift and free

            Tests:
                matching employees on shift and free -> included in result
                matching employees off shift or busy -> excluded from result
            """
            return [employee for employee in self.staff if isinstance(employee, typeOfEmployee) and employee.isOnShift() and employee.busyFor == 0]

    def getCaretakers(self) -> List[Caretaker]:
        """Returns all available caretakers.

        Args:
            self

        Returns:
            List[Caretaker]: caretakers currently on shift and free

        Tests:
            caretakers on shift and free -> included in result
            caretakers off shift or busy -> excluded from result
        """
        return self.__getEmployeesByType(Caretaker)

    def getVets(self) -> List[Vet]:
            """Returns all available vets.

            Args:
                self

            Returns:
                List[Vet]: vets currently on shift and free

            Tests:
                vets on shift and free -> included in result
                vets off shift or busy -> excluded from result
            """
            return self.__getEmployeesByType(Vet)

    def getCashiers(self) -> List[Cashier]:
            """Returns all available cashiers.

            Args:
                self

            Returns:
                List[Cashier]: cashiers currently on shift and free

            Tests:
                cashiers on shift and free -> included in result
                cashiers off shift or busy -> excluded from result
            """
            return self.__getEmployeesByType(Cashier)

    def animalDies(self, animal: Animal):
        """Removes the given animal from the zoo.

        Args:
            self
            animal: the animal that died

        Tests:
            animal is in self.animals -> it gets removed
            animal not in self.animals -> raises ValueError
        """
        self.animals.remove(animal)


    def buyNewAnimal(self, animalType: type[Animal], name: str, birthdate: int, gender: Gender):
        """Buys an animal with given species, gender and name.

        Args:
            self
            animalType: the Animal subclass to buy, carrying its purchase price as a class attribute
            name: name for the new animal
            birthdate: day that the animal was born, determines age
            gender: gender of the new animal

        Tests:
            budget covers the chosen animal -> animal is added to the zoo
            budget insufficient -> purchase is rejected
        """
        newAnimal = animalType(name, birthdate, gender)
        if self.budget < newAnimal.price:
            return
        self.budget -= newAnimal.price
        self.animals.append(newAnimal)

    def sellAnimal(self, animal: Animal):
          """Sells a chosen animal.

          Args:
              self
              animal: the animal to sell

          Tests:
              chosen animal exists in the zoo -> animal is removed and budget increases
              no animal selected -> no-op
          """
          if animal not in self.animals:
              return
          self.budget += animal.price // 2
          self.animals.remove(animal)

    def hireEmployee(self, employeeType: type[Employee], name: str, workingHours: WorkingHours):
         """Hires a new employee.

         Args:
             self
             employeeType: the Employee subclass to hire
             name: name of the new employee
             workingHours: the new employee's shift hours

         Tests:
             valid employee data provided -> employee is added to staff
             invalid employee data -> hire is rejected
         """
         if not name:
             return
         if not (0 <= workingHours.startOfShift <= 23) or not (0 <= workingHours.endOfShift <= 23):
             return
         self.staff.append(employeeType(name, workingHours))

    def buyFood(self, foodType: type[Food], weight: int, elapsedDays: int):
          """Buys chosen food items and adds them to the inventory.

          Args:
              self
              foodType: the Food subclass to buy
              weight: kilograms to buy
              elapsedDays: number of full days elapsed in the simulation, used to compute the food's expiry

          Tests:
              budget covers the chosen food -> items are added to inventory
              budget insufficient -> purchase is rejected
          """
          foodInstance = foodType()
          totalPrice = foodInstance.pricePerKg * weight
          if self.budget < totalPrice:
              return
          self.budget -= totalPrice
          self.inventory.food.append(FoodItem(foodInstance, weight, elapsedDays))

    def buyMedicine(self, medicine: Medicine, quantity: int):
          """Buys chosen medicine items and adds them to the inventory.

          Args:
              self
              medicine: the medicine to buy
              quantity: number of units to buy

          Tests:
              budget covers the chosen medicine -> items are added to inventory
              budget insufficient -> purchase is rejected
          """
          totalPrice = medicine.price * quantity
          if self.budget < totalPrice:
              return
          self.budget -= totalPrice
          for _ in range(quantity):
              self.inventory.medicine.append(medicine)

    def healAnimal(self, animal: Animal):
        """Heals the given animal by consuming matching medicine from inventory.

        Args:
            animal: the animal to heal

        Returns:
            bool: True if the animal was healed, False otherwise.

        Tests:
            animal has no illness -> returns False and inventory is unchanged
            matching medicine in stock -> illness is removed and medicine consumed
            no matching medicine in stock -> returns False
        """
        if animal.illness is None:
            return False

        matching_medicine = [med for med in self.inventory.medicine if type(med.illness) == type(animal.illness)]
        if not matching_medicine:
            return False

        self.inventory.medicine.remove(matching_medicine[0])
        animal.illness = None
        animal.health = min(1.0, animal.health + 0.3)
        return True
       
