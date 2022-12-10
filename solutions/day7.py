from collections import deque
from math import inf


class Directory:
    def __init__(self, name):
        self.name = name
        self.directories = {}
        self.files = {}

    def add_directory(self, directory):
        if directory in self.directories.keys():
            return
        self.directories[directory] = Directory(name=directory)

    def add_file(self, file, size):
        self.files[file] = size

    def size(self):
        total = sum(self.files.values())
        return total + sum(dir.size() for dir in self.directories.values())

    def __repr__(self):
        return f"""
    {self.name}
    {list(self.directories.keys())}
    {self.files}"""


def parse(lines):
    root = lines[0].split(" ")[-1]
    tree = current = Directory(name=root)
    dirs = deque([tree])

    for line in lines[1:]:
        parts = line.lstrip("$ ").split(" ")
        if parts[0] == "cd":
            if parts[1] == "..":  # Go up one directory
                dirs.pop()
                current = dirs[-1]
            else:
                current = current.directories[parts[1]]
                dirs.append(current)
        elif parts[0] == "dir":
            current.add_directory(directory=parts[1])
        elif parts[0].isnumeric():  # File size
            current.add_file(file=parts[1], size=int(parts[0]))
        # If ls, pass
    return tree


def solve_parts(tree, max_size, to_free):
    total = 0
    candidates = deque([tree])
    best_size = inf

    while candidates:
        current = candidates.pop()
        size = current.size()

        if size <= max_size:
            total += size
        candidates.extend(current.directories.values())
        if size > to_free:
            best_size = min(best_size, size)
    return total, best_size


# cd /; ls -R -g --size --block-size=K  | grep ^total | sed s/[a-zA-Z ]+//g | sed -E 's/^[1-9][0-9]{5,}/0/' | paste -sd+ | bc
with open("inputs/day7.txt") as f:
    raw_input = f.read().splitlines()

tree = parse(raw_input)
total_size = tree.size()
total_space = 70000000
target_free = 30000000
actual_free = total_space - total_size
to_free = target_free - actual_free

part1, part2 = solve_parts(tree, 100000, to_free=to_free)
print(part1)
print(part2)
