from collections import defaultdict
from functools import reduce
from math import copysign

from utils.utils import split_lines

ROCK = "#"
SAND = "o"
EMPTY = "."
MAP = defaultdict(lambda: EMPTY)


class Cave:
    def __init__(self, map, origin):
        self.map = map.copy()
        self.origin = origin

    def simulate(self):
        fallen = 0

        current = self.origin
        while True:
            target = self.highest_beneath(current)
            # This doesn't move if already resting on solid
            if MAP[self.origin] == SAND or target is None:
                return fallen
                # If stopped from origin point, all blocked
            current = (current[0], target[1] - 1)
            # Fill in pyramid all at once:

            if self.map[(southwest := (current[0] - 1, current[1] + 1))] == EMPTY:
                current = southwest
            elif self.map[(southeast := (current[0] + 1, current[1] + 1))] == EMPTY:
                current = southeast
            else:
                self.map[current] = SAND
                fallen += 1
                current = self.origin
            # Nowhere left to fall; start over

    def highest_beneath(self, coord):
        beneath = list(
            filter(
                lambda other: __class__.below(other, coord)
                and self.map[other] != EMPTY,
                self.map.keys(),
            )
        )
        if not beneath:
            return None
        return min(beneath, key=lambda coord: coord[1])

    @staticmethod
    def below(first, second):
        # Is first below second?
        return first[0] == second[0] and first[1] > second[1]


class BoundedCave(Cave):
    def __init__(self, map, origin):
        super().__init__(map, origin)
        self.floor = max(coord[1] for coord in map.keys()) + 2

    def highest_beneath(self, coord):
        x, y = coord
        # Count up here
        for i in range(y + 1, self.floor, 1):
            this = (x, i)
            if self.map[this] != EMPTY:
                return this
        else:
            # Floor is always at very bottom
            return (x, self.floor)

    def simulate(self):
        fallen = 0

        current = self.origin
        while True:
            target = self.highest_beneath(current)
            # This doesn't move if already resting on solid
            # If stopped from origin point, all blocked
            current = (current[0], target[1] - 1)

            above_floor = current[1] < self.floor - 1
            if (
                above_floor
                and self.map[(southwest := (current[0] - 1, current[1] + 1))] == EMPTY
            ):
                current = southwest
            elif (
                above_floor
                and self.map[(southeast := (current[0] + 1, current[1] + 1))] == EMPTY
            ):
                current = southeast
            else:
                fallen += 1
                self.map[current] = SAND
                if current == self.origin:
                    return fallen
                current = self.origin


def draw_segment(start, end):
    end = tuple(map(int, end.split(",")))
    common_dimension = int(start[1] == end[1])
    different_dimension = int(not common_dimension)
    difference = start[different_dimension] - end[different_dimension]
    sign = int(copysign(1, difference))
    basis = list(end)
    # Start should have been marked in previous iteration
    # This iteration's end becomes start of next
    for _ in range(end[different_dimension], start[different_dimension], sign):
        MAP[tuple(basis)] = ROCK
        basis[different_dimension] += sign
    return end


def parse_segments(line):
    coords = line.split(" -> ")
    coords[0] = tuple(int(x) for x in coords[0].split(","))
    MAP[coords[0]] = ROCK
    reduce(draw_segment, coords)


raw_input = split_lines("inputs/day14.txt")

for line in raw_input:
    parse_segments(line)

cave1 = Cave(MAP, (500, 0))
part1 = cave1.simulate()
print(part1)

cave2 = BoundedCave(MAP, (500, 0))
part2 = cave2.simulate()
print(part2)
