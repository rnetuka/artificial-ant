import unittest
from unittest import TestCase

import src.evolution.selection as selection
from src.evolution.evolution import Fitness
from src.evolution.evolution import Individual


class StrongestSelectionTest(TestCase):

    def setUp(self):
        self.population = [
            Individual(chromosome=None, fitness=Fitness(80, 50)),
            Individual(chromosome=None, fitness=Fitness(70, 3)),
            Individual(chromosome=None, fitness=Fitness(90, 5)),
            Individual(chromosome=None, fitness=Fitness(90, 10))
        ]

    def test_selection(self):
        best = selection.select_strongest(self.population, 2)
        self.assertEqual([self.population[2], self.population[3]], best)

    def test_select_no_one(self):
        self.assertRaises(ValueError, selection.select_strongest, self.population, 0)

    def test_select_exactly_as_there_are(self):
        """Test that selecting all individuals is legal operation (i.e. no ValueError is raised)"""
        selection.select_strongest(self.population, 4)

    def test_select_more_that_there_are(self):
        """Test that one cannot select more individuals that there currently are in the population. This also covers
        the test case if the population is empty.
        """
        self.assertRaises(ValueError, selection.select_strongest, self.population, 5)


class WeakestSelectionTest(TestCase):

    def setUp(self):
        self.population = [
            Individual(chromosome=None, fitness=Fitness(80, 50)),
            Individual(chromosome=None, fitness=Fitness(70, 3)),
            Individual(chromosome=None, fitness=Fitness(90, 5)),
            Individual(chromosome=None, fitness=Fitness(90, 10))
        ]

    def test_selection(self):
        best = selection.select_weakest(self.population, 2)
        self.assertEqual([self.population[1], self.population[0]], best)

    def test_select_no_one(self):
        self.assertRaises(ValueError, selection.select_weakest, self.population, 0)

    def test_select_exactly_as_there_are(self):
        """Test that selecting all individuals is legal operation (i.e. no ValueError is raised)"""
        selection.select_weakest(self.population, 4)

    def test_select_more_that_there_are(self):
        """Test that one cannot select more individuals that there currently are in the population. This also covers
        the test case if the population is empty.
        """
        self.assertRaises(ValueError, selection.select_weakest, self.population, 5)


if __name__ == '__main__':
    unittest.main()