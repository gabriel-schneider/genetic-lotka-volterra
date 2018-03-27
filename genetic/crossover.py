from abc import ABC
import math
import random


class CrossoverException(Exception):
    pass

class Crossover(ABC):
    """Base class for crossover classes"""

    def __call__(self, genotype_a, genotype_b):
        if len(genotype_a) != len(genotype_b):
            raise CrossoverException('Genotypes length do not match!')


class SinglePointCrossover(Crossover):
    def __call__(self, genotype_a, genotype_b):
        super().__call__(genotype_a, genotype_b)
        pivot = random.randint(1, len(genotype_a) - 1)
        return (genotype_a[:pivot] + genotype_b[pivot:], genotype_b[:pivot] + genotype_a[pivot:])


class TwoPointCrossover(Crossover):
    def __call__(self, genotype_a, genotype_b):
        super().__call__(genotype_a, genotype_b)
        half_genotype = len(
            genotype_a) // 2 if len(genotype_a) % 2 == 0 else len(genotype_a) // 2 + 1
        _range = random.randint(1, half_genotype)
        _pos = random.randint(0, len(genotype_a) - half_genotype)
        return (
            genotype_a[:_pos] + genotype_b[_pos:_pos +
                                           _range] + genotype_a[_pos + _range:],
            genotype_b[:_pos] + genotype_a[_pos:_pos +
                                           _range] + genotype_b[_pos + _range:]
        )
