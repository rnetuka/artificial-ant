import math


class Fitness:

    def __init__(self, baits_eaten: int, total_baits: int, steps_used: int):
        self.__baits_eaten = baits_eaten
        self.__total_baits = total_baits
        self.__steps_used = steps_used

    @property
    def baits_eaten(self) -> int:
        return self.__baits_eaten

    @property
    def steps_used(self) -> int:
        return self.__steps_used

    @property
    def success_rate(self) -> int:
        """Return a percentage of all baits eaten by the ant"""
        return int(math.floor(self.__baits_eaten / self.__total_baits * 100))

    def __str__(self) -> str:
        return '{} out of {} baits eaten {}% in {} steps'.format(self.baits_eaten, self.__total_baits, self.success_rate, self.steps_used)

    def __eq__(self, other) -> bool:
        return self.success_rate == other.success_rate and self.steps_used == other.steps_used if isinstance(other, Fitness) else False

    def __gt__(self, other) -> bool:
        if self.success_rate > other.success_rate:
            return True
        elif self.success_rate == other.success_rate:
            return self.steps_used < other.steps_used
        else:
            return False

    def __ge__(self, other) -> bool:
        if self.success_rate > other.success_rate:
            return True
        elif self.success_rate == other.success_rate:
            return self.steps_used < other.steps_used or self.steps_used == other.steps_used
        else:
            return False

    @staticmethod
    def unspecified():
        return Fitness(0, 1, 100)

    @staticmethod
    def from_result(total_baits: int, baits_eaten: int, steps_used: int):
        return Fitness(baits_eaten, total_baits, steps_used)
