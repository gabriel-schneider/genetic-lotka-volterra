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


class Population(ABC):
    def __init__(self, maximum, fitness_rule):
        self.maximum = maximum
        self.solutions = {}
        self._fitness_rule = fitness_rule
        self.best = None

    def populate(self, count=-1):
        """Insert random solutions in the population"""
        pass

    def cap(self, maximum=-1, fitness_rule=None):
        """Limit the population size using a fitness rule"""
        maximum = self.maximum if maximum == -1 else maximum
        if fitness_rule is None:
            fitness_rule = self._fitness_rule

        solutions = list(self.solutions.values())
        fitness_rule.apply(solutions)
        for solution in solutions[maximum:]:
            self.remove(solution.identifier)

    def remove(self, identifier):
        if self.best == self.solutions[identifier]:
            self.best = None
        del self.solutions[identifier]

    def cataclysm(self, amount):
        del self.solutions[self.best.identifier]
        for _ in range(amount):
            self.remove(random.choice(list(self.solutions.keys())))
        self.solutions[self.best.identifier] = self.best

    def evaluate(self, environment):
        for solution in self.solutions.values():
            solution.fitness = environment.evaluate(solution)

    def insert(self, solution):
        try:
            self.solutions[solution.identifier] = solution
            if self.best is None or self.best is not self._fitness_rule.compare(self.best, solution):
                self.best = solution
        except KeyError:
            return False

    def get(self, identifier):
        if isinstance(identifier, (tuple, list)):
            solutions = ()
            for _id in identifier:
                solutions = solutions + (self.solutions[_id],)
            return solutions
        else:
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
