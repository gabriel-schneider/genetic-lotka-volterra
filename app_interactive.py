from lotkavolterra.core import Simulation, Population, Solution
from genetic.selection import TournamentSelection, EliteSelection
from genetic.fitness import SmallerIsBetterRule, HigherIsBetterRule
from genetic.crossover import TwoPointCrossover, SinglePointCrossover
from genetic.mutation import FlipBitMutator, SwapBitMutator
import matplotlib.pyplot as pyplot
import random
import math


def main():

    random.seed()

    options = {}

    print('Population Size [1000]: ')
    options['population'] = int(input('=> ') or 1000)

    print('Population fitness rule [0]: ')
    print('[0] Smaller is Better')
    print('[1] Higher is Better')

    fitness_rules = [
        SmallerIsBetterRule(),
        HigherIsBetterRule()
    ]

    options['population_fitness_rule'] = fitness_rules[int(input('=> ') or 0)]

    population = Population(
        options['population'], options['population_fitness_rule'])

    print('Number of prey [80]: ')
    options['prey'] = int(input('=> ') or 80)

    print('Number of predators [30]: ')
    options['predator'] = int(input('=> ') or 30)

    environment = Simulation(
        prey=options['prey'], predator=options['predator'])

    population.populate()
    population.evaluate(environment)

    print('Crossover method [0]: ')
    print('[0] Single Point ')
    print('[1] Two Points')

    crossover_options = [
        SinglePointCrossover(),
        TwoPointCrossover()
    ]

    crossover = crossover_options[int(input('=> ') or 0)]

    print('Crossover method [0]: ')
    print('[0] Flip Bit Mutator ')
    print('[1] Swap Bit Mutator')

    mutator_options = [
        FlipBitMutator(1),
        SwapBitMutator(1)
    ]

    mutator = mutator_options[int(input('=> ') or 0)]

    print('Mutation ratio [0.05]: ')
    mutator._ratio = float(input('=> ') or 0.05)

    print('Selection method [0]: ')
    print('[0] Tournament')
    print('[1] Elite')

    selector_options = [
        TournamentSelection(100),
        EliteSelection(options['population_fitness_rule'])
    ]

    options['selector'] = selector_options[int(input('=> ') or 0)]
    if isinstance(options['selector'], TournamentSelection):
        print('Tournament size [100]: ')
        options['selector']._size = int(input('=> ') or 100)

    selector = options['selector']

    stats = []

    print('Number of generations [1000]: ')
    generations = int(input('=> ') or 1000)

    step = 10

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

            if population.best.fitness == 0:
                break

            if generation % step == 0:
                sum_of_fitness = sum(
                    x.fitness for x in population.solutions.values())
                stats.append(sum_of_fitness)
                print(
                    f'Generation {generation}... ({population.best.fitness}, {sum_of_fitness})')
    except KeyboardInterrupt:
        print(population.best, sum(
            x.fitness for x in population.solutions.values()))

    print(population.best, sum(
        x.fitness for x in population.solutions.values()))

    pyplot.plot(stats)
    pyplot.xlabel('Generations')
    pyplot.ylabel('Population Fitness')
    pyplot.show()


if __name__ == '__main__':
    main()
