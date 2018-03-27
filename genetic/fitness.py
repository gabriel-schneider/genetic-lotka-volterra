class FitnessRule:
    def apply(self, solutions):
        """Apply a fitness rule to a list of solution"""


class SmallerIsBetterRule(FitnessRule):
    def apply(self, solutions):
        solutions.sort(key=lambda x: x.fitness)


class HigherIsBetterRule(FitnessRule):
    def apply(self, solutions):
        solutions.sort(key=lambda x: x.fitness, reverse=True)


# TODO: Approximation Fitness Rule
class ApproximationRule(FitnessRule):
    def __init__(self, best, lowest, highest):
        pass
