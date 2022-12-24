from collections import defaultdict
from collections import deque
from functools import cache
from math import inf

from utils import split_lines


def print_graph(graph):
    ymin = 0
    ymax = int(max(graph.keys(), key=lambda x: x.imag).imag)
    xmin = 0
    xmax = int(max(graph.keys(), key=lambda x: x.real).real)

    for i in range(ymin, ymax + 1):
        print(
            "".join("1" if complex(j, i) in graph else ".")
            for j in range(xmin, xmax + 1)
        )


@cache
def neighbors(coord):
    # Middle of each tuple is target
    return {
        "nw": coord + (-1 - 1j),
        "n": coord - 1j,
        "ne": coord + (1 - 1j),
        "e": coord + 1,
        "se": coord + (1 + 1j),
        "s": coord + 1j,
        "sw": coord + (-1 + 1j),
        "w": coord - 1,
    }


def parse_board(lines):
    result = set()
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "#":
                result.add(complex(j, i))
    return result


def simulate(board, iterations, until_stable=False):
    directions = deque(
        [("n", "ne", "nw"), ("s", "se", "sw"), ("w", "nw", "sw"), ("e", "ne", "se")]
    )

    i = 1
    new = board.copy()
    while i <= iterations:
        propositions = defaultdict(lambda: [])
        changed = 0
        previous = new.copy()

        for elf in board:
            elf_neighbors = neighbors(elf)
            occupied = {
                dir: coord for dir, coord in elf_neighbors.items() if coord in board
            }
            if occupied == {}:
                continue
            found = occupied.keys()
            for direction in directions:
                if not (
                    direction[0] in found
                    or direction[1] in found
                    or direction[2] in found
                ):
                    target = elf_neighbors[direction[0]]
                    assert target not in board
                    propositions[target].append(elf)
                    break
        for target, elf in propositions.items():
            if len(elf) == 1:
                board.add(target)
                board.remove(elf[0])
                changed += 1

        new = board.copy()
        if until_stable and changed == 0:
            return i
        directions.rotate(-1)
        i += 1
    return board


# Get 8 neighbor tiles
# If none occupied, break
# Else for each direction:
# If no elf in corresponding tiles
# Add this elf and target tile to propositions
# Else add target to overloaded

# For elf, target in propositions:
# Move elf to tile


def count_empty(board):
    xmin = ymin = inf
    xmax = ymax = -inf
    total = 0

    for k in board:
        xmin = min(xmin, k.real)
        xmax = max(xmax, k.real)
        ymin = min(ymin, k.imag)
        ymax = max(ymax, k.imag)
        total += 1

    return ((xmax - xmin + 1) * (ymax - ymin + 1)) - total


raw_input = split_lines("inputs/day23.txt")

start = parse_board(raw_input)
result = simulate(start.copy(), 10)
part1 = int(count_empty(result))
print(part1)

part2 = simulate(start, inf, True)
print(part2)
