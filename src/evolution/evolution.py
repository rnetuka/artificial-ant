from src.config import Config
from src.genetics.chromosome import Chromosome
from src.genetics.genotype import Genotype
from src.simulation.statemachine import AntStateMachineBuilder
from src.evolution.fitness import Fitness
from src.evolution.proving_grounds import ProvingGrounds
from src.evolution.individual import Individual


class Evolution:

    def __init__(self, config: Config=Config.load()):
        self.config = config
        self.population = []
        self.proving_grounds = ProvingGrounds()

    @property
    def chromosome_prototype(self) -> Chromosome:
        return AntStateMachineBuilder.create_prototype(self.config.statemachine_size()).to_chromosome()

    @property
    def genotype(self) -> Genotype:
        return self.chromosome_prototype.genotype

    @property
    def best_individual(self) -> Individual:
        return None if len(self.population) == 0 else sorted(self.population, reverse=True)[0]

    def create_initial_population(self) -> list:
        prototype = self.chromosome_prototype
        chromosomes = [prototype]
        chromosomes += [Chromosome.random_from(prototype) for _ in range(self.config.population_size() - 1)]
        individuals = list(map(Individual, chromosomes))
        for individual in individuals:
            individual.prove_yourself_on(self.proving_grounds)
        return individuals

    def select_parents(self) -> list:
        return self.config.parent_selection(self.population, self.config.parent_count())

    def next_generation(self):
        parents = self.select_parents()
        children = []

        for i in range(0, len(parents), 2):
            father, mother = parents[i], parents[i + 1]
            child1, child2 = father.mate_with(mother)
            child1.prove_yourself_on(self.proving_grounds)
            child2.prove_yourself_on(self.proving_grounds)
            children += [child1, child2]

        deceased = self.config.decease_selection(self.population, self.config.decease_count())

        for individual in deceased:
            self.population.remove(individual)

        for child in children:
            self.population.append(child)

    def evaluate(self, chromosome: Chromosome) -> Fitness:
        individual = Individual(chromosome)
        individual.prove_yourself_on(self.proving_grounds)
        return individual.fitness

    def start(self, years: int=None) -> Individual:

        if years is None:
            years = self.config.evolution_years()

        if years <= 0:
            raise ValueError('Cannot start evolution. Invalid length of {} years.'.format(years))

        self.population = self.create_initial_population()

        print('Starting evolution of {} ants.'.format(len(self.population)))
        print('Year 0. Best individual: {}'.format(self.best_individual.fitness))

        for year in range(1, years + 1):
            self.next_generation()

            print('Year {}. Best individual: {}'.format(year, self.best_individual.fitness))

        return self.best_individual
