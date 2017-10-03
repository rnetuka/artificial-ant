class Genotype:
    """Genotype is a representation of gene sequence with all possible alleles for each such gene. The Genotype class
    is immutable.
    """

    def __init__(self, genes):
        self._genes = genes

    @property
    def genes(self):
        """Return a list of genes for this genotype."""
        return self._genes.copy()

    @property
    def mutable_genes(self):
        return [gene for gene in self._genes if gene.is_mutable()]

    def gene(self, name):
        try:
            return next(gene for gene in self._genes if gene.name == name)
        except StopIteration:
            raise ValueError('{} is not in this genotype'.format(name))

    def is_valid_chromosome(self, chromosome_string):
        for gene in self._genes:
            allele_length = len(gene.alleles[0])

            if len(chromosome_string) < allele_length:
                return False

            allele = chromosome_string[:allele_length]
            if allele not in gene.alleles:
                return False

            chromosome_string = chromosome_string[allele_length:]

        if len(chromosome_string) > 0:
            return False

        return True

    def __str__(self):
        return 'Genotype: ' + ' '.join(str(gene) + ' ' + str(gene.alleles) for gene in self._genes)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._genes == other._genes
        else:
            return False


class GenotypeBuilder:

    def __init__(self):
        self._genes = []

    def add(self, gene):
        self._genes.append(gene)
        return self

    def create_genotype(self):
        return Genotype(self._genes)



class GenotypeException(Exception):

    def __init__(self, message):
        super().__init__(message)