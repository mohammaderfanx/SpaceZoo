"""
author: Jasmin Romeyke
date: 08.08.2026
version: 1
"""


import threading
from core.eventScheduler import EventScheduler
from core.zoo import Zoo
import statistics

class SimulationEngine:
    """Drives the zoo's simulation loop, advancing time and applying periodic effects each tick."""

    def __init__(self):
        self.zoo = Zoo()
        self.eventScheduler: EventScheduler = EventScheduler(self.zoo)
        self.secondsPerTick = 10 #possibly change
        self.ticks = 0
        self.elapsedHours = 0
        self.elapsedDays = 0
        self.running = False


    def tick(self):
        """Advances the simulation by one time step and applies all periodic effects.

        Args:
            self

        Tests:
            called once -> elapsed time advances and all periodic effects apply, with the next tick scheduled via threading.Timer
        """
        self.increaseTime()
        self.eventScheduler.scheduleEvents(self.elapsedDays, self.elapsedHours)
        self.decreaseSaturation()
        self.decreaseHealth()
        self.decreaseEnergy()
        self.layEggs()
        self.eggsHatch()
        self.catchIllnesses()
        self.cleanEnclosures()
        self.calculateVisitorScore()
        threading.Timer(self.secondsPerTick, self.tick).start()


    def increaseTime(self):
        """Advances the elapsed hour/day counters.

        Args:
            self

        Tests:
            elapsedHours below 23 -> only elapsedHours increases
            elapsedHours reaches 24 -> elapsedHours resets to 0 and elapsedDays increases
        """
        self.elapsedHours += 1
        if self.elapsedHours == 24:
            self.elapsedHours = 0
            self.elapsedDays += 1


    def decreaseSaturation(self):
        """Reduces saturation for unfed animals, possibly killing them.

        Args:
            self

        Return:
            None

        Tests:
            animal not fed this tick -> saturation decreases
            animal already at minimum saturation -> animal dies
        """

    def decreaseHealth(self):
        """Reduces health for sick animals, possibly killing them.

        Args:
            self

        Return:
            None
        
                    
        Tests:
            animal is sick -> health decreases
            animal's health reaches 0 -> animal dies
        """

    def decreaseEnergy(self):
        """Reduces energy for animals that aren't sleeping.

        Args:
            self

        Return:
            None

                    
        Tests:
            animal is awake -> energy decreases
            animal is asleep -> energy stays the same
        """

    def layEggs(self):
        """Lets eligible animals lay eggs, by chance, in a suitable spot.

        Args:
            self

        Return:
            None

        Tests:
            eligible animal and a free spot -> egg may be created
            no eligible animals -> no eggs are created
        """

    def eggsHatch(self):
        """Hatches eggs that are due, creating new animals.

        Args:
            self

        Return:
            None

        Tests:
            egg's dayOfHatching has passed -> new animal is created and egg removed
            egg not yet due -> egg remains unchanged
        """

    def catchIllnesses(self):
        """Randomly assigns illnesses to animals, more likely where a sick animal already shares the enclosure.

        Args:
            self

        Return:
            None

        Tests:
            enclosure has a sick animal -> higher chance of new illnesses there
            no sick animals present -> lower baseline chance applies
        """


    def cleanEnclosures(self):
        """Cleans enclosures where a caretaker is available.

        Args:
            self

        Return:
            None

        Tests:
            caretaker available -> enclosure cleanliness increases
            no caretaker available -> enclosure stays dirty
        """

    def calculateVisitorScore(self):
        """Computes the visitor score from environment, animal count, and enclosure cleanliness.

        Args:
            self

        Return:
            None

        Returns:
            float: combined score used to attract visitors

        Tests:
            high environmental attractiveness and clean enclosures -> high score
            no enclosures -> cleanliness doesn't affect score
        """
        environmentalScore =  self.zoo.environment.getVisitorAttractiveness() # why :(?
        animalScore = len(self.zoo.animals)
        cleanlinessScore =1
        if len(self.zoo.enclosures) != 0:
            cleanlinessScore = statistics.mean(enclosure.cleanliness for enclosure in self.zoo.enclosures)
        return environmentalScore * animalScore * cleanlinessScore
        

    def start(self):
        """Starts the simulation loop.

        Args:
            self

        Return:
            None

        Tests:
            called once -> tick() begins the recurring simulation loop
            called again while already running -> is a no-op, no overlapping loop starts
        """
        if self.running:
            return
        self.running = True
        self.tick()
