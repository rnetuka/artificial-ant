import unittest

from src.genetics.gene import Gene
from unittest import TestCase


class GeneTest(TestCase):

    def test_create_gene_with_empty_alleles(self):
        """Test that gene cannot be created without any alleles"""
        self.assertRaises(ValueError, Gene.__init__, 'C', [])
