import copy

from src.config import Config
from src.simulation.ant import Ant
from src.simulation.ant import InputBus


class Simulation:

    ANT_FACING_NORTH = (0, -1)
    ANT_FACING_SOUTH = (0, 1)
    ANT_FACING_WEST = (-1, 0)
    ANT_FACING_EAST = (1, 0)

    def __init__(self, state_machine, grid, ant_position=(0, 0), ant_direction=ANT_FACING_EAST, max_steps=Config.instance().ant_steps()):
        self.input_bus = InputBus()
        self.ant = Ant(state_machine, self.input_bus)

        self.ant.turn_left_listener = self.turn_ant_left
        self.ant.turn_right_listener = self.turn_ant_right
        self.ant.move_listener = self.move_ant

        self._grid = copy.deepcopy(grid)
        self.total_baits = self._grid.remaining_baits()

        self._ant_position = ant_position
        self.ant_direction = ant_direction

        self.max_steps = max_steps
        self.steps_used = 0

    @property
    def ant_position(self):
        return self._ant_position

    @property
    def ant_facing_direction(self):
        return {Simulation.ANT_FACING_NORTH: 'north', Simulation.ANT_FACING_SOUTH: 'south', Simulation.ANT_FACING_WEST: 'west', Simulation.ANT_FACING_EAST: 'east'}[self.ant_direction]

    @property
    def grid(self):
        return self._grid

    def turn_ant_left(self):
        self.turn_ant(-1)

    def turn_ant_right(self):
        self.turn_ant(1)

    def turn_ant(self, direction):
        directions = [Simulation.ANT_FACING_NORTH, Simulation.ANT_FACING_EAST, Simulation.ANT_FACING_SOUTH, Simulation.ANT_FACING_WEST]
        i = directions.index(self.ant_direction) + direction
        i %= len(directions)
        self.ant_direction = directions[i]

    def move_ant(self):
        x, y = self.ant_position
        dx, dy = self.ant_direction

        if self._grid.is_in_bounds(x + dx, y + dy):
            x += dx
            y += dy

            if self._grid.has_bait_at(x, y):
                self._grid.remove_bait_from(x, y)

            self._ant_position = (x, y)

    def do_tick(self):
        if self.steps_used < self.max_steps:
            x, y = self.ant_position
            dx, dy = self.ant_direction

            self.input_bus.bait_in_sight = self._grid.has_bait_at(x, y, dx, dy)
            self.ant.perform_action()
            self.steps_used += 1

    def run(self):
        """Run the simulation. Return number of baits eaten and steps used."""
        while self.steps_used < self.max_steps:
            self.do_tick()

            if self._grid.remaining_baits() == 0:
                break

        baits_eaten = self.total_baits - self._grid.remaining_baits()
        return baits_eaten, self.steps_used


