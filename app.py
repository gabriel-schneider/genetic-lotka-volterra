import matplotlib.pyplot as pyplot
import random
import time
from datetime import datetime
import csv
import os

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

    def export(id):

        # CSV export
        with open(f'data/{id}/generation_{generation}.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['Generation', 'Prey', 'Predator'])
            for i, stat in enumerate(environment.stats):
                writer.writerow([i, stat[0], stat[1]])

        # Plot
        x, y = zip(*environment.stats)
        pyplot.clf()
        pyplot.plot(x, 'r-', label='Prey')
        pyplot.plot(y, 'b-', label='Predator')
        pyplot.savefig(f'data/{id}/generation_{generation}.png')

    started_at = time.time()
    run_id = datetime.now().strftime('%Y%m%d_%H%M%S')
    os.makedirs(f'data/{run_id}')

    try:
        generations = 10000
        export_interval = 100
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
                environment.evaluate(population.best, 64, True)
                export(run_id)

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

    finished_at = time.time()
    print(f'Run duration: {math.floor(finished_at - started_at)} seconds')


if __name__ == '__main__':
    main()
