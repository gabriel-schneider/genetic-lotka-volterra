from lotkavolterra.core import Simulation, Population, Solution
from genetic.selection import TournamentSelection
from genetic.fitness import SmallerIsBetterRule, HigherIsBetterRule
from genetic.crossover import TwoPointCrossover
from genetic.mutation import FlipBitMutator
import random


def main():

    random.seed()

    population = Population(1000, SmallerIsBetterRule())

    environment = Simulation(prey=80, predator=30)

    population.populate()
    population.evaluate(environment)

    crossover = TwoPointCrossover()
    mutator = FlipBitMutator(0.05)
    selector = TournamentSelection(100)

    stats = []

    try:
        for generation in range(1000):
            solutions_to_crossover = population.select(
                4, selector)
            for solution_set in solutions_to_crossover:
                offsprings = Solution.crossover(
                    population.get(solution_set), crossover)
                for offspring in offsprings:
                    offspring.mutate(mutator)
                    offspring.fitness = environment.evaluate(offspring, 1000)
                    population.insert(offspring)
            population.cap()
            if generation % 10 == 0:
                sum_of_fitness = sum(
                    x.fitness for x in population.solutions.values())
                stats.append(sum_of_fitness)
                print(
                    f'Generation {generation}... ({population.best.fitness}, {sum_of_fitness})')
    except KeyboardInterrupt:

        print(population.best, sum(
            x.fitness for x in population.solutions.values()))


if __name__ == '__main__':

    # def approx(value, lowest, best, highest):
    #     if value >= best:
    #         return 1 - (value - best) / (highest - best)
    #     else:
    #         return (value - lowest) / (best - lowest)

    # for x in range(0, 110, 10):
    #     print(f'{x}: {approx(x, 0, 50, 100)}')

    main()
