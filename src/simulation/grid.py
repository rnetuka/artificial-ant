class Grid:

    def __init__(self, width, height, baits=list()):
        self._width = width
        self._height = height
        self._baits = baits.copy()

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def baits(self):
        return self._baits.copy()

    def is_in_bounds(self, x, y):
        return 0 <= x < self._width and 0 <= y < self._height

    def has_bait_at(self, x, y, dx=0, dy=0):
        if dx != 0 or dy != 0:
            if 0 > x + dx >= self._width:
                return False
            if 0 > y + dy >= self._height:
                return False

            return (x + dx, y + dy) in self._baits

        if not 0 <= x < self._width or not 0 <= y < self._height:
            raise ValueError('Coordinates not in grid\'s bounds: (%i, %i)' % (x, y))

        return (x, y) in self._baits

    def remove_bait_from(self, x, y):
        if not self.has_bait_at(x, y):
            raise ValueError('No bait at (%i, %i)' % (x, y))

        self._baits.remove((x, y))

    def remaining_baits(self):
        return len(self._baits)

    @staticmethod
    def from_file(path):
        width = 0
        height = 0
        baits = []
        with open(path) as file:
            lines = file.read().splitlines()
            for line in lines:
                width = max(width, len(line))
                height += 1
                for i, char in enumerate(line):
                    if char == '*':
                        baits.append((i, height - 1))
        return Grid(width, height, baits)

    def __str__(self):
        string = ''
        for y in range(self._height):
            for x in range(self._width):
                string += '*' if self.has_bait_at(x, y) else ' '
            string += '\n'
        return string.rstrip('\n')