import re
from math import inf

from utils import l1
from utils import split_lines


def parse_line(line):
    numbers = [int(x) for x in re.findall(r"-?\d+", line)]
    return Sensor(tuple(numbers[:2]), tuple(numbers[2:]))


def interval_overlap(intervals):
    # Assume no point intervals
    intervals = sorted(set(intervals))
    total = 0
    highest_endpoint = -inf

    while intervals:
        current = intervals.pop(0)
        # Skip intervals contained in previous intervals
        if current[1] > highest_endpoint:
            lower_bound = (
                highest_endpoint if current[0] < highest_endpoint else current[0]
            )
            total += current[1] - lower_bound
            # Must be greater than previous
            highest_endpoint = current[1]

    return total


def find_intervals(sensors, y):
    intervals = []
    for sens in sensors:
        this_exclusion = sens.exclusions_in_row(y)
        if this_exclusion:
            intervals.append(this_exclusion)
    return intervals


def check_intervals(intervals, xmin, xmax):
    intervals = sorted(set(intervals))

    # TODO Optimization: find max overlap of any two intervals, return it, skip that many rows
    candidate = xmin
    while intervals and candidate <= xmax:
        current = intervals.pop(0)
        if current[0] > candidate:
            if candidate >= xmax:
                break
            else:  # Valid coordinate within range
                return candidate
        candidate = max(current[1] + 1, candidate)
    return None


def frequency(coord):
    return coord[0] * 4000000 + coord[1]


class Sensor:

    # Diamond of equal Manhattan distance centered on center
    def __init__(self, center, beacon) -> None:
        self.center = center
        self.distance = l1(self.center, beacon)
        self.xmin = self.center[0] - self.distance
        self.xmax = self.center[0] + self.distance

    # Get endpoints (inclusive) of excluded area given a y-coordinate
    def exclusions_in_row(self, y):
        offset = abs(y - self.center[1])
        if offset > self.distance:
            return None
        return (self.xmin + offset, self.xmax - offset)


raw_input = split_lines("inputs/day15.txt")
sensors = [parse_line(line) for line in raw_input]
y = 2000000
part1_intervals = find_intervals(sensors, y)
part1 = interval_overlap(part1_intervals)
print(part1)

xmin = ymin = 0
xmax = ymax = 4000000
beacon = None

for y in range(ymax + 1):
    this_intervals = find_intervals(sensors, y)
    coordinate = check_intervals(this_intervals, xmin, xmax)
    if coordinate:
        beacon = (coordinate, y)
        break

part2 = frequency(beacon)
print(part2)
