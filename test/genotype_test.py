import unittest

from src.genetics.gene import Gene
from src.genetics.genotype import GenotypeBuilder
from unittest import TestCase


class GenotypeTest(TestCase):

    def setUp(self):
        self.genotype = GenotypeBuilder() \
            .add(Gene('A', ['00', '01', '10', '11'])) \
            .add(Gene('B', ['0', '1'])) \
            .create_genotype()

    def test_equals_allele_order_is_indifferent(self):
        """Test that two genotypes are equal. Gene order is important, but allele order for each gene is indifferent."""
        other_genotype = GenotypeBuilder()\
            .add(Gene('A', ['11', '10', '01', '00']))\
            .add(Gene('B', ['0', '1']))
        self.assertTrue(self.genotype == other_genotype)

    def test_not_equal_gene_order(self):
        """Test that two similar genotypes are not equal because of different gene order."""
        other_genotype = GenotypeBuilder() \
            .add(Gene('B', ['0', '1']))\
            .add(Gene('A', ['00', '01', '10', '11']))
        self.assertFalse(self.genotype == other_genotype)


if __name__ == '__main__':
    unittest.main()