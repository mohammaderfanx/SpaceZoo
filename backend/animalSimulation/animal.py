from enum import Enum
from backend.animalSimulation.illness import Illness
from backend.animalSimulation.lifecycle import Lifecycle, LifecyclePhase
from backend.animalSimulation.habits import Habits, SleepingHabit, EatingHabit, FoodPreference

class Gender(Enum):
    """Biological sex of an animal."""

    FEMALE = "female"
    MALE = "male"

class Animal:
    """Base class for a zoo animal, tracking identity, lifecycle, health, and habits."""

    def __init__(self, id_: str, name: str, birthdate: int, gender: Gender):
            self.id = id_
            self.name = name
            self.birthdate = birthdate
            self.gender = gender
            self.saturation = 1
            self.illness: Illness = None
            self.lifecycle: Lifecycle
            self.habits: Habits

    def getLifecyclePhase(self, elapsedDays):
        """Returns the animal's current lifecycle phase based on its age."""
        age = elapsedDays - self.birthdate
        if age < self.lifecycle.childPhase.endOfPhaseAge:
            return self.lifecycle.childPhase
        elif age < self.lifecycle.adultPhase.endOfPhaseAge:
            return self.lifecycle.adultPhase
        else:
            return self.lifecycle.seniorPhase
         
    def feed(self, percentHungerQuelled: float):
        """Sets the animal's saturation to the percentage of hunger quelled."""
        self.saturation = percentHungerQuelled

    def sleep(self):
        """Puts the animal to sleep."""

    def age(self):
         """Advances the animal to its next lifecycle phase."""

    def layEgg(self):
        """Lays an egg."""

class Eagle(Animal):
    """Animal species preset: eagle, with its specific habits and lifecycle."""

    def __init__(self, id_: str, name: str, birthdate: int):
        super().__init__(id_, name, birthdate)
        self.habits = Habits(SleepingHabit(5, 18), EatingHabit(FoodPreference.OMNIVORE, [6, 16]))
        self.lifecycle = Lifecycle(LifecyclePhase(4, 1, 0.4),
                                   LifecyclePhase(8, 2, 1),
                                   LifecyclePhase(13, 2, 1.4))


class Wolf(Animal):
    """Animal species preset: wolf, with its specific habits and lifecycle."""

    def __init__(self, id_: str, name: str, birthdate: int):
        super().__init__(id_, name, birthdate)
        self.habits = Habits(SleepingHabit(19, 6), EatingHabit(FoodPreference.CARNIVORE, [20, 5]))
        self.lifecycle = Lifecycle(LifecyclePhase(6, 3, 0.4),
                                   LifecyclePhase(15, 8, 1),
                                   LifecyclePhase(20, 6, 1.4))

class Rabbit(Animal):
    """Animal species preset: rabbit, with its specific habits and lifecycle."""

    def __init__(self, id_: str, name: str, birthdate: int):
            super().__init__(id_, name, birthdate)
            self.habits = Habits(SleepingHabit(10, 20), EatingHabit(FoodPreference.HERBIVORE, [20, 5]))
            self.lifecycle = Lifecycle(LifecyclePhase(1, 1, 0.4),
                                       LifecyclePhase(10, 3, 1),
                                       LifecyclePhase(15, 3, 1.4))
