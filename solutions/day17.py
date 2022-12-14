from itertools import cycle
from math import ceil


def find_cycle(states):
    for iteration, state in states.items():
        for second in range(iteration + 1, iterations):
            if (
                states[second]["piece_i"] == state["piece_i"]
                and states[second]["instruction_i"] == state["instruction_i"]
            ):
                period = second - iteration
                difference = states[second]["height"] - state["height"]
                for third in range(second + 1, iterations):
                    # Found a cycle
                    if (
                        states[third]["piece_i"] == state["piece_i"]
                        and states[third]["instruction_i"] == state["instruction_i"]
                        and third - second == period
                        and states[third]["height"] - states[second]["height"]
                        == difference
                    ):
                        return iteration, period


def print_board(board, upper):
    for i in range(int(upper), -1, -1):
        print("".join((str(board.get(complex(j, i), ".")) for j in range(-3, 4))))


class Piece:
    def __init__(self, coords) -> None:
        self.coords = coords
        self.height = (
            max(x.imag for x in self.coords) - min(x.imag for x in self.coords) + 1
        )
        self.size = len(coords)

    def draw_with_offset(self, offset):
        return [coord + complex(0, offset) for coord in self.coords]


with open("inputs/day17.txt") as f:
    raw_input = f.read().rstrip("\n")

# True x coord, y indexed relative to bottom
# Minus, plus, backward l, I, block
coords = [
    (complex(-1, 0), complex(0, 0), complex(1, 0), complex(2, 0)),
    (complex(0, 0), complex(-1, 1), complex(0, 1), complex(1, 1), complex(0, 2)),
    (complex(-1, 0), complex(0, 0), complex(1, 0), complex(1, 1), complex(1, 2)),
    (complex(-1, 0), complex(-1, 1), complex(-1, 2), complex(-1, 3)),
    (complex(-1, 0), complex(0, 0), complex(-1, 1), complex(0, 1)),
]
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
iterations = 2022
iter = 0

cycle_found = False
states = {}
n_pieces = len(coords)
n_instructions = len(raw_input)
target_iterations = 2022
iterations = max(n_pieces * n_instructions, target_iterations)
piece_i = instruction_i = -1

while iter < iterations:
    # start = max(x.imag for x in board.keys()) + 4
    # start = highest + 4
    piece = next(pieces)
    piece_i += 1
    piece_i %= n_pieces
    current_piece = piece.draw_with_offset(start)
    # Inclusive of topmost part of piece
    this_size = piece.size

    # Move until unable
    for move in instructions:
        # print(current_piece)
        # sleep(1)
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
        # assert coord not in board.keys()
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

cycle_start, period = find_cycle(states)
cycle_height = states[cycle_start + period]["height"] - states[cycle_start]["height"]
bottom = states[cycle_start - 1]["height"]
target = 1000000000000 - cycle_start

# Since cycle doesn't start on bottom
complete_cycles = target // period
leftover = target % period
leftover_height = (
    states[cycle_start + leftover]["height"] - states[cycle_start]["height"]
)
part2 = int(cycle_height * complete_cycles + leftover_height + bottom + 1)
print(part2)
