from enum import Enum
from illness import Illness
from lifecycle import Lifecycle, LifecyclePhase
from habits import Habits, SleepingHabit, EatingHabit, FoodPreference

class Gender(Enum):
    FEMALE = "female"
    MALE = "male"

class Animal:

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
        age = elapsedDays - self.birthdate
        if age < self.lifecycle.childPhase.endOfPhaseAge:
            return self.lifecycle.childPhase
        elif age < self.lifecycle.adultPhase.endOfPhaseAge:
            return self.lifecycle.adultPhase
        else:
            return self.lifecycle.seniorPhase
         
    def feed(self, percentHungerQuelled: float):
        self.saturation = percentHungerQuelled

    def sleep(self):
        """"""

    def age(self):
         """"""

    def layEgg(self):
        """wird von außen (SimulationEngine) aufgerufen"""

class Birdy(Animal):

    def __init__(self, id_: str, name: str, birthdate: int):
        super().__init__(id_, name, birthdate)
        self.habits = Habits(SleepingHabit(5, 18), EatingHabit(FoodPreference.OMNIVORE, [6, 16]))
        self.lifecycle = Lifecycle(LifecyclePhase(4, 1, 0.4),
                                   LifecyclePhase(8, 2, 1),
                                   LifecyclePhase(13, 2, 1.4))


class Sami(Animal):

    def __init__(self, id_: str, name: str, birthdate: int):
        super().__init__(id_, name, birthdate)
        self.habits = Habits(SleepingHabit(19, 6), EatingHabit(FoodPreference.CARNIVORE, [20, 5]))
        self.lifecycle = Lifecycle(LifecyclePhase(6, 3, 0.4),
                                   LifecyclePhase(15, 8, 1),
                                   LifecyclePhase(20, 6, 1.4))
