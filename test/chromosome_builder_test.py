import unittest

from src.genetics.chromosome import Chromosome
from src.genetics.chromosome import ChromosomeBuilder
from src.genetics.genotype import Genotype
from unittest import TestCase


class ChromosomeBuilderTest(TestCase):

    def test_build_chromosome(self):
        """"""
        genotype = Genotype()
        genotype.add_gene('A', ['0', '1'])
        genotype.add_gene('B', ['-'])
        genotype.add_gene('C', ['aa', 'bb', 'cc', 'dd'])

        builder = ChromosomeBuilder(genotype)
        builder.allele('A', '0')
        builder.allele('B', '-')
        builder.allele('C', 'aa')

        chromosome = builder.create_chromosome()

        expected = Chromosome(genotype)
        expected.alleles['A'] = '0'
        expected.alleles['B'] = '-'
        expected.alleles['C'] = 'aa'

        self.assertEqual(expected, chromosome)