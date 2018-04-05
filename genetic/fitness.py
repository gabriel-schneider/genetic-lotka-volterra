class FitnessRule:
    def apply(self, solutions):
        """Apply a fitness rule to a list of solution"""

    def compare(self, solution_a, solution_b):
        """Compare two solutions using class rules"""
        solutions = [solution_a, solution_b]
        self.apply(solutions)
        return solutions[0]


class SmallerIsBetterRule(FitnessRule):
    def apply(self, solutions):
        solutions.sort(key=lambda x: x.fitness)

    def __str__(self):
        return 'Smaller Is Better Rule'


class HigherIsBetterRule(FitnessRule):
    def apply(self, solutions):
        solutions.sort(key=lambda x: x.fitness, reverse=True)

    def __str__(self):
        return 'Higher Is Better Rule'


# TODO: Approximation Fitness Rule
class ApproximationRule(FitnessRule):
    def __init__(self, best, lowest, highest):
        pass

    def __str__(self):
        return 'Approximation Rule'
