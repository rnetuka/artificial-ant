class Gene:

    def __init__(self, name, alleles, mutable=True):
        if len(alleles) < 1:
            raise ValueError('Gene must have at least one allele')

        self._name = name
        self._alleles = alleles.copy()
        self._mutable = mutable

    @property
    def name(self):
        return self._name

    @property
    def alleles(self):
        return self._alleles.copy()

    @property
    def allele_length(self):
        return len(self._alleles[0])

    def is_mutable(self):
        return self._mutable and len(self._alleles) > 1

    def is_immutable(self):
        return not self.is_mutable()

    def __str__(self):
        return self._name

    def __eq__(self, other):
        if isinstance(other, Gene):
            return self.name == other.name and self.alleles == other.alleles and self.is_mutable() == other.is_mutable()
        else:
            return False