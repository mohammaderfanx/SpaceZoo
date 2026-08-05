import threading

class SimulationEngine:

    def __init__(self):
        self.secondsPerTick = 10 #possibly change
        self.ticks = 0
        self.elapsedHours = 0
        self.elapsedDays = 0

    
    def tick(self):
        self.elapsedHours += 1
        if self.elapsedHours == 24:
            self.elapsedHours = 0
            self.elapsedDays += 1
        threading.Timer(self.secondsPerTick, self.tick).start()


    def start(self):
        self.tick()
