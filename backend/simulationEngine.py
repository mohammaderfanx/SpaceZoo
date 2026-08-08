import threading
from eventScheduler import EventScheduler
from zoo import Zoo

class SimulationEngine:

    def __init__(self):
        self.zoo = Zoo
        self.eventScheduler: EventScheduler = EventScheduler(self.zoo)
        self.secondsPerTick = 10 #possibly change
        self.ticks = 0
        self.elapsedHours = 0
        self.elapsedDays = 0

    
    def tick(self):
        self.increaseTime()
        self.eventScheduler.scheduleEvents(self.elapsedDays, self.elapsedHours)
        self.decreaseSaturation()
        self.decreaseHealth()
        self.decreaseEnergy()
        self.layEggs()
        self.eggsHatch()
        self.catchIllnesses()
        self.cleanEnclosures()
        threading.Timer(self.secondsPerTick, self.tick).start()


    def increaseTime(self):
        self.elapsedHours += 1
        if self.elapsedHours == 24:
            self.elapsedHours = 0
            self.elapsedDays += 1


    def decreaseSaturation():
        """Alle Tiere verlieren Saturation, wenn sie nicht da gefüttert werden, possibly tot (Funktion in zoo)"""

    def decreaseHealth():
        """Alle kranken Tiere verlieren Health, possibly tot (Funktion in zoo)"""

    def decreaseEnergy():
        """Wenn sie nicht schlafen"""

    def layEggs(self):
        """Schaut wo möglich, dann Chance, Ei kommt irgendwo hin"""

    def eggsHatch(self):
        """schaut welche Eier schlüpfen, neues Tier"""

    def catchIllnesses(self):
        """Verteilt zufällig Krankheiten (Chance wird größer wenn schon krankes Tier in Gehege)"""


    def cleanEnclosures(self):
        """schaut ob Caretaker da, wenn ja können die Enclosures cleanen"""

    def start(self):
        self.tick()
