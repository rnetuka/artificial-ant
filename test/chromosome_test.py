import unittest

from src.genetics.chromosome import Chromosome
from src.genetics.chromosome import ChromosomeBuilder
from src.genetics.genotype import GenotypeBuilder
from src.genetics.genotype import GenotypeException
from unittest import TestCase


class ChromosomeTest(TestCase):

    def setUp(self):
        """Create a simple chromosome """
        genotype_builder = GenotypeBuilder()
        genotype_builder.add('FRM', ['000', '001', '010', '011', '100'])
        genotype_builder.add('IN', ['0', '1'])
        genotype_builder.add('TO', ['000', '001', '010', '011', '100'])
        genotype_builder.add('OUT', ['00', '01', '10', '11'])

        self.genotype = genotype_builder.create_genotype()

        chromosome_builder = ChromosomeBuilder(self.genotype)
        chromosome_builder.allele('FRM', '000')
        chromosome_builder.allele('IN', '1')
        chromosome_builder.allele('TO', '011')
        chromosome_builder.allele('OUT', '00')

        self.chromosome = chromosome_builder.create_chromosome()

    def test_to_string(self):
        """Test """
        self.assertEqual('000101100', str(self.chromosome))

    def test_from_string(self):
        """"""
        self.assertEqual(self.chromosome, Chromosome.from_string('000101100', self.genotype))

    def test_from_string_shorter_length(self):
        self.assertRaises(ValueError, Chromosome.from_string, '000101100'[:-1], self.genotype)

    def test_from_string_longer_length(self):
        self.assertRaises(ValueError, Chromosome.from_string, '000101100' + '1', self.genotype)

    def test_from_string_invalid_data(self):
        self.assertRaises(GenotypeException, Chromosome.from_string, '111101100', self.genotype)

    def test_mutate_gene(self):
        """"""
        self.chromosome.mutate_gene('FRM')
        self.assertTrue(str(self.chromosome) in ['001101100', '010101100', '011101100', '100101100'])

    def test_mutate_immutable_gene(self):
        """Test that immutable genes cannot be mutated"""
        self.chromosome._genotype.data['IN'] = ['0']
        self.assertRaises(ValueError, self.chromosome.mutate_gene, 'IN')

    def test_mutate(self):
        """"""
        self.chromosome.mutate(4)
        self.assertTrue(str(self.chromosome) in [
            '001000001', '001000010', '001000011',
            '001000001', '001000010', '001000011',
            '001001001', '001001010', '001001011',
            '001010001', '001010010', '001010011',
            '010000001', '010000010', '010000011',
            '010000101', '010000110', '010000111',
            '010001001', '010001010', '010001011',
            '010010001', '010010010', '010010011',
            '011000001', '011000010', '011000011',
            '011000101', '011000110', '011000111',
            '011001001', '011001010', '011001011',
            '011010001', '011010010', '011010011',
            '100000001', '100000010', '100000011',
            '100000101', '100000110', '100000111',
            '100001001', '100001010', '100001011',
            '100010001', '100010010', '100010011'
        ])

    def test_mutate_less_then_one_gene(self):
        """Test that it's not possible to mutate less than 1 gene"""
        self.assertRaises(ValueError, self.chromosome.mutate, 0)

    def test_mutate_more_than_there_are_genes(self):
        """Test that it's not possible to mutate more genes than there actually are"""
        self.assertRaises(ValueError, self.chromosome.mutate, 5)

    def test_recombination(self):
        """"""
        a = Chromosome.from_string('000101100', self.genotype)
        b = Chromosome.from_string('000101100', self.genotype)
        c, d = a.recombine_with(b)
        #self.assertEqual(str(c), '')

    def test_equal_to(self):
        """"""

    def test_not_equal_to(self):
        """"""


if __name__ == '__main__':
    unittest.main()