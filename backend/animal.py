from enum import Enum
from simulation_engine import get_current_day
from illness import Illness
from lifecycle import Lifecycle, LifecyclePhase


class AnimalType(Enum):
    CARNIVORE = "carnivore"
    HERBIVORE = "herbivore"


class Animal:
    def __init__(self, id_: str, name: str, birthdate = get_current_day()):
            self.id = id_
            self.name = name
            self.birthdate = birthdate
            self.hunger = 0
            self.illness: Illness = None
            self.animalType: AnimalType
            self.lifecycle: Lifecycle


class Birdy(Animal):
    def __init__(self, id_: str, name: str, birthdate = get_current_day()):
        super().__init__(id_, name, birthdate)
        self.animalType = AnimalType.HERBIVORE
        self.lifecycle = Lifecycle(LifecyclePhase(4, 1, 0.4),
                                   LifecyclePhase(8, 2, 1),
                                   LifecyclePhase(13, 2, 1.4))

class Sami(Animal):
    def __init__(self, id_: str, name: str, birthdate = get_current_day()):
        super().__init__(id_, name, birthdate)
        self.animalType = AnimalType.CARNIVORE
        self.lifecycle = Lifecycle(LifecyclePhase(6, 3, 0.4),
                                   LifecyclePhase(15, 8, 1),
                                   LifecyclePhase(20, 6, 1.4))
        