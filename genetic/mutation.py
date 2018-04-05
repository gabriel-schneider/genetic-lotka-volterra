from abc import ABC
import random
import math


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


class SwapBitMutator(Mutator):
    def __call__(self, genotype):
        genes = list(genotype)
        for _ in range(math.ceil(len(genotype) * self._ratio)):
            first = random.randint(1, len(genotype) - 1)
            second = (first + random.randint(1, len(genotype) - 2)
                      ) % len(genotype)
            tmp_gene = genes[first]
            genes[first] = genes[second]
            genes[second] = tmp_gene
        return ''.join(genotype)
