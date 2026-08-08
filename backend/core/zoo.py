from typing import List

from backend.animalSimulation.animal import Animal
from backend.zooManagement.employee import Employee, Caretaker, Vet, Cashier
from backend.zooManagement.inventory import Inventory
from backend.zooManagement.enclosure import Enclosure
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
        self.inventory: Inventory
        self.eggs: List[Egg] = []
        self.environment: EnvironmentalFactors = EnvironmentalFactors()
        self.score: float = 0

    def __getEmployeesByType(self, typeOfEmployee: type[Employee]):
            """Returns staff of the given type who are on shift and not busy."""
            return [employee for employee in self.staff if type[employee] == typeOfEmployee and employee.isOnShift() and employee.busyFor == 0]

    def getCaretakers(self) -> List[Caretaker]:
        """Returns all available caretakers."""
        return self.__getEmployeesByType(Caretaker)

    def getVets(self) -> List[Vet]:
            """Returns all available vets."""
            return self.__getEmployeesByType(Vet)

    def getCashiers(self) -> List[Cashier]:
            """Returns all available cashiers."""
            return self.__getEmployeesByType(Cashier)

    def animalDies(self, animal: Animal):
        """Removes the given animal from the zoo."""
        self.animals.remove(animal)


    def buyNewAnimal(self):
        """Lets the player choose and buy a new animal from the known types."""

    def sellAnimal(self):
          """Sells a chosen animal."""

    def hireEmployee(self):
         """Hires a new employee."""

    def buyFood(self):
          """Buys chosen food items and adds them to the inventory."""

    def buyMedicine(self):
          """Buys chosen medicine items and adds them to the inventory."""

    def healAnimal(self, animal: Animal):
        """Heals the given animal using an available vet if matching medicine is in stock."""
        if animal.illness == None:
          return
        if self.inventory.checkForMedicineForSpecificIllness(animal.illness):
            availableVets = self.getVets()
            availableVets[0].healAnimal(animal)
            self.inventory.medicine.remove(medicine for medicine in self.inventory.medicine if type[medicine.illness] == type[animal.illness])
       
