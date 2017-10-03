import unittest
from unittest import TestCase

from src.genetics.gene import Gene
from src.genetics.genotype import GenotypeBuilder
from src.genetics.recombination import OnePointCrossover


class RecombinationTest(TestCase):

    def setUp(self):
        self.genotype = GenotypeBuilder() \
            .add(Gene('FRM', ['000', '001', '010', '011'], mutable=False)) \
            .add(Gene('IN', ['0', '1'], mutable=False)) \
            .add(Gene('TO', ['00', '01', '10', '11'])) \
            .add(Gene('OUT', ['000', '001', '010', '011'])) \
            .create_genotype()
        self.recombination = OnePointCrossover()

    def test_crossover_points(self):
        # chromosome 000 0 000 00
        expected = [4, 5, 6, 7, 8]
        actual = self.recombination.crossover_points(self.genotype)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()