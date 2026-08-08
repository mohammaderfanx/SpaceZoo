"""
author: Jasmin Romeyke
date: 08.08.2026
version: 1
"""

from enum import Enum
from animalSimulation.illness import Illness
from animalSimulation.lifecycle import Lifecycle, LifecyclePhase
from animalSimulation.habits import Habits, SleepingHabit, EatingHabit, FoodPreference

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
            self.health = 1
            self.energy = 1
            self.illness: Illness = None
            self.lifecycle: Lifecycle
            self.habits: Habits
            self.awake: bool = True

    def getLifecyclePhase(self, elapsedDays):
        """Returns the animal's current lifecycle phase based on its age.

        Args:
            self
            elapsedDays: number of full days elapsed in the simulation

        Returns:
            LifecyclePhase: the phase (child, adult, or senior) matching the animal's current age

        Tests:
            age below childPhase.endOfPhaseAge -> returns childPhase
            age below adultPhase.endOfPhaseAge but at or beyond childPhase.endOfPhaseAge -> returns adultPhase
            age at or beyond adultPhase.endOfPhaseAge -> returns seniorPhase
        """
        age = elapsedDays - self.birthdate
        if age < self.lifecycle.childPhase.endOfPhaseAge:
            return self.lifecycle.childPhase
        elif age < self.lifecycle.adultPhase.endOfPhaseAge:
            return self.lifecycle.adultPhase
        else:
            return self.lifecycle.seniorPhase

         
    def feed(self, percentHungerQuelled: float):
        """Sets the animal's saturation to the percentage of hunger quelled.

        Args:
            self
            percentHungerQuelled: fraction of the animal's hunger that gets satisfied

        Tests:
            percentHungerQuelled is 1.0 -> saturation is set to 1.0
            percentHungerQuelled is 0.0 -> saturation is set to 0.0
        """
        self.saturation = percentHungerQuelled

    def sleep(self):
        """Puts the animal to sleep.

        Args:
            self

        Tests:
            called while awake -> animal's energy increases
            called while asleep -> no-op
        """

    def wake(self):
        """Puts the animal to sleep.
         
        Args:
            self

        Tests:
            called while asleep -> animal wakes, energy stops increasing
            called while awake -> no-op
        """

    def age(self):
         """Advances the animal to its next lifecycle phase.

         Args:
             self

         Tests:
             animal reaches the end of its current phase -> lifecycle phase advances
             called on a senior animal -> animal dies
         """

    def layEgg(self):
        """Lays an egg, called externally by the SimulationEngine.

        Args:
            self

        Tests:
            conditions for laying are met -> a new Egg is added to the zoo
            conditions not met -> no egg is created
        """

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
