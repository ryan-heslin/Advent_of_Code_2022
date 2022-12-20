from collections import defaultdict
from collections import deque
from itertools import permutations
from math import inf

from utils import split_lines


def parse(line):
    pressure, neighbors = line.split("; ")
    parts = pressure.split(" ")
    flow = int(parts[-1].split("=")[-1])
    name = parts[1]
    split = "valve " if "valve " in neighbors else "valves "
    neighbors = set(neighbors.split(split)[-1].split(", "))
    return name, {"pressure": flow, "neighbors": neighbors}


raw_input = split_lines("inputs/day16.txt")
map = dict(parse(line) for line in raw_input)
start = "AA"

# Node: time, activated, unactivated, pressure


def find_neighbors(state):
    result = []
    if state["time"] == 0 or not state["unactivated"]:
        return result
    time = state["time"] - 1
    current = state["node"]
    # Activate current node
    if (
        state["node"] not in state["unactivated"]
        and map[state["node"]]["pressure"] != 0
    ):
        result.append(
            {
                "node": current,
                "time": time,
                "pressure": state["pressure"] + map[current]["pressure"] * (time - 1),
                "unactivated": state["unactivated"] - {current},
            }
        )
    # Move to other node
    result += [
        {
            "node": neighbor,
            "time": time,
            "pressure": state["pressure"],
            "unactivated": state["unactivated"].copy(),
        }
        for neighbor in map[current]["neighbors"]
    ]
    return result


def floyd_johnson(map):
    pairs = defaultdict(lambda: inf)
    # Direct connections
    for node in map.keys():
        pairs[(node, node)] = 0
        for neighbor in map[node]["neighbors"]:
            pairs[(node, neighbor)] = 1

    all = map.keys()
    for i in all:
        for j in all:
            for k in all:
                if pairs[(i, j)] > pairs[(i, k)] + pairs[(k, j)]:
                    pairs[(i, j)] = pairs[(i, k)] + pairs[(k, j)]
    return pairs


def explore(start, graph, pressures):

    current = {"node": start, "time": 30, "pressure": 0, "done": set()}
    visited = set()
    best_pressure = -inf
    Q = deque([current])
    targets = pressures.keys()

    while Q:
        v = Q.popleft()
        hash = ",".join(
            (v["node"], str(v["time"]), str(v["pressure"]), str(sorted(v["done"])))
        )

        if hash in visited:
            continue
        visited.add(hash)

        # Activate valve
        if v["node"] in targets and v["node"] not in v["done"] and v["time"] > 0:
            Q.appendleft(
                {
                    "node": v["node"],
                    "time": v["time"] - 1,
                    "pressure": v["pressure"] + pressures[v["node"]] * (v["time"] - 1),
                    "done": v["done"] | {v["node"]},
                }
            )
        if v["done"] == targets or graph[v["node"]] == {} or v["time"] == 0:
            best_pressure = max(v["pressure"], best_pressure)
            continue

        neighbors = graph[v["node"]]
        for neighbor, cost in neighbors.items():
            new_time = v["time"] - cost

            # Else, invalid state
            if new_time >= 0:
                Q.appendleft(
                    {
                        "node": neighbor,
                        "time": new_time,
                        "pressure": v["pressure"],
                        "done": v["done"].copy(),
                    }
                )

    return best_pressure


# def brute_force(start, graph):
#     best_pressure = -inf
#     targets = (k for k in graph.keys() if k != start)
#     possibilities = permutations(targets)
#
#     # breakpoint()
#     greatest = max(pressures.values())
#     i = 0
#     dead_ends = {k for k, v in graph.items() if v == {}}
#     max_end = len(tuple(targets)) - len(dead_ends)
#
#     # starts = ((k, v) for k, v in pairs.items() if k[0] == start)
#
#     for perm in possibilities:
#         # invalid = False
#         # for node in dead_ends:
#         #     if perm.index(node) != tail:
#         #         invalid = True
#         # if invalid:
#         #     break
#         for node
#         prev = perm[0]
#         # if sum(graph[start][prev] l + )
#         if prev not in graph[start].keys():
#             continue
#         time = 30 - graph[start][prev] - 1
#         this_pressure = pressures[prev] * time
#
#         for node in perm[1:]:
#             if graph[prev] == {}:
#                 break
#             time -= graph[prev][node] + 1
#             if time <= 0 or this_pressure + time * greatest <= best_pressure:
#                 break
#             this_pressure += pressures[node] * time
#             prev = node
#         else:
#             best_pressure = max(this_pressure, best_pressure)
#     return best_pressure
#
#
# def dijkstra(start):
#
#

#
#     dist = defaultdict(lambda: -inf)
#     prev = {}
#     prev[start] = None
#     dist[start] = 0
#     Q = deque(start)
#
#     while Q:
#         # print(len(Q))
#         u = max(Q, key=lambda state: state["pressure"])
#         Q.remove(u)
#         new_neighbors = find_neighbors(u)
#         for neighbor in new_neighbors:
#             this_hash = hash(neighbor.values())
#             dist[this_hash] = max(dist[this_hash], neighbor["pressure"])
#             if neighbor["time"] != 0 and neighbor["unactivated"]:
#                 Q.appendleft(neighbor)
#     return max(dist.values())
#     # alt = dist[this_hash] + neighbor["pressure"]
#     # if alt > dist:
#     #     dist[this_hash] = alt
#     #
#
#
# part1 = dijkstra(start)
# print(part1)


targets = {node for node, v in map.items() if v["pressure"] > 0}
# targets.add(start)
pairs = floyd_johnson(map)
pairs = {
    source: dest
    for source, dest in pairs.items()
    if (source[0] == start and source[1] != start)
    or (source[0] in targets and source[1] in targets)
    and source[0] != source[1]
}

graph = {}
for el in pairs.items():

    source = el[0][0]
    if source not in graph.keys():
        graph[source] = {el[0][1]: el[1]}
    else:
        graph[source][el[0][1]] = el[1]

pressures = {k: map[k]["pressure"] for k in targets}
graph_reduced = {
    source: {
        dest: cost
        for dest, cost in edges.items()
        if cost < inf and dest in pressures.keys()
    }
    for source, edges in graph.items()
}

part1 = explore(start, graph_reduced, pressures)
print(part1)
# TODO: Discord hint: " such that it is a Dijkstra where instead of hashing all that you hash into a set of visited nodes, you instead use a dict which simply maps the current valve and set of opened valves to the current highest pressure and only rerun a node if the cached highest pressure is lower than the current highest pressure and that this could be further reduced if you remove nodes with 0 flow rate and build up a weighted graph Not sure about implementation bugs atm"
