import re

# real = x
# imag = y

strides = {"R": 1, "U": -1j, "L": -1, "D": 1j}
directions = list(strides.keys())
n_directions = len(directions)

wraparounds = {
    1
    + 0j: lambda map, current: min(
        (k for k in map.keys() if k.imag == current.imag), key=lambda x: x.real
    ),
    -1
    + 0j: lambda map, current: max(
        (k for k in map.keys() if k.imag == current.imag), key=lambda x: x.real
    ),
    0
    - 1j: lambda map, current: max(
        (k for k in map.keys() if k.real == current.real), key=lambda x: x.imag
    ),
    # coords increase down
    0
    + 1j: lambda map, current: min(
        (k for k in map.keys() if k.real == current.real), key=lambda x: x.imag
    ),
}
scores = {1 + 0j: 0, -1 + 0j: 2, 0 + 1j: 1, 0 - 1j: 3}


def print_graph(graph):
    ymin = 1
    ymax = int(max(graph.keys(), key=lambda x: x.imag).imag)
    xmin = 1
    xmax = int(max(graph.keys(), key=lambda x: x.real).real)

    for i in range(ymin, ymax + 1):
        print(
            "".join(str(graph.get(complex(j, i), ".")) for j in range(xmin, xmax + 1))
        )


# Map transition for each stride for each face
# Start in lefmost top


def rotate(x, change):
    # current = directions.index(change)
    # print(current)
    # return directions[(current + 1 if directions == "L" else -1) % n_directions]
    if change == "L":  # counterclockwise
        x = complex(x.imag, -x.real)
    elif change == "R":
        x = complex(-x.imag, x.real)
    return x


def traverse(graph, instructions, start, initial):

    current = start
    stride = initial
    # breakpoint()
    for pair in instructions:
        # if current == 8 + 8j:
        #     breakpoint()
        steps = pair[0]
        # next = current + stride * steps

        # if next not in graph.keys() or next[graph] == 1:
        # next = current
        for _ in range(steps):
            new = current + stride
            if new not in graph.keys():
                new = wraparounds[stride](graph, current)  # Check wraparound
            if graph[new] == 1:  # Stop on hitting wall
                break
            current = new
        stride = rotate(stride, pair[1])
    return current, stride


# In eye-popping 3-D!
def traverse_3d(graph, instructions, start, initial):

    current = start
    stride = initial
    for pair in instructions:
        # if current == 8 + 8j:
        #     breakpoint()
        steps = pair[0]
        # next = current + stride * steps

        # if next not in graph.keys() or next[graph] == 1:
        # next = current
        for _ in range(steps):
            new = current + stride
            new_stride = stride
            if new not in graph.keys():
                current_side = faces[current]
                new, new_stride = transitions[(current_side, stride)](current)
            if graph[new] == 1:  # Stop on hitting wall
                break
            current = new
            stride = new_stride
        stride = rotate(stride, pair[1])
        # print(stride)
    return current, stride


def parse_instructions(instructions):
    divided = re.split(r"(?<=[LRDU])(?=\d+)", instructions)
    return [(int(pair.rstrip("LRDU")), pair.lstrip("0123456789")) for pair in divided]


def parse_map(lines):
    result = {}
    faces = {}
    side_length = min(len(line.lstrip(" ")) for line in lines)
    pattern = int(max(len(line.lstrip(" ")) for line in lines) == side_length * 3)
    sides_seen = set()
    translations = {".": 0, "#": 1}
    prev_chars = 0

    # both should be 1-indexed
    for j, line in enumerate(lines):
        length = len(line)
        line = line.lstrip(" ")
        reduced = len(line)
        offset = length - reduced
        line = line.rstrip(" ")

        if reduced != prev_chars:
            new_sides = tuple(
                (0 if not len(sides_seen) else max(sides_seen)) + i
                for i in range(1, (reduced // side_length) + 1)
            )
            sides_seen.update(new_sides)

        for i, char in enumerate(line):
            coord = complex(offset + i + 1, j + 1)
            result[coord] = translations[char]
            faces[coord] = new_sides[i // side_length]
        prev_chars = reduced
    return result, faces, pattern


def password(position, direction):
    return 1000 * position.imag + 4 * position.real + scores[direction]


with open("inputs/day22.txt") as f:
    map_lines, instructions = f.read().split("\n\n")
map_lines = map_lines.split("\n")
instructions = instructions.rstrip("\n")
instructions = parse_instructions(instructions)

# Fill trailing direction
# if instructions[-1][1] == "":
#     instructions[-1] = (instructions[-1][0], instructions[-2][1])

# Is it the example pattern or the real input
graph, faces, pattern = parse_map(map_lines)
start = min(graph.keys(), key=lambda coord: (coord.imag, coord.real))
end, direction = traverse(graph, instructions, start, 1)

ranges = {}
for side in set(faces.values()):
    coords = tuple(k for k, v in faces.items() if v == side)
    xmin = min(x.real for x in coords)
    xmax = max(x.real for x in coords)
    ymin = min(y.imag for y in coords)
    ymax = max(y.imag for y in coords)
    ranges[side] = {"xmin": xmin, "xmax": xmax, "ymin": ymin, "ymax": ymax}

# Forgive me
if pattern:
    transitions = {
        (1, -1): lambda coord: (
            complex(
                ranges[3]["xmin"] + (coord.imag - ranges[1]["ymin"]), ranges[3]["ymin"]
            ),
            -1j,
        ),
        (1, 1): lambda coord: (
            complex(
                ranges[6]["xmax"], ranges[6]["ymin"] + (ranges[1]["ymax"] - coord.real)
            ),
            -1,
        ),
        (1, -1j): lambda coord: (
            complex(
                ranges[2]["xmax"] - (coord.real - ranges[1]["xmin"]), ranges[2]["ymin"]
            ),
            1,
        ),
        (2, -1): lambda coord: (
            complex(
                ranges[6]["xmin"] + (coord.imag - ranges[2]["ymin"]), ranges[6]["ymax"]
            ),
            -1j,
        ),  # -> 6
        (2, 1j): lambda coord: (
            complex(
                ranges[5]["xmax"] - (coord.real - ranges[2]["xmin"]), ranges[5]["ymax"]
            ),
            -1j,
        ),  # ->5
        (2, -1j): lambda coord: (
            complex(
                ranges[1]["xmax"] - (coord.real - ranges[2]["xmin"]), ranges[1]["ymin"]
            ),
            1j,
        ),  # -> 1
        (3, 1j): lambda coord: (
            complex(
                ranges[5]["xmin"], ranges[5]["ymax"] - (coord.real - ranges[3]["xmin"])
            ),
            1,
        ),  # ->5
        (3, -1j): lambda coord: (
            complex(
                ranges[1]["xmin"], ranges[1]["ymin"] + (coord.real - ranges[3]["xmin"])
            ),
            1,
        ),  # -> 1
        (4, 1): lambda coord: (
            complex(
                ranges[6]["xmax"] - (coord.imag - ranges[4]["ymin"]), ranges[6]["ymin"]
            ),
            1j,
        ),
        (5, -1): lambda coord: (
            complex(
                ranges[3]["xmin"] - (coord.imag - ranges[5]["ymin"]), ranges[3]["ymin"]
            ),
            -1j,
        ),  # -> 3
        (5, 1j): lambda coord: (
            complex(
                ranges[2]["xmax"] - (coord.real - ranges[5]["xmin"]), ranges[2]["ymax"]
            ),
            -1j,
        ),  # -> 2
        (6, 1): lambda coord: (
            complex(
                ranges["xmax"][1], ranges[1]["ymax"] - (coord.imag - ranges[6]["ymin"])
            ),
            -1,
        ),  # -> 1
        (6, 1j): lambda coord: (
            complex(
                ranges[2]["xmin"], ranges[2]["ymax"] - (coord.imag - ranges[6]["ymin"])
            ),
            1,
        ),  # -> 2
        (6, -1j): lambda coord: (
            complex(
                ranges[4]["xmax"], ranges[4]["ymax"] - (coord.real - ranges[6]["xmin"])
            ),
            -1,
        ),  # -> 4
    }
else:
    transitions = {
        (1, -1): lambda coord: (
            complex(
                ranges[4]["xmin"], ranges[4]["ymax"] - (coord.imag - ranges[1]["ymin"])
            ),
            1,
        ),  # -> 4
        (1, -1j): lambda coord: (
            complex(
                ranges[6]["xmin"], ranges[6]["ymin"] + (coord.real - ranges[1]["xmin"])
            ),
            1,
        ),  # -> 6
        (2, 1): lambda coord: (
            complex(
                ranges[5]["xmax"], ranges[5]["ymax"] - (coord.imag - ranges[2]["ymin"])
            ),
            -1,
        ),  # -> 5
        (2, -1j): lambda coord: (
            complex(
                ranges[6]["xmin"] + (coord.real - ranges[2]["xmin"]), ranges[6]["ymax"]
            ),
            -1j,
        ),  # -> 6
        (2, 1j): lambda coord: (
            complex(
                ranges[3]["xmax"], ranges[3]["ymin"] + (coord.real - ranges[2]["xmin"])
            ),  # -> 3
            -1,
        ),
        (3, -1): lambda coord: (
            complex(
                ranges[4]["xmin"] + (coord.imag - ranges[3]["ymin"]), ranges[4]["ymin"]
            ),
            1j,
        ),  # ->4
        (3, 1): lambda coord: (
            complex(
                ranges[2]["xmin"] + (coord.imag - ranges[3]["ymin"]), ranges[2]["ymax"]
            ),  # -> 2
            -1j,
        ),
        (4, -1): lambda coord: (
            complex(
                ranges[1]["xmin"],
                ranges[1]["ymax"] - (coord.imag - ranges[4]["ymin"]),
            ),
            1,
        ),
        (4, -1j): lambda coord: (
            complex(
                ranges[3]["xmin"], ranges[3]["ymin"] + (coord.real - ranges[4]["xmin"])
            ),
            1,
        ),  # -> 3
        (5, 1): lambda coord: (
            complex(
                ranges[2]["xmax"], ranges[2]["ymax"] - (coord.imag - ranges[5]["ymin"])
            ),
            -1,
        ),  # -> 2
        (5, 1j): lambda coord: (
            complex(
                ranges[6]["xmax"], ranges[6]["ymin"] + (coord.real - ranges[5]["xmin"])
            ),
            -1,
        ),  # -> 6
        (6, -1): lambda coord: (
            complex(
                ranges[1]["xmin"] + (coord.imag - ranges[6]["ymin"]), ranges[1]["ymin"]
            ),
            1j,
        ),  # -> 1
        (6, 1): lambda coord: (
            complex(
                ranges[5]["xmin"] + (coord.imag - ranges[6]["ymin"]), ranges[5]["ymax"]
            ),
            -1j,
        ),  # -> 5
        (6, 1j): lambda coord: (
            complex(
                ranges[2]["xmin"] + (coord.real - ranges[6]["xmin"]), ranges[2]["ymin"]
            ),
            1j,
        ),  # -> 2
    }

part1 = int(password(end, direction))
print(part1)

end, direction = traverse_3d(graph, instructions, start, 1)
part2 = int(password(end, direction))
print(part2)
# If
