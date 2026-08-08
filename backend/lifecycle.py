class LifecyclePhase:
    def __init__(self, endOfPhaseAge: int, requiredFoodPerFeeding: int, riskOfIllnessMultiplier: float):
        self.endOfPhaseAge = endOfPhaseAge
        self.requiredFoodPerFeeding = requiredFoodPerFeeding
        self.riskOfIllnessMultiplier = riskOfIllnessMultiplier



class Lifecycle:
    def __init__(self, childPhase: LifecyclePhase, adultPhase: LifecyclePhase, seniorPhase: LifecyclePhase):
        self.childPhase = childPhase
        self.adultPhase = adultPhase
        self.seniorPhase = seniorPhase

