import getopt
import sys

from getopt import  GetoptError

from src.ui.main_window import ArtificialAntApplication
from src.simulation.simulation import Simulation
from src.simulation.statemachine import AntStateMachine
from src.evolution.evolution import Evolution
from src.config import Config

if __name__ == '__main__':
    gui = False
    chromosome = None  # '000110011000000110001101100001001010010100000010010010011101001011000010100101111100001111'

    try:
        options, arguments = getopt.getopt(sys.argv[1:], 'hc:g', ['gui', 'help', 'chromosome='])
    except GetoptError:
        print('usage: python3 main.py [--gui] [-c <chromosome>]')
        sys.exit(1)

    for option, argument in options:

        if option in ('-h', '--help'):
            print('usage: python3 main.py [--gui] [-c <chromosome>]')

        if option in ('-g', '--gui'):
            gui = True

        if option in ('-c', '--chromosome'):
            chromosome = argument

    config = Config.load()
    evolution = Evolution(config)

    if chromosome:
        state_machine = AntStateMachine.from_chromosome_string(chromosome, evolution.genotype)
        score = evolution.evaluate(state_machine.to_chromosome())
    else:
        evolution = Evolution(config)
        best_individual = evolution.start()
        state_machine = AntStateMachine.from_chromosome(best_individual.chromosome)
        score = best_individual.fitness

        print('Best found state machine:')
        print(state_machine.to_chromosome())

    simulation = Simulation(state_machine, grid=config.grid())

    if gui:
        gui_application = ArtificialAntApplication(simulation)
        gui_application.run(sys.argv)
    else:
        # Run in command line
        print(str(score))



# 000101101000000110001100111001010011010101011010000101011100111011000011100101111100001111
# 41 out of 88 baits eaten 46% in 500 steps

# 000110011000000110001101100001001010010100000010010010011101001011000010100101111100001111
# 87 out of 88 baits eaten 98% in 500 steps