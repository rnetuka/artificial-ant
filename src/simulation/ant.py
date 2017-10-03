from enum import Enum


class Action(Enum):

    WAIT       = 0
    TURN_LEFT  = 1
    TURN_RIGHT = 2
    MOVE       = 3

    def encode(self):
        """Encode the action into binary string"""
        return bin(self.value)[2:]

    def __call__(self, ant):
        methods = [Ant.wait, Ant.turn_left, Ant.turn_right, Ant.move]
        methods[self.value](ant)


class Ant:

    def __init__(self, state_machine, input_bus=None):
        self.state_machine = state_machine

        # for simulation purpose only
        self.turn_left_listener = None
        self.turn_right_listener = None
        self.move_listener = None
        self.input_bus = input_bus

    def scan(self):
        """Scans if food pellet is in the front of the ant"""
        if self.input_bus is not None:
            return self.input_bus.bait_in_sight

    def turn_left(self):
        # for simulation purpose only
        if self.turn_left_listener is not None:
            self.turn_left_listener()

        # placeholder for mechanical turn

    def turn_right(self):
        # for simulation purpose only
        if self.turn_right_listener is not None:
            self.turn_right_listener()

        # placeholder for mechanical turn

    def wait(self):
        pass

    def move(self):
        """Move the ant forward"""

        # for simulation purpose only
        if self.move_listener is not None:
            self.move_listener()

        # placeholder for mechanical move forward

    def perform_action(self):
        input = self.scan()
        action = Action(self.state_machine.read(input))
        action(self)


class InputBus:

    def __init__(self):
        self.bait_in_sight = False

    def clear(self):
        self.bait_in_sight = False