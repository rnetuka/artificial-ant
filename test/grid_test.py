from unittest import TestCase

from src.simulation.grid import Grid


class GridTest(TestCase):

    def setUp(self):
        self.grid = Grid.from_file('../res/santa_fe_trail.txt')

    def test(self):
        a =1 + 1