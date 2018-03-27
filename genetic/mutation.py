from abc import ABC
import random


class Mutator(ABC):
    def __init__(self, ratio):
        self._ratio = ratio

    def __call__(self, genotype):
        """Mutate a solution changing its genotype data"""
        pass


class FlipBitMutator(Mutator):
    def __call__(self, genotype):
        genotype = list(genotype)
        for i, gene in enumerate(genotype):
            if random.random() <= self._ratio:
                genotype[i] = str(1 - int(gene))
        return ''.join(genotype)
