from collections import deque
from functools import cache
from itertools import repeat
from math import inf

from utils import l1
from utils import split_lines

ascii_a = 97
raw_input = split_lines("inputs/day12.txt")
graph = {}


class Node:
    def __init__(self, coord, elevation, container) -> None:
        self.coord = coord
        self.elevation = elevation
        self.container = container

    def neighbors(self):
        return filter(
            lambda coord: coord in self.container.keys()
            and self.container[coord].elevation <= self.elevation + 1,
            (
                (self.coord[0] + 1, self.coord[1]),
                (self.coord[0] - 1, self.coord[1]),
                (self.coord[0], self.coord[1] + 1),
                (self.coord[0], self.coord[1] - 1),
            ),
        )


def elevation(letter):
    letter = "z" if letter == "E" else "a" if letter == "S" else letter
    return ord(letter) - ascii_a


def dijkstra(G, start, goal):
    if list(graph[start].neighbors()) == []:
        return {}, {}
    coords = G.keys()
    size = len(coords)

    Q = deque(coords)
    dist = dict(zip(coords, repeat(inf, size)))
    prev = dict(zip(coords, repeat(None, size)))
    dist[start] = 0

    while Q:
        u = min(Q, key=lambda coord: dist[coord])
        if u == goal:
            break
        Q.remove(u)

        for v in graph[u].neighbors():
            if v in Q:
                alt = dist[u] + 1
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u

    return dist, prev


def reconstruct_path(u, previous):
    S = deque()
    if u in previous.keys():
        while u is not None:
            S.appendleft(u)
            u = previous[u]
    return S


start = goal = None
for i, line in enumerate(raw_input):
    for j, letter in enumerate(line):
        coord = (i, j)
        if letter == "S":
            start = coord
        elif letter == "E":
            goal = coord
        graph[coord] = Node(coord, elevation(letter), graph)

dist, prev = dijkstra(graph, start, goal)

path = reconstruct_path(goal, prev)
part1 = len(path) - 1
print(part1)

min_elevation = min(v.elevation for v in graph.values())
starts = set(
    sorted(
        [k for k, v in graph.items() if v.elevation == min_elevation],
        key=lambda v: l1(v, goal),
    )
)

# Something something programmer time more valuable than execution time
best = inf
while starts:
    current = starts.pop()
    dist, prev = dijkstra(graph, current, goal)
    if not (dist == {} or prev == {}):
        path = reconstruct_path(goal, prev)
        path.popleft()
        if path:
            this_best = length = len(path)

            # Subtract path length from any other valid start encountered on returned path
            for i, el in enumerate(path):
                if el in starts:
                    starts.remove(el)
                    this_best = length - i - 1

            best = min(best, this_best)
    else:
        path = filter(lambda node: node.elevation == 0, reconstruct_path(goal, prev))
        starts.difference_update(path)


print(best)
