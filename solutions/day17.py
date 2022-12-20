from itertools import cycle
from math import ceil
from time import sleep

# Draw piece 3 spaces above highest
# Check spaces below
# If any full, stop, record piece height + bottom y-val as new floor
# Else reduce all y-coords 1
#  Start with floor spaces


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

# raw_input = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
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
highest = 0
iterations = 2022

for _, piece in zip(range(iterations), pieces):
    # breakpoint()
    # TODO do this more efficiently
    # TODO cycle detection for part 2
    start = max(x.imag for x in board.keys()) + 4
    # start = highest + 4
    # if _ > 1 and current_piece[0] == -3 + 4j:
    #     breakpoint()
    current_piece = piece.draw_with_offset(start)
    # Inclusive of topmost part of piece
    highest = start + piece.height - 1
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
        highest -= 1
        current_piece = down_coords.copy()

    for coord in current_piece:
        # assert coord not in board.keys()
        board[coord] = 1 + board.get(coord, 0)

part1 = int(max(x.imag for x in board.keys()))
print(part1)


# for i in range(int(part1), -1, -1):
#     print("".join((str(board.get(complex(j, i), ".")) for j in range(-3, 4))))
