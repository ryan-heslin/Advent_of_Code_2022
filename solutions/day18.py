from collections import deque

from utils.utils import split_lines

raw_input = split_lines("inputs/day18.txt")

bases = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

# Process after pop from queue, not when doing neighbors
def check_range(vector, ranges):
    on_border = False
    for i in range(len(vector)):
        if vector[i] in ranges[i]:
            on_border = True
        elif not ranges[i][0] <= vector[i] <= ranges[i][1]:
            return False, False
    return True, on_border


def flood_fill(start, exclusions, trapped, exposed, ranges):
    Q = deque([start])
    visited = set()
    discovered = set()
    category = trapped
    dim = len(ranges)

    while Q:
        current = Q.popleft()
        in_bounds, on_border = check_range(current, ranges)
        if in_bounds:
            # if not (
            #     current in exposed
            #     or current in trapped
            #     or current in exclusions
            #     or current in visited
            # ):
            visited.add(current)
            if on_border:
                category = exposed
            for vector in bases:
                neighbor = tuple(current[j] + vector[j] for j in range(dim))
                # Since each index used twice
                if not (
                    neighbor in exposed
                    or neighbor in trapped
                    or neighbor in exclusions
                    or neighbor in visited
                ):
                    Q.appendleft(neighbor)

    # Update identified type with coordinates
    category.update(visited)


def neighbors(coord, dim=3):
    x, y, z = coord
    return {
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1),
    }


coords = {tuple(int(num) for num in line.split(",")) for line in raw_input}


trapped = set()
exposed = set()

columns = list(zip(*coords))
xmin, ymin, zmin = (min(col) for col in columns)
xmax, ymax, zmax = (max(col) for col in columns)

ranges = [
    (xmin, xmax),
    (ymin, ymax),
    (zmin, zmax),
]

for x in range(xmin, xmax + 1):
    for y in range(ymin, ymax + 1):
        for z in range(zmin, zmax + 1):
            coord = (x, y, z)
            # if coord == (2, 2, 5):
            #     breakpoint()
            if coord not in coords:
                if not (coord in trapped or coord in exposed):
                    flood_fill(coord, coords, trapped, exposed, ranges)


part1 = part2 = 0
dim = len(ranges)
for coord in coords:
    this_neighbors = neighbors(coord)
    part1 += 6 - len(coords.intersection(this_neighbors))
    part2 += len(exposed.intersection(this_neighbors)) + sum(
        sum(n[i] < ranges[i][0] or n[i] > ranges[i][1] for i in range(dim))
        for n in this_neighbors
    )

print(part1)
print(part2)
# Subtract 6* trapped cubes from total exposed faces
# Pick random air cube
# Flood-fill, limited to grid bounds
# If exterior found, mark exposed
# Add to exposed if any cube exposed, otherwise trapped
# Count faces touching exposed cubes
