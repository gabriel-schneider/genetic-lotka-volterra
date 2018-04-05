import matplotlib.pyplot as pyplot
import random
import time


from lotkavolterra.core import Simulation, Population, Solution
from genetic.selection import TournamentSelection
from genetic.fitness import SmallerIsBetterRule, HigherIsBetterRule
from genetic.crossover import TwoPointCrossover
from genetic.mutation import FlipBitMutator, SwapBitMutator


def main():

    random.seed()

    population = Population(1000, SmallerIsBetterRule())

    environment = Simulation(prey=80, predator=30)

    population.populate()
    population.evaluate(environment)

    crossover = TwoPointCrossover()
    mutator = SwapBitMutator(0.05)
    selector = TournamentSelection(100)

    stats = []

    generations = 1000
    step = 100

    start = time.time()
    try:
        for generation in range(generations):
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
            if generation % step == 0:
                sum_of_fitness = sum(
                    x.fitness for x in population.solutions.values())
                stats.append(sum_of_fitness)
                print(
                    f'Generation {generation}... ({population.best.fitness}, {sum_of_fitness})')
    except KeyboardInterrupt:
        print(population.best, sum(
            x.fitness for x in population.solutions.values()))

    print(f'Duration: {time.time() - start}')
    pyplot.plot(stats)
    pyplot.xlabel('Generations')
    pyplot.ylabel('Population Fitness')
    pyplot.show()


if __name__ == '__main__':
    main()
