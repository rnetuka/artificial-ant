import math

from src.genetics.chromosome import Chromosome
from src.genetics.chromosome import ChromosomeBuilder
from src.genetics.gene import Gene
from src.genetics.genotype import GenotypeBuilder


class StateMachineError(Exception):
    pass


class State:

    def __init__(self, index, bin):
        self.index = index
        self.bin = bin

    def __str__(self):
        return str(self.index) + '(' + self.bin + ')'

    @staticmethod
    def decode(bin):
        return State(int(bin, 2), bin)


class Input:

    def __init__(self, value, bin):
        self.value = value
        self.bin = bin

    def __str__(self):
        return str(self.value) + '(' + self.bin + ')'

    @staticmethod
    def decode(bin):
        return Input(bool(int(bin)), bin)


class Output:

    def __init__(self, value, bin):
        self.value = value
        self.bin = bin

    def __str__(self):
        return str(self.value) + '(' + self.bin + ')'

    @staticmethod
    def decode(bin):
        return Output(int(bin, 2), bin)


class Rule:

    def __init__(self, state_from, input, state_to, output):
        self.state_from = state_from
        self.input = input
        self.state_to = state_to
        self.output = output

    def __str__(self):
        return '{} + {} -> {} + {}'.format(self.state_from, self.input, self.state_to, self.output)


class AntStateMachine:

    def __init__(self):
        self.states = []
        self.input_alphabet = (Input(True, '1'), Input(False, '0'))
        self.output_alphabet = (Output(0, '00'), Output(1, '01'), Output(2, '10'), Output(3, '11'))
        self.rules = []
        self.initial_state = None
        self.current_state = None

    def switch_to(self, state):
        """
        :param state:   state index
        :return:
        """
        self.current_state = state

    def rule_for(self, input):
        applicable_rules = [rule for rule in self.rules if rule.state_from.index == self.current_state and rule.input.value == input]

        if len(applicable_rules) == 0:
            raise StateMachineError('No rule for combination {} + {}'.format(self.current_state, input))

        if len(applicable_rules) > 1:
            raise StateMachineError('More than one rule applicable for {} + {}'.format(self.current_state, input))

        return applicable_rules[0]

    def read(self, input):
        if input not in [input_obj.value for input_obj in self.input_alphabet]:
            raise StateMachineError('Unable to precess input {}. Not in input alphabet.'.format(input))

        rule = self.rule_for(input)
        self.switch_to(rule.state_to.index)
        return rule.output.value

    @staticmethod
    def decode_state(state):
        return int(state, 2)

    @staticmethod
    def decode_input(input):
        return bool(int(input))

    @staticmethod
    def decode_output(output):
        return int(output, 2)

    @property
    def genotype(self):
        builder = GenotypeBuilder()

        for i, rule in enumerate(self.rules):
            builder.add(Gene('FRM{}'.format(i), [state.bin for state in self.states], mutable=False))
            builder.add(Gene('IN{}'.format(i), [input.bin for input in self.input_alphabet], mutable=False))
            builder.add(Gene('TO{}'.format(i), [state.bin for state in self.states]))
            builder.add(Gene('OUT{}'.format(i), [output.bin for output in self.output_alphabet]))

        return builder.create_genotype()

    def to_chromosome(self):
        builder = ChromosomeBuilder(self.genotype)

        for i, rule in enumerate(self.rules):
            builder.allele('FRM{}'.format(i), rule.state_from.bin)
            builder.allele('IN{}'.format(i), rule.input.bin)
            builder.allele('TO{}'.format(i), rule.state_to.bin)
            builder.allele('OUT{}'.format(i), rule.output.bin)

        return builder.create_chromosome()

    @staticmethod
    def state_count(chromosome):
        genes = [gene for gene in chromosome.genotype.genes if gene.name.startswith('FRM')]
        return 0 if len(genes) == 0 else len(genes[0].alleles)

    @staticmethod
    def rule_count(chromosome):
        genes = [gene for gene in chromosome.genotype.genes if gene.name.startswith('FRM')]
        return len(genes)

    @staticmethod
    def from_chromosome(chromosome):
        builder = AntStateMachineBuilder()
        builder.state_count(AntStateMachine.state_count(chromosome))
        builder.initial_state(0)

        for i in range(AntStateMachine.rule_count(chromosome)):
            state_from = State.decode(chromosome.allele_of('FRM{}'.format(i))).index
            input = Input.decode(chromosome.allele_of('IN{}'.format(i))).value
            state_to = State.decode(chromosome.allele_of('TO{}'.format(i))).index
            output = Output.decode(chromosome.allele_of('OUT{}'.format(i))).value

            builder.rule(state_from, input, state_to, output)

        return builder.create_state_machine()

    @staticmethod
    def from_chromosome_string(chromosome_string, genotype):
        return AntStateMachine.from_chromosome(Chromosome.from_string(chromosome_string, genotype))


class AntStateMachineBuilder:

    def __init__(self):
        self._states = []
        self._rules = []
        self._initial_state = None

    def state_count(self, count):
        padding_length = math.ceil(math.sqrt(count))
        self._states = [State(i, format(i, '0%ib' % padding_length)) for i in range(count)]
        return self

    def initial_state(self, initial_state):
        if initial_state not in [state.index for state in self._states]:
            raise ValueError('{} is not a part of state machine states'.format(initial_state))

        self._initial_state = initial_state
        return self

    def rule(self, state_from, input, state_to, output):
        if state_from not in [state.index for state in self._states]:
            raise ValueError('{} is not a part of state machine states'.format(state_from))

        if state_to not in [state.index for state in self._states]:
            raise ValueError('{} in not s part of state machine states'.format(state_to))

        if input not in (True, False):
            raise ValueError('Invalid input {}, could only be one of: True, False'.format(input))

        self._rules.append(Rule(self._states[state_from], Input(input, '1' if input else '0'), self._states[state_to], Output(output, format(output, '02b'))))

    def create_state_machine(self):
        state_machine = AntStateMachine()
        state_machine.states = self._states.copy()
        state_machine.initial_state = self._initial_state
        state_machine.current_state = self._initial_state
        state_machine.rules = self._rules.copy()
        return state_machine

    @staticmethod
    def create_prototype(states_no=4):
        builder = AntStateMachineBuilder()
        builder.state_count(states_no)
        for i in range(states_no):
            builder.rule(i, True, i, 3) # move
            builder.rule(i, False, i, 2) # turn right
        return builder.create_state_machine()