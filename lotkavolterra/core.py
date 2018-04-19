import genetic.core
import random
import math


class Population(genetic.core.Population):
    def populate(self, amount=-1):
        if amount == -1:
            amount = self.maximum
        while len(self.solutions) < amount:
            solution = Solution()
            solution.random()
            self.insert(solution)


class Solution(genetic.core.Solution):
    def __init__(self, prey_growth=0, predator_growth=0, predator_mortality=0, encounter_rate=0):
        super().__init__()
        self.prey_growth = prey_growth
        self.predator_growth = predator_growth
        self.predator_mortality = predator_mortality
        self.encounter_rate = encounter_rate

    def random(self):
        self.prey_growth = random.randint(0, 1023)
        self.predator_growth = random.randint(0, 1023)
        self.predator_mortality = random.randint(0, 1023)
        self.encounter_rate = random.randint(0, 1023)

    @property
    def genotype(self):
        self._genotype = f'{self.prey_growth:b}'.zfill(10) + f'{self.predator_growth:b}'.zfill(
            10) + f'{self.predator_mortality:b}'.zfill(10) + f'{self.encounter_rate:b}'.zfill(10)

        return self._genotype

    @genotype.setter
    def genotype(self, genotype):
        self._genotype = genotype
        self.prey_growth = int(genotype[:10], 2)
        self.predator_growth = int(genotype[10:20], 2)
        self.predator_mortality = int(genotype[20:30], 2)
        self.encounter_rate = int(genotype[30:], 2)

    @property
    def identifier(self):
        return self.genotype

    @staticmethod
    def crossover(solutions, method):
        genotypes = method(solutions[0].genotype, solutions[1].genotype)
        offsprings = (Solution(), Solution())
        for i, offspring in enumerate(offsprings):
            offspring.genotype = genotypes[i]
        return offsprings

    def __str__(self):
        result = [
            f'Genotype: {self.genotype}',
            f'Prey Growth: {self.prey_growth} => {self.prey_growth / 1023}',
            f'Predator Growth: {self.predator_growth} => {self.predator_growth / 1023}',
            f'Predator Mortality: {self.predator_mortality} => {self.predator_mortality / 1023}',
            f'Encounter Rate: {self.encounter_rate} => {self.encounter_rate / 1023}',
            f'Fitness: {self.fitness}'
        ]
        return '\n'.join(result)


class Simulation(genetic.core.Environment):
    """Environment for lotka-volterra simulation"""

    def __init__(self, prey, predator):
        self.prey = prey
        self.predator = predator
        self.valid = False
        self.stats = []
        self.stats_cycle_steps = 0

    def evaluate(self, solution, steps=1000, stats=False):
        """Evaluates a solution simulating it against the environment"""
        if stats:
            self.stats.clear()

        prey = self.prey
        pred = self.predator

        ratio_lowest = math.inf
        ratio_highest = -math.inf

        for step in range(steps):

            if stats:
                self.stats.append((prey, pred))

            prey = prey + ((solution.prey_growth / 1023 * prey) -
                           (solution.encounter_rate / 1023 * prey * pred))
            pred = pred + ((solution.predator_growth / 1023 *
                            prey * pred) - (solution.predator_mortality / 1023 * pred))

            if math.isinf(pred) or math.isinf(prey) or math.floor(pred) <= 0 or math.floor(prey) <= 0:
                self.valid = False
                return 10 - step/steps

            ratio = max(1, prey) / max(1, pred)
            ratio_lowest = ratio if ratio < ratio_lowest else ratio_lowest
            ratio_highest = ratio if ratio > ratio_highest else ratio_highest

        self.valid = True
        return ratio_highest - ratio_lowest
