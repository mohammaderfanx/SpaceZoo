import threading
from eventScheduler import EventScheduler
from zoo import Zoo
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

    
    def tick(self):
        """Advances the simulation by one time step and applies all periodic effects."""
        self.increaseTime()
        # stop being busy?
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
        """Advances the elapsed hour/day counters."""
        self.elapsedHours += 1
        if self.elapsedHours == 24:
            self.elapsedHours = 0
            self.elapsedDays += 1


    def decreaseSaturation():
        """Reduces saturation for unfed animals, possibly killing them."""

    def decreaseHealth():
        """Reduces health for sick animals, possibly killing them."""

    def decreaseEnergy():
        """Reduces energy for animals that aren't sleeping."""

    def layEggs(self):
        """Lets eligible animals lay eggs, by chance, in a suitable spot."""

    def eggsHatch(self):
        """Hatches eggs that are due, creating new animals."""

    def catchIllnesses(self):
        """Randomly assigns illnesses to animals, more likely where a sick animal already shares the enclosure."""


    def cleanEnclosures(self):
        """Cleans enclosures where a caretaker is available."""

    def calculateVisitorScore(self):
        """Computes the visitor score from environment, animal count, and enclosure cleanliness."""
        environmentalScore =  self.zoo.environment.getVisitorAttractiveness() # why :(?
        animalScore = len(self.zoo.animals)
        cleanlinessScore = statistics.mean(enclosure.cleanliness for enclosure in self.zoo.enclosures)
        return environmentalScore * animalScore * cleanlinessScore
        

    def start(self):
        """Starts the simulation loop."""
        self.tick()
