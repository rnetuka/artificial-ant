from src.evolution.individual import Individual
from src.evolution.fitness import Fitness
from src.config import Config
from src.simulation.simulation import Simulation
from src.simulation.statemachine import AntStateMachine


class ProvingGrounds:
    """Proving grounds where individuals test their skills and are assigned fitness in the end of the process"""

    def __init__(self):
        self.__grid = Config.instance().grid()
        self.__total_baits = self.__grid.remaining_baits()
        self.__score_board = {}

    def evaluate(self, individual: Individual) -> Fitness:
        """Evaluate an individual on the proving grounds. Return a fitness of this individual."""

        if individual not in self.__score_board:
            baits_eaten, steps_used = Simulation(AntStateMachine.from_chromosome(individual.chromosome), self.__grid).run()
            fitness = Fitness.from_result(self.__total_baits, baits_eaten, steps_used)
            self.__score_board[individual] = fitness

        return self.__score_board[individual]
