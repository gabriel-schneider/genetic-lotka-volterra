import unittest
from genetic.core import Solution, Population
from genetic.selection import EliteSelection
from genetic.fitness import SmallerIsBetterRule, HigherIsBetterRule


class SelectionTestCase(unittest.TestCase):

    class DummySolution(Solution):
        def __init__(self, fitness):
            super().__init__()
            self._fitness = fitness
            self._identifier = fitness

    def test_elite_smaller_is_better(self):

        population = Population(100, SmallerIsBetterRule())
        population.insert(self.DummySolution(100))
        population.insert(self.DummySolution(50))
        population.insert(self.DummySolution(500))
        population.insert(self.DummySolution(125))
        population.insert(self.DummySolution(25))
        population.insert(self.DummySolution(200))

        selector = EliteSelection(population._fitness_rule, False)

        solutions = selector(population.solutions)

        self.assertEqual('25', str(solutions[0]))
        self.assertEqual('50', str(solutions[1]))

    def test_elite_higher_is_better(self):

        population = Population(100, HigherIsBetterRule())
        population.insert(self.DummySolution(100))
        population.insert(self.DummySolution(50))
        population.insert(self.DummySolution(500))
        population.insert(self.DummySolution(125))
        population.insert(self.DummySolution(25))
        population.insert(self.DummySolution(200))

        selector = EliteSelection(population._fitness_rule, False)

        solutions = selector(population.solutions)

        self.assertEqual('500', str(solutions[0]))
        self.assertEqual('200', str(solutions[1]))
