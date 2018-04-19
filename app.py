import matplotlib.pyplot as pyplot
from datetime import datetime
import random
import time
import math
import csv
import os
import statistics

from lotkavolterra.core import Simulation, Population, Solution
from genetic.selection import TournamentSelection
from genetic.fitness import SmallerIsBetterRule, HigherIsBetterRule
from genetic.crossover import TwoPointCrossover
from genetic.mutation import FlipBitMutator, SwapBitMutator


def main():

    random.seed()

    population = Population(1000, SmallerIsBetterRule())
    population.populate()

    environment = Simulation(prey=80, predator=30)
    population.evaluate(environment)

    crossover = TwoPointCrossover()
    mutator = SwapBitMutator(0.05)
    selector = TournamentSelection(100)

    stats = []

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
        generations = 10000
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
