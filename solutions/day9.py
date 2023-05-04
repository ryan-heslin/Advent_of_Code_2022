from collections import defaultdict

import numpy as np

mask = np.zeros((15, 15))

directions = {
    "R": lambda x: (x, 0),
    "D": lambda x: (0, -x),
    "L": lambda x: (-x, 0),
    "U": lambda x: (0, x),
}

adjacents = [
    [1, 1],
    [-1, 1],
    [-1, -1],
    [1, -1],
    [0, 1],
    [1, 0],
    [-1, 0],
    [0, -1],
    [0, 0],
]
# Tuple with index replaced with value
def update_tuple(tupe, i, value):
    return (x if j != i else value for j, x in enumerate(tupe))


def l1(x, y):
    return sum(abs(xi - yi) for xi, yi in zip(x, y))


def l2(x, y):
    return (sum((xi - yi) ** 2 for xi, yi in zip(x, y))) ** (0.5)


def clip(x):
    absolute = abs(x)
    return (absolute - 1) * (absolute / x)


def parse(line):
    direction, value = line.split()
    return directions[direction](int(value))


class State:
    def __init__(self, head_start, tail_start) -> None:
        self.head = list(head_start)
        self.tail = list(tail_start)
        self.touched = defaultdict(lambda: 0)
        self.touched[tuple(tail_start)] += 1

    def move(self, offset):
        # 0 -> same coordinate:
        # 1 -> beside
        # 2 -> diagonal
        # else -> error
        # (0, 0) is no-op

        if offset != [0, 0]:
            orig_distance = l1(self.head, self.tail)
            target = (self.head[0] + offset[0], self.head[1] + offset[1])
            dynamic_dimension = int(offset[1] != 0)
            static_dimension = (dynamic_dimension + 1) % 2
            sign = -1 if target[dynamic_dimension] < self.head[dynamic_dimension] else 1

            self.head[dynamic_dimension] += sign
            # print(f"New head: {self.head}")
            # print(self.touched.keys())
            # print("\n")
            offset[dynamic_dimension] -= sign
            new_distance = l1(self.head, self.tail)

            match (orig_distance, new_distance):
                case (0, 1):
                    self.advance(target, sign, static_dimension, dynamic_dimension)
                    # Moving from same space
                case (1, 0):
                    self.move(offset)  # Reversing direction, moving onto rope
                case (1, 2):  # Either moving straight away, or beside -> diagonal
                    if (
                        self.head[static_dimension] == self.tail[static_dimension]
                    ):  # Being dragged behind

                        self.tail[static_dimension] = self.head[static_dimension]
                        self.tail[dynamic_dimension] = (
                            self.head[dynamic_dimension] - sign
                        )
                        self.touched[tuple(self.tail)] += 1
                        self.advance(target, sign, static_dimension, dynamic_dimension)
                    else:
                        # else, adjacent ->diagonal
                        self.move(offset)
                case (2, 1):  # Diagonal to adjacent
                    self.move(offset)

                case (2, 3):
                    # Only case where tail changes row and column
                    self.tail[static_dimension] = self.head[static_dimension]
                    self.tail[dynamic_dimension] = self.head[dynamic_dimension] - sign
                    # print(f"New tail: {self.tail}")
                    # One behind
                    self.touched[tuple(self.tail)] += 1
                    self.advance(target, sign, static_dimension, dynamic_dimension)
                case _:
                    raise ValueError("Unexpected value")

    def advance(self, target, sign, static_dimension, dynamic_dimension):

        # Mark every coord touched by tail
        temp = self.tail.copy()
        for i in range(self.head[dynamic_dimension], target[dynamic_dimension], sign):
            temp[dynamic_dimension] = i
            self.touched[tuple(temp)] += 1
        self.head[dynamic_dimension] = target[dynamic_dimension]
        # print(f"New head: {self.head}")
        # print(self.touched.keys())
        self.tail[dynamic_dimension] = (
            target[dynamic_dimension] - sign
        )  # one behind; should be marked in loop
        # print(f"New tail: {self.tail}")
        # print("\n")


class Rope:
    def __init__(self, knots):
        self.knots = [[0, 0] for _ in range(knots)]
        self.head = self.knots[0]
        self.touched = set([(0, 0)])
        self.n_knots = knots
        self.dimension = 2

    def move_knot(self, leading, trailing):
        new_distance = l1(leading, trailing)
        # if adjacent or diagonal, don't move
        #     breakpoint()
        if new_distance >= 2:
            diags = [
                [trailing[i] + corner[i] for i in range(self.dimension)]
                for corner in adjacents[:4]
            ]
            if new_distance > 2 or leading not in diags:
                # Find and move to closest of 8 adjacent spaces
                diags.extend(
                    [
                        [trailing[i] + corner[i] for i in range(self.dimension)]
                        for corner in adjacents[4:]
                    ]
                )
                new_location = min(diags, key=lambda coord: l1(coord, leading))
                trailing[0] = new_location[0]
                trailing[1] = new_location[1]

        # else, find closest adjacent space to next link and move to it

    def matrix(self):
        matrix = mask
        for i, coord in enumerate(self.knots):
            matrix[int(coord[0]) + 5, int(coord[1]) + 5] = i
        return matrix

    def move(self, offset):
        # breakpoint()
        target = [self.knots[0][0] + offset[0], self.knots[0][1] + offset[1]]
        dynamic_dimension = int(offset[1] != 0)
        sign = -1 if target[dynamic_dimension] < self.knots[0][dynamic_dimension] else 1
        # Repeat until head in position
        while self.knots[0] != target:
            # Adjust each knot by known logica
            self.knots[0][dynamic_dimension] += sign
            for i in range(1, self.n_knots):
                self.move_knot(self.knots[i - 1], self.knots[i])

            self.touched.add(tuple(self.knots[-1]))
            # Mark position 9


with open("inputs/day9.txt") as f:
    raw_input = f.read().splitlines()

processed = [parse(line) for line in raw_input]

first_state = State((0, 0), (0, 0))

for line in processed:
    first_state.move(list(line))

part1 = len(first_state.touched.keys())
print(part1)

rope = Rope(knots=10)
for line in processed:
    rope.move(list(line))

part2 = len(rope.touched)
print(part2)
