from collections import defaultdict
from time import sleep

directions = {
    "R": lambda x: (x, 0),
    "D": lambda x: (0, -x),
    "L": lambda x: (-x, 0),
    "U": lambda x: (0, x),
}
# Tuple with index replaced with value
def update_tuple(tupe, i, value):
    return (x if j != i else value for j, x in enumerate(tupe))


def l1(x, y):
    return sum(abs(xi - yi) for xi, yi in zip(x, y))


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

        # breakpoint()
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

            if new_distance == 1:
                if (
                    self.head[static_dimension] == self.tail[static_dimension]
                ):  # Being dragged behind
                    self.advance(target, sign, static_dimension, dynamic_dimension)
                else:
                    # else, now adjacent, but not behind relative to direction of motion
                    self.move(offset)

            elif new_distance == 0 or (
                new_distance == 2 and orig_distance == 1
            ):  # diagonal -> beside or beside -> overlap, so no tail movement
                self.move(offset)
            elif new_distance == 3:  # diagonal -> knight's move offset
                # Only case where tail changes row and column
                self.tail[static_dimension] = self.head[static_dimension]
                self.tail[dynamic_dimension] = self.head[dynamic_dimension] - sign
                # print(f"New tail: {self.tail}")
                # One behind
                self.touched[tuple(self.tail)] += 1
                self.advance(target, sign, static_dimension, dynamic_dimension)
        # sleep(1)

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


with open("inputs/day9.txt") as f:
    raw_input = f.read().splitlines()

processed = [parse(line) for line in raw_input]

first_state = State((0, 0), (0, 0))

for line in processed:
    first_state.move(list(line))

part1 = len(first_state.touched.keys())
# print("\n")
print(part1)
# 6405 too low
