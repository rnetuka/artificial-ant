#!/usr/bin/env python3
# individual.py

"""Module containing the Individual class for genetic programming

Available classes:
- Individual
"""

import copy

from src.evolution.fitness import Fitness
from src.genetics.chromosome import Chromosome


class Individual:

    def __init__(self, chromosome: Chromosome, fitness: Fitness=Fitness.unspecified()):
        """Create a new Individual from specific chromosome and optional fitness.

        :param chromosome:  a Chromosome object

        :param fitness:
        """
        self.__chromosome = chromosome
        self.__fitness = fitness

    @property
    def chromosome(self) -> Chromosome:
        """Return this individual's chromosome."""
        return copy.deepcopy(self.__chromosome)

    @property
    def fitness(self) -> Fitness:
        """Return this individual's fitness."""
        return self.__fitness

    def mate_with(self, other):
        father_chromosome = self.chromosome
        mother_chromosome = other.chromosome
        child_1_chromosome, child_2_chromosome = Chromosome.recombination_of(father_chromosome, mother_chromosome)
        child_1_chromosome.mutate()
        child_2_chromosome.mutate()
        return Individual(child_1_chromosome), Individual(child_2_chromosome)

    def prove_yourself_on(self, proving_grounds):
        self.__fitness = proving_grounds.evaluate(self)

    def __gt__(self, other):
        return self.__fitness > other.__fitness

    def __eq__(self, other):
        return self.__chromosome == other.__chromosome

    def __hash__(self) -> int:
        return hash(self.__chromosome)