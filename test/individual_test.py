from unittest import TestCase

from src.evolution.evolution import Fitness
from src.evolution.evolution import Individual


class IndividualTest(TestCase):

    def test_ordering(self):
        population = [
            Individual(chromosome=None, fitness=Fitness(90, 10)),
            Individual(chromosome=None, fitness=Fitness(80, 5)),
            Individual(chromosome=None, fitness=Fitness(90, 5))
        ]
        self.assertEqual([population[2], population[0], population[1]], sorted(population, reverse=True))