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

    # def mutate(self, ratio):
    #     genotype = list(self.genotype)
    #     for i, gene in enumerate(genotype):
    #         if random.random() <= ratio:
    #             genotype[i] = str(1 - int(gene))
    #     self.genotype = ''.join(genotype)

    def __str__(self):
        return f'Genotype: {self.genotype}\nPrey Growth: {self.prey_growth}\nPredator Growth: {self.predator_growth}\nPredator Mortality: {self.predator_mortality}\nEncounter Rate: {self.encounter_rate}\nFitness: {self.fitness}\n'


class Simulation(genetic.core.Environment):
    """Environment for lotka-volterra simulation"""

    def __init__(self, prey, predator):
        # Initial values for preys and predators
        self.prey = prey
        self.predator = predator

    def evaluate(self, solution, steps=1000):
        prey = self.prey
        pred = self.predator

        ratio_lowest = math.inf
        ratio_highest = -math.inf

        for step in range(steps):

            prey = prey + ((solution.prey_growth/1023 * prey) -
                           (solution.encounter_rate/1023 * prey * pred))
            pred = pred + ((solution.predator_growth/65535 *
                            prey * pred) - (solution.predator_mortality/1023 * pred))

            if math.isinf(pred) or math.isinf(prey) or math.floor(pred) <= 0 or math.floor(prey) <= 0:
                return math.inf

            ratio = prey / pred
            ratio_lowest = ratio if ratio < ratio_lowest else ratio_lowest
            ratio_highest = ratio if ratio > ratio_highest else ratio_highest

        return ratio_highest - ratio_lowest
