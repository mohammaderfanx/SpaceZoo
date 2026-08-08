"""
author: Jasmin Romeyke
date: 08.08.2026
version: 1
"""


from typing import List

from animalSimulation.animal import Animal
from zooManagement.employee import Employee, Caretaker, Vet, Cashier
from zooManagement.inventory import Inventory
from zooManagement.enclosure import Enclosure
from animalSimulation.egg import Egg
from animalSimulation.environmentalFactors import EnvironmentalFactors

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
            return [employee for employee in self.staff if type[employee] == typeOfEmployee and employee.isOnShift() and employee.busyFor == 0]

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


    def buyNewAnimal(self):
        """Lets the player choose and buy a new animal from the known types.

        Args:
            self

        Tests:
            budget covers the chosen animal -> animal is added to the zoo
            budget insufficient -> purchase is rejected
        """

    def sellAnimal(self):
          """Sells a chosen animal.

          Args:
              self

          Tests:
              chosen animal exists in the zoo -> animal is removed and budget increases
              no animal selected -> no-op
          """

    def hireEmployee(self):
         """Hires a new employee.

         Args:
             self

         Tests:
             valid employee data provided -> employee is added to staff
             invalid employee data -> hire is rejected
         """

    def buyFood(self):
          """Buys chosen food items and adds them to the inventory.

          Args:
              self

          Tests:
              budget covers the chosen food -> items are added to inventory
              budget insufficient -> purchase is rejected
          """

    def buyMedicine(self):
          """Buys chosen medicine items and adds them to the inventory.

          Args:
              self

          Tests:
              budget covers the chosen medicine -> items are added to inventory
              budget insufficient -> purchase is rejected
          """

    def healAnimal(self, animal: Animal):
        """Heals the given animal using an available vet if matching medicine is in stock.

        Args:
            self
            animal: the animal to heal

        Tests:
            animal has no illness -> method returns immediately, no vet used
            matching medicine in stock and vet available -> animal gets healed and medicine is consumed
            illness present but no matching medicine -> animal remains unhealed
        """
        if animal.illness == None:
          return
        if self.inventory.checkForMedicineForSpecificIllness(animal.illness):
            availableVets = self.getVets()
            availableVets[0].healAnimal(animal)
            self.inventory.medicine.remove(medicine for medicine in self.inventory.medicine if type[medicine.illness] == type[animal.illness])
       
