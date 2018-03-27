from abc import ABC
import random


class Environment(ABC):
    """Base class for any environment"""

    def evaluate(self, solution):
        """Evaluate a solution using environment rules"""
        pass


class Solution(ABC):
    def __init__(self):
        self._fitness = 0
        self._genotype = ''
        self._identifier = ''

    def random(self):
        """Define random attributes"""
        pass

    def mutate(self, mutator):
        """Mutate solution changing the genotype data using a mutator object"""
        self.genotype = mutator(self.genotype)

    @staticmethod
    def crossover(solutions, method):
        pass

    @property
    def genotype(self):
        return self._genotype

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, value):
        self._identifier = value

    @property
    def fitness(self):
        return self._fitness

    @fitness.setter
    def fitness(self, value):
        self._fitness = value


class PopulationError(Exception):
    pass


class Population(ABC):
    def __init__(self, maximum):
        self.maximum = maximum
        self.solutions = {}
        self.generation = 1

    def populate(self, count=-1):
        """Insert random solutions in the population"""
        pass

    def cap(self, fitness_rule, maximum=-1):
        """Limit the population size using a fitness rule"""
        maximum = self.maximum if maximum == -1 else maximum
        solutions = list(self.solutions.values())
        fitness_rule.apply(solutions)
        for solution in solutions[maximum:]:
            del self.solutions[solution.identifier]

    def cataclysm(self, amount):
        for _ in range(amount):
            del self.solutions[random.choice(list(self.solutions.keys()))]
        self.populate()

    def evaluate(self, environment):
        for solution in self.solutions.values():
            solution.fitness = environment.evaluate(solution)

    def insert(self, solution):
        try:
            self.solutions[solution.identifier] = solution
        except KeyError:
            raise PopulationError('Solution with identifier already exists!')

    def get(self, identifier):
        return self.solutions[identifier]

    def select(self, number_of_pairs, method):
        solutions = dict(self.solutions)
        pairs = []
        while len(pairs) < number_of_pairs:
            pair = method(solutions)
            pairs.append(pair)
            for solution in pair:
                del solutions[solution]
        return pairs

    def __len__(self):
        return len(self.solutions)
