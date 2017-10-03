import copy

from src.simulation.grid import Grid

import src.evolution.selection as selection


class Config:

    def __init__(self):
        self.__grid = None

    def grid(self):
        return copy.deepcopy(self.__grid)

    def ant_steps(self):
        return 500

    def evolution_years(self):
        return 5000 #5000

    def population_size(self):
        return 500

    def statemachine_size(self):
        return 5

    def parent_count(self):
        return 10

    def parent_selection(self, *args, **kwargs):
        return selection.select_strongest(*args, **kwargs)

    def decease_count(self):
        return self.parent_count()

    def decease_selection(self, *args, **kwargs):
        return selection.select_weakest(*args, **kwargs)

    @property
    def mutation_chance(self):
        return 0.02

    @property
    def recombination(self):
        import src.genetics.recombination as recombination
        return recombination.OnePointCrossover()

    @staticmethod
    def load(path='../res/config.yaml'):
        config = Config()
        config.__grid = Grid.from_file('../res/santa_fe_trail.txt')
        return config

    @staticmethod
    def instance():
        return Config.load()