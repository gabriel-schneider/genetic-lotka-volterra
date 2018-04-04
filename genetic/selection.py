from abc import ABC
import random


class Selection(ABC):
    def __init__(self, allow_duplicates=False):
        self._allow_duplicates = allow_duplicates

    def __call__(self, solutions):
        """Return a pair of solution identifiers"""
        pass


class TournamentSelection(Selection):
    def __init__(self, size, allow_duplicates=False):
        super().__init__(allow_duplicates)
        self._size = size

    def __call__(self, solutions):
        solutions = list(solutions.values())
        if len(solutions) < self._size:
            raise Exception(
                'Solution list size cannot be less than tournament size!')

        pair = []
        for _ in range(2):
            random.shuffle(solutions)
            candidates = solutions[:self._size]
            candidates.sort(key=lambda x: x.fitness)
            pair.append(solutions.pop().identifier)
        return pair

# TODO: Implement


class EliteSelection(Selection):
    def __init__(self, fitness_rule, allow_duplicates=False):
        super().__init__(allow_duplicates)
        self._fitness_rule = fitness_rule

    def __call__(self, solutions):
        solutions = list(solutions.values())
        self._fitness_rule.apply(solutions)
        return (solutions[0].identifier, solutions[1].identifier)
