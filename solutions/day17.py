from itertools import cycle
from math import ceil
from time import sleep

# Draw piece 3 spaces above highest
# Check spaces below
# If any full, stop, record piece height + bottom y-val as new floor
# Else reduce all y-coords 1
#  Start with floor spaces


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

raw_input = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
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
tortoise = 1
hare = 2
iter = 0

heights = {}
cycle_found = False
updates = []
while not cycle_found or iter < 2022:
    # start = max(x.imag for x in board.keys()) + 4
    # start = highest + 4
    piece = next(pieces)
    current_piece = piece.draw_with_offset(start)
    # Inclusive of topmost part of piece
    this_size = piece.size

    # Move until unable
    for move in instructions:
        # print(current_piece)
        # sleep(1)
        side_coords = [None] * this_size
        moved_side = False
        for i in range(this_size):
            this_coord = current_piece[i] + move
            if (not xmin <= this_coord.real <= xmax) or board.get(this_coord, False):
                break
            side_coords[i] = this_coord
            # Piece's sideways movement blocked, so ignore
        else:
            moved_side = True

        if moved_side:
            current_piece = side_coords.copy()

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
        current_piece = down_coords.copy()

    for coord in current_piece:
        # assert coord not in board.keys()
        start = max(start, coord.imag + 4)
        board[coord] = 1

    if not cycle_found:
        lowest = min(coord.imag for coord in current_piece)
        # Cache this piece configuration
        updates.append(
            tuple(complex(coord.real, coord.imag - lowest) for coord in current_piece)
        )
        heights[iter] = start - 4
        if len(set(updates)) < len(updates):
            cycle_ends = [i for i, el in enumerate(updates) if el == updates[-1]]
            # TODO actually detect cycle by checking for patterns that repeat the same block multiple times
            if (
                len(cycle_ends) > 2
                and heights[cycle_ends]
                and updates[
                    cycle_ends[0] : (cycle_ends[1] + 1)
                    == updates[cycle_ends[1] : (cycle_ends[2] + 1)]
                ]
            ):
                cycle_length = cycle_ends[1] - cycle_ends[0]
                cycle_height = heights[cycle_ends[1]] - heights[cycle_ends[0]]
                cycle_found = True
        # for i in range(iter // 2):
        #     first = updates[i]
        #     try:
        #         recurrence = updates[(i + 1) :].index(first)
        #         length = recurrence - first
        #         if (iter - recurrence) >= length and updates[
        #             first : (recurrence + 1)
        #         ] == updates[recurrence : (recurrence + length + 1)]:
        #             cycle_length = length
        #             cycle_height = heights[recurrence] - heights[i]
        #             cycle_found = True
        #
        #     except:
        #         pass
    if iter == 2021:
        part1 = int(max(x.imag for x in board.keys()))
    iter += 1
# Period of 53
# heights[iter] = start - 4  # Inclusive of top
# if iter % 2 == 0:
#     candidate = iter // 2
#     split_height = heights[candidate]
#     lower = set()
#     upper = set()
#
#     for coord in board.keys():
#         if 0 < coord.imag <= split_height:
#             lower.add(coord)
#         else:
#             upper.add(complex(coord.real, coord.imag - split_height))
#
#     if upper == lower:
#         cycle_found = True
#         period = candidate
#         cycle_height = heights[candidate]


# part1 = int(max(x.imag for x in board.keys()))
print(part1)

target = 1000000000
complete_cycles = target // period
leftover = target % period
part2 = cycle_height * complete_cycles + heights[leftover]
print(part2)
