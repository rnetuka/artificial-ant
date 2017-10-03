import random

from collections import OrderedDict
from src.config import Config
from src.genetics.genotype import GenotypeException


class Chromosome:

    def __init__(self, genotype):
        """Create a new chromosome with specific genotype. The genotype provides information about what genes is the
        chromosome composed of and also what alleles are valid
        """
        self.genotype = genotype
        self._alleles = []

    @property
    def alleles(self):
        return self._alleles.copy()

    def allele_of(self, gene_name):
        gene = self.genotype.gene(gene_name)
        i = self.genotype.genes.index(gene)
        return self.alleles[i]

    def mutate(self, chance=Config.instance().mutation_chance):
        """Mutate the chromosome"""
        genes = self.genotype.mutable_genes
        random.shuffle(genes)
        for gene in genes:
            if random.random() < chance:
                self.mutate_gene(gene)

    def mutate_gene(self, gene=None, name=None):
        """Mutate a selected gene"""
        if gene is None:
            gene = self.genotype.gene(name)

        if gene not in self.genotype.mutable_genes:
            raise ValueError('Gene {} is not mutable'.format(gene.name))

        i = self.genotype.genes.index(gene)
        different_alleles = [allele for allele in gene.alleles if allele != self.allele_of(gene.name)]
        self._alleles[i] = random.choice(different_alleles)

    def randomize(self):
        """Randomize the chromosome. Each mutable gene could change."""
        for gene in self.genotype.mutable_genes:
            if random.randint(0, 1):
                self.mutate_gene(gene)

    def recombine_with(self, other, technique):
        new_self, new_other = technique(self, other)
        self._alleles = new_self.alleles
        other._alleles = new_other.alleles

    @staticmethod
    def recombination_of(chromosome_a, chromosome_b, technique=None):
        if technique is None:
            technique = Config.instance().recombination
        return technique(chromosome_a, chromosome_b)

    @staticmethod
    def from_string(string, genotype):
        builder = ChromosomeBuilder(genotype)
        for gene in genotype.genes:
            allele_length = gene.allele_length  # Genotype is guaranteed to have at least one allele.
                                                               # Also, all alleles are of the same length
            if len(string) < allele_length:
                raise ValueError('Provided string cannot be parsed as a chromosome. It is missing some genes.')

            allele = string[:allele_length]
            builder.allele(gene.name, allele)
            string = string[allele_length:]

        if len(string) > 0:
            raise ValueError('Provided string cannot be parsed as a chromosome. It has additioanl data.')

        return builder.create_chromosome()

    @staticmethod
    def random_from(chromosome):
        result = Chromosome(chromosome.genotype)
        result._alleles = chromosome.alleles
        result.randomize()
        return result

    def __str__(self):
        return ''.join(self.alleles)

    def __eq__(self, other):
        if isinstance(other, Chromosome):
            return self.genotype == other.genotype and self.alleles == other.alleles
        else:
            return False

    def __hash__(self):
        return hash(str(self))


class ChromosomeBuilder:

    def __init__(self, genotype):
        self.genotype = genotype
        self.alleles = OrderedDict()

    def allele(self, gene_name, allele):
        gene = self.genotype.gene(gene_name)

        if allele not in gene.alleles:
            raise GenotypeException('Allele {} is not valid for gene {}'.format(allele, gene_name))

        self.alleles[gene_name] = allele
        return self

    def create_chromosome(self):
        alleles = []
        for gene in self.genotype.genes:
            alleles.append(self.alleles[gene.name])

        chromosome = Chromosome(self.genotype)
        chromosome._alleles = alleles
        return chromosome