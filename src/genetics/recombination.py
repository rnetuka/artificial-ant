import random

from src.genetics.chromosome import Chromosome


class OnePointCrossover:

    def __call__(self, chromosome_a, chromosome_b):
        """
        Perform a recombination and return the two new chromosomes.

        :param chromosome_a: Chromosome A

        :param chromosome_b: Chromosome B

        :return: two new chromosomes
        """
        if chromosome_a.genotype != chromosome_b.genotype:
            raise ValueError('Chromosomes must have the same genotype')

        recombination = OnePointCrossover.Recombination(chromosome_a, chromosome_b)

        genotype = chromosome_a.genotype

        crossover_points = recombination.preferred_crossover_points()

        if len(crossover_points) > 0:
            point = random.choice(crossover_points)
            str_c, str_d = recombination.perform(point)
            return Chromosome.from_string(str_c, genotype), Chromosome.from_string(str_d, genotype)
        else:
            return chromosome_a, chromosome_b

    class Recombination():

        def __init__(self, chromosome_a, chromosome_b):
            self.chromosome_a = chromosome_a
            self.chromosome_b = chromosome_b

        @property
        def genotype(self):
            return self.chromosome_a.genotype

        def is_valid(self, point):
            str_c, str_d = self.perform(point)
            return self.genotype.is_valid_chromosome(str_c) and self.genotype.is_valid_chromosome(str_d)

        def is_different(self, point):
            a = str(self.chromosome_a)
            b = str(self.chromosome_b)
            c, d = self.perform(point)
            return a != b != c != d

        def perform(self, i):
            c = str(self.chromosome_a)[:i] + str(self.chromosome_b)[i:]
            d = str(self.chromosome_b)[:i] + str(self.chromosome_a)[i:]
            return c, d

        def crossover_points(self):
            crossover_points = []
            i = 0
            for gene in self.genotype.genes:
                if gene.is_mutable():
                    crossover_points += [i + j for j in range(gene.allele_length)]
                i += gene.allele_length
            return crossover_points

        def valid_crossover_points(self):
            return [point for point in self.crossover_points() if self.is_valid(point)]

        def preferred_crossover_points(self):
            return [point for point in self.valid_crossover_points() if self.is_different(point)]
