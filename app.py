from lotkavolterra.core import Simulation, Population, Solution
from genetic.crossover import TwoPointCrossover
from genetic.selection import TournamentSelection
from genetic.mutation import FlipBitMutator
from genetic.fitness import SmallerIsBetterRule
import random


def main():
    random.seed()

    population = Population(1000)

    environment = Simulation(prey=750, predator=500)

    population.populate()

    best_solution = None
    no_improvement_count = 0
    try:
        while True:
            sum_of_fitness = sum(
                x.fitness for x in population.solutions.values())
            if no_improvement_count > 1000:
                print('Cataclysm!')
                population.cataclysm(100)
                no_improvement_count = 0

            solutions_to_crossover = population.select(
                4, TournamentSelection(100))
            for solution_set in solutions_to_crossover:
                solutions = (
                    population.solutions[solution_set[0]], population.solutions[solution_set[1]])
                new_solutions = Solution.crossover(
                    solutions, TwoPointCrossover())
                for solution in new_solutions:
                    solution.mutate(FlipBitMutator(0.1))
                    solution.fitness = environment.evaluate(solution, 1000)
                    try:
                        population.insert(solution)
                    except:
                        continue
                    if best_solution == None or solution.fitness < best_solution.fitness:
                        best_solution = solution
            population.cap(SmallerIsBetterRule())
            if population.generation % 100 == 0:
                print(f'Generation {population.generation}...', end='')
                print(f'({best_solution.fitness})')

            if sum_of_fitness <= sum(x.fitness for x in population.solutions.values()):
                no_improvement_count += 1
            else:
                no_improvement_count = 0
            population.generation += 1
    except KeyboardInterrupt:
        print(best_solution)


if __name__ == '__main__':
    main()
