class LifecyclePhase:
    """A single life stage of an animal, defining its age limit, food needs, and illness risk."""

    def __init__(self, endOfPhaseAge: int, requiredFoodPerFeeding: int, riskOfIllnessMultiplier: float):
        self.endOfPhaseAge = endOfPhaseAge
        self.requiredFoodPerFeeding = requiredFoodPerFeeding
        self.riskOfIllnessMultiplier = riskOfIllnessMultiplier



class Lifecycle:
    """The three life stages (child, adult, senior) of an animal species."""

    def __init__(self, childPhase: LifecyclePhase, adultPhase: LifecyclePhase, seniorPhase: LifecyclePhase):
        self.childPhase = childPhase
        self.adultPhase = adultPhase
        self.seniorPhase = seniorPhase

