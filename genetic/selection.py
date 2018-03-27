from abc import ABC
import random


class Selection(ABC):
    # def __init__(self, allow_duplicates):

    def __call__(self, solutions):
        """Return a pair of solution identifiers"""
        pass


class TournamentSelection(Selection):
    def __init__(self, size):
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


class EliteSelection(Selection):
    pass
