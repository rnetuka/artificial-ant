#from typing import List

from src.evolution.individual import Individual


def select_strongest(population: list, count: int) -> list:
    """Select strongest individuals from the population. The number being selected must be between 1 and population size.
     Selected individuals are returned in a list, in descending order of their fitness.

    :param population:
    :param count:
    :return:
    """
    if not len(population) >= count > 0:
        raise ValueError('Cannot perform selection for {} individuals. Population size is {}.'.format(count, len(population)))

    return sorted(population, reverse=True)[:count]


def select_weakest(population: list, count: int) -> list:
    if not len(population) >= count > 0:
        raise ValueError('Cannot perform selection for {} individuals. Population size is {}.'.format(count, len(population)))

    return sorted(population)[:count]