from collections import defaultdict
from math import inf
from queue import PriorityQueue

from utils.utils import split_lines

ascii_a = ord("a")
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
            # and self.container[coord].elevation <= self.elevation + 1,
            and self.container[coord].elevation >= self.elevation - 1,
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


def dijkstra(G, start):
    coords = G.keys()
    Q = PriorityQueue()
    dist = defaultdict(lambda: inf)
    dist[start] = 0
    Q.put((0, start), block=False)
    visited = set()

    while Q.qsize():
        current_dist, u = Q.get()

        alt = current_dist + 1
        for v in graph[u].neighbors():
            if v in coords:
                if alt < dist[v]:
                    dist[v] = alt
                if v not in visited:
                    Q.put((alt, v), block=False)
                    visited.add(v)

    return dist


start = goal = None
for i, line in enumerate(raw_input):
    for j, letter in enumerate(line):
        coord = (i, j)
        if letter == "S":
            start = coord
        elif letter == "E":
            goal = coord
        graph[coord] = Node(coord, elevation(letter), graph)

dist = dijkstra(graph, goal)

part1 = dist[start]
print(part1)


min_elevation = min(v.elevation for v in graph.values())
part2 = min(v for k, v in dist.items() if graph[k].elevation == min_elevation)
print(part2)
