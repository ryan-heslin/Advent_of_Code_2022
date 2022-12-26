from collections import defaultdict
from collections import deque
from collections import namedtuple
from math import copysign
from math import inf

from utils import split_lines

# NOTE: may want to use right-hand coordinates (x increases, y increases) to consistently handle blizzardd direction


def parse(lines):
    start = complex(lines[0][1:].find("."), -1)
    width = len(lines[0]) - 2
    stop = width + 1
    height = len(lines) - 2
    end = complex(
        lines[-1][1:].find("."),
        height,
    )
    translations = {">": 1, "<": 2, "^": 4, "v": 8}
    result = defaultdict(lambda: 0)

    for i, line in enumerate(lines[1 : (height + 1)]):
        for j, char in enumerate(line[1:stop]):
            if char != ".":
                result[complex(j, i)] = translations[char]
                # No verticals on start/end cols
                assert not (
                    j in (0, width - 1) and i in (0, height - 1) and char in ("v", "^")
                )

    return result, width, height, start, end


def advance_state(grid, height, width):
    new = defaultdict(lambda: 0)
    # += 1 for horizontal, -+ 1j for vertical
    for coord, blizzard in grid.items():
        # Bit encoding: {">": 1, "<": 2, "^": 4, "v": 8}
        # Negative modulo is safe
        if blizzard & 1:
            new[complex((coord.real + 1) % width, coord.imag)] += 1

        blizzard >>= 1
        if blizzard & 1:
            new[complex((coord.real - 1) % width, coord.imag)] += 2

        blizzard >>= 1
        if blizzard & 1:  # left/right
            new[complex(coord.real, (coord.imag - 1) % height)] += 4

        blizzard >>= 1
        if blizzard & 1:  # left/right
            new[complex(coord.real, (coord.imag + 1) % height)] += 8

    # assert max(new.values()) < 16
    return new


def search(graph, start, goal, height, width):
    states = {0: graph}
    xmin = ymin = 0
    xmax = width - 1
    ymax = height - 1
    top_target = goal.real == -1
    period = width * height
    best = inf
    visited = set()

    # state index, coord
    start = (0, start)
    Q = deque([start])

    while Q:
        current = Q.popleft()
        index, coord = current
        print(coord)
        visited.add(current)
        this_iter = index + 1

        if coord == goal:
            best = min(index, best)
        else:
            # Skip if even ideal completion time too slow
            if index < best and abs(coord.real - goal.real) + abs(
                coord.imag - goal.imag
            ) < (best - index):
                # reduced_index = this_iter % period
                next_state = states.get(
                    this_iter, advance_state(states[index], height, width)
                )
                states[index] = next_state
                neighbors = deque([])

                # Okay to wait
                if next_state[coord] < 1 and (new := (this_iter, coord)) not in visited:
                    neighbors.append(new)
                # Left, up, right, down
                if (
                    (coord.real > xmin and coord.imag <= ymax)
                    and next_state[(new_coord := coord - 1)] < 1
                    and (new := (this_iter, new_coord)) not in visited
                ):
                    neighbors.append(new)
                # Up; I guess we don't move back into start square
                # Final move for backward case
                if (
                    (coord.imag > ymin or coord - 1j == goal)
                    and next_state[(new_coord := coord - 1j)] < 1
                    and (new := (this_iter, new_coord)) not in visited
                ):
                    neighbors.append(new)
                if (
                    (coord.real < xmax and coord.imag >= ymin)
                    and next_state[(new_coord := coord + 1)] < 1
                    and (new := (this_iter, new_coord)) not in visited
                ):
                    neighbors.append(new)
                if (
                    (coord.imag < ymax or coord + 1j == goal)
                    and next_state[(new_coord := coord + 1j)] < 1
                    and (new := (this_iter, new_coord)) not in visited
                ):
                    neighbors.append(new)
                # In reverse order, so last added go first
                # if top_target:
                #     neighbors.reverse()
                Q.extendleft(neighbors)

    return best, states[int(best)]


raw_input = split_lines("inputs/day24.txt")
graph, width, height, start, end = parse(raw_input)
assert start == -1j
part1, end_state = search(graph, start, end, height, width)
print(part1)
stage2, end_state = search(end_state, end, start, height, width)
stage3, _ = search(end_state, start, end, height, width)
part2 = part1 + stage2 + stage3
print(part2)
# 155 too low

# Move before check
# If old position has blizzard, must move; otherwise, can wait
