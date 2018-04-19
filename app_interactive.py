import matplotlib.pyplot as pyplot
from datetime import datetime
import random
import time
import math
import csv
import os
import statistics

from lotkavolterra.core import Simulation, Population, Solution
from genetic.selection import TournamentSelection, EliteSelection
from genetic.fitness import SmallerIsBetterRule, HigherIsBetterRule
from genetic.crossover import TwoPointCrossover, SinglePointCrossover
from genetic.mutation import FlipBitMutator, SwapBitMutator


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

    def export(id, cycle=0):

        def round_down(value):
            return math.floor(value * 10) / 10

        def get_cycle(index):
            value = -1
            repeats = []

            for i, stat in enumerate(environment.stats):
                if round_down(stat[index]) == round_down(value):
                    repeats.append(i)

                if round_down(stat[index]) > round_down(value):
                    value = round_down(stat[index])
                    repeats.clear()

            if len(repeats) > 1:
                return math.ceil(statistics.mean(
                    [repeats[i + 1] - x for i, x in enumerate(repeats[:-1])]))
            else:
                return len(environment.stats)

        if cycle == 0:
            cycle = max(get_cycle(1), get_cycle(0))

        # CSV export
        with open(f'data/{id}/generation_{generation}.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Generation', 'Prey', 'Predator'])
            for i, stat in enumerate(environment.stats[:cycle]):
                writer.writerow([i, stat[0], stat[1]])

        # Plot
        x, y = zip(*environment.stats[:cycle])
        pyplot.clf()
        pyplot.grid(True)
        pyplot.plot(x, 'r-', label='Prey')
        pyplot.plot(y, 'b-', label='Predator')
        pyplot.savefig(f'data/{id}/generation_{generation}.png')

    started_at = time.time()
    run_id = datetime.now().strftime('%Y%m%d_%H%M%S')
    os.makedirs(f'data/{run_id}')

    try:
        export_interval = 10
        last_fitness = math.inf
        for generation in range(generations):

            # Check equilibrium
            if population.best.fitness == 0:
                print('[!] Equilibrium found!')
                raise KeyboardInterrupt

            # Select, crossover and mutate!
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

            if generation % export_interval == 0:

                environment.evaluate(population.best, 1000, True)
                if (environment.valid and population.best.fitness < last_fitness):
                    last_fitness = population.best.fitness
                    export(run_id, 100)

                # Algorithm statistics
                sum_of_fitness = sum(
                    x.fitness for x in population.solutions.values())
                stats.append(sum_of_fitness)
                print(
                    f'Generation {generation}... ({population.best.fitness}, {sum_of_fitness})')

    except KeyboardInterrupt:
        export(run_id)
        print(population.best, sum(
            x.fitness for x in population.solutions.values()))

    pyplot.clf()
    pyplot.grid(True)
    pyplot.plot(stats, 'r-', label='Population')
    pyplot.savefig(f'data/{run_id}/population.png')

    finished_at = time.time()
    print(f'Run duration: {(finished_at - started_at):0.2f} seconds')


if __name__ == '__main__':

    # solution = Solution()
    # solution.genotype = '1001110100000000101111011010100000010101'
    # environment = Simulation(prey=80, predator=30)
    # solution.fitness = environment.evaluate(solution, stats=True)

    # print(solution)

    main()
