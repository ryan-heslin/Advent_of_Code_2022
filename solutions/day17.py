from itertools import cycle
from math import ceil
from operator import attrgetter

imag = attrgetter("imag")


def identical_states(x, y):
    return x["piece_i"] == y["piece_i"] and x["instruction_i"] == y["instruction_i"]


# Broken because only compares state at indices, not state of surrounding pieces
def find_cycle(states):
    for iteration, state in states.items():
        for second in range(iteration + 1, iterations - 2):
            if (
                (
                    iteration > 0
                    and identical_states(states[iteration - 1], states[second - 1])
                )
                and identical_states(state, states[second])
                and identical_states(states[iteration + 1], states[second + 1])
            ):
                period = second - iteration
                second_state = states[second]
                difference = states[second]["height"] - state["height"]
                third = second + period
                if third > iterations: 
                    break
                third_state = states[second + period]

                if (
                    states[third]["height"] - states[second]["height"]
                                            == difference and
                    (
                        iteration > 0
                        and identical_states(states[second - 1], states[third - 1])
                    )
                    and identical_states(second_state, third_state)
                    and identical_states(states[second + 1], states[third + 1])
                ):
                    return iteration, period
                for third in range(second + 1, iterations):
                    # Found a cycle
                    if (
                        identical_states(state, states[third])
                        and third - second == period
                        and states[third]["height"] - states[second]["height"]
                        == difference
                    ):
                        return iteration, period
    return None, None

def print_board(board, upper):
    for i in range(int(upper), -1, -1):
        print(
            str(i)
            + ": "
            + "".join((str(board.get(complex(j, i), ".")) for j in range(-3, 4)))
        )


class Piece:
    def __init__(self, coords) -> None:
        self.coords = coords
        self.height = (
            int(max(self.coords, key=imag).imag)
            - int(max(self.coords, key=imag).imag)
            + 1
        )
        self.size = len(coords)

    def draw_with_offset(self, offset):
        return [coord + complex(0, offset) for coord in self.coords]


def parse_piece(chars):
    result = []
    chars = chars.splitlines()
    for j, line in enumerate(chars):
        for i, char in enumerate(line):
            if char == "#":
                result.append(complex(i - 1, j))
    return tuple(result)


with open("inputs/day17.txt") as f:
    raw_input = f.read().rstrip("\n")
pieces = """####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##"""

# True x coord, y indexed relative to bottom
coords = list(map(parse_piece, pieces.split("\n\n")))
# Have to invert L for some reason
height = int(max(coords[2], key=imag).imag)
coords[2] = tuple(
    complex(x.real, 0 if x.imag == height else height if x.imag == 0 else x.imag)
    for x in coords[2]
)

pieces = cycle([Piece(coord) for coord in coords])

replacements = {
    "<": complex(-1, 0),
    ">": complex(1, 0),
}
instructions = cycle([replacements[char] for char in raw_input])
width = 7
xmax = width // 2
xmin = -xmax

board = dict(
    zip(
        (complex(i, 0) for i in range(0 - (width // 2), ceil(width / 2))),
        (1 for _ in range(width)),
    )
)
start = 4
iter = 0

cycle_found = False
states = {}
n_pieces = len(coords)
n_instructions = len(raw_input)
target_iterations = iterations = 2022
iterations = max(n_pieces * n_instructions, target_iterations)
piece_i = instruction_i = -1

while iter < iterations:
    piece = next(pieces)
    piece_i += 1
    piece_i %= n_pieces
    current_piece = piece.draw_with_offset(start)
    # Inclusive of topmost part of piece
    this_size = piece.size

    # Move until unable
    for move in instructions:
        side_coords = [None] * this_size
        moved_side = False
        instruction_i += 1
        instruction_i %= n_instructions

        for i in range(this_size):
            this_coord = current_piece[i] + move
            if (not xmin <= this_coord.real <= xmax) or board.get(this_coord, False):
                break
            side_coords[i] = this_coord
            # Piece's sideways movement blocked, so ignore
        else:
            moved_side = True

        if moved_side:
            current_piece = side_coords

        down_coords = [None] * this_size
        moved_down = False

        # Try to move down
        for i in range(this_size):
            this_coord = current_piece[i] - 1j
            if board.get(this_coord, False):
                break
            down_coords[i] = this_coord
        else:
            moved_down = True
            # Since we moved down

        if not moved_down:
            break
        current_piece = down_coords

    for coord in current_piece:
        start = max(start, coord.imag + 4)
        board[coord] = 1
    states[iter] = {
        "height": start - 4,
        "piece_i": piece_i,
        "instruction_i": instruction_i,
    }

    iter += 1


# Too lazy to look up Floyd's
part1 = int(states[target_iterations - 1]["height"])
print(part1)

# Period always 2781; detection is bugged
cycle_start, period = find_cycle(states)
assert cycle_start
cycle_height = states[cycle_start + period]["height"] - states[cycle_start]["height"]
bottom = states[cycle_start - 1]["height"]
elephant_demand = 1000000000000
target = elephant_demand - cycle_start

# Since cycle doesn't start on bottom
complete_cycles = target // period
leftover = target % period
leftover_height = (
    states[cycle_start + leftover]["height"] - states[cycle_start]["height"]
)
part2 = int(cycle_height * complete_cycles + leftover_height + bottom + 1)
print(part2)
