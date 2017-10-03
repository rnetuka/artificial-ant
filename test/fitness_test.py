from unittest import TestCase

from src.evolution.evolution import Fitness


class FitnessTest(TestCase):

    def test_build_from_results(self):
        fitness = Fitness.from_result(total_baits=3, baits_eaten=1, steps_used=100)
        self.assertEqual(33, fitness.success_rate)

    def test_ordering(self):
        score = [Fitness(90, 10), Fitness(80, 5), Fitness(90, 5)]
        score.sort(reverse=True)
        self.assertEqual([Fitness(90, 5), Fitness(90, 10), Fitness(80, 5)], score)