from collections import defaultdict
from collections import deque
from math import inf


def parse(line):
    pressure, neighbors = line.split("; ")
    parts = pressure.split(" ")
    flow = int(parts[-1].split("=")[-1])
    name = parts[1]
    split = "valve " if "valve " in neighbors else "valves "
    neighbors = set(neighbors.split(split)[-1].split(", "))
    return name, {"pressure": flow, "neighbors": neighbors}


with open("inputs/day16.txt") as f:
    raw_input = f.read().splitlines()
map = dict(parse(line) for line in raw_input)
start = "AA"

# Node: time, activated, unactivated, pressure


def floyd_warshall(map):
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
                if pairs[(j, k)] > (candidate := pairs[(j, i)] + pairs[(i, k)]):
                    pairs[(j, k)] = candidate
                if pairs[(k, j)] > (candidate := pairs[(i, j)] + pairs[(k, i)]):
                    pairs[(k, j)] = candidate
    return pairs


def explore(start, graph, pressures, start_time=30):

    current = {"node": start, "time": start_time, "pressure": 0, "done": set()}
    # Remove nodes already visited

    Q = deque([current])
    targets = pressures.keys()
    bests = defaultdict(lambda: -inf)

    while Q:
        v = Q.popleft()
        current_key = (tuple(v["done"]), v["node"], v["time"])
        if bests[current_key] >= v["pressure"]:
            continue
        bests[current_key] = v["pressure"]

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
        if (
            (v["node"] != start and v["node"] not in v["done"])
            or (graph[v["node"]] == {} and v["node"] in v["done"])
            or v["time"] == 0
        ):
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

    return bests


targets = {node for node, v in map.items() if v["pressure"] > 0}
pairs = floyd_warshall(map)
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
    cost = el[1]
    if source not in graph.keys():
        graph[source] = {el[0][1]: cost}
    else:
        graph[source][el[0][1]] = cost

pressures = {k: map[k]["pressure"] for k in targets}

# Only paths to pressure nodes
graph_reduced = {
    source: {
        dest: cost
        for dest, cost in edges.items()
        if cost < inf and dest in pressures.keys()
    }
    for source, edges in graph.items()
}

results = explore(start, graph_reduced, pressures)
part1 = max(results.values())
print(part1)

new_time = 26
starts = explore(start, graph_reduced, pressures, new_time)
part2 = -inf
starts = {k: starts[k] for k in sorted(starts.keys(), key=lambda x: -starts[x])}
greatest = max(starts.values())

for nodes, pressure in starts.items():
    # Skip if less even after adding best possible 26-minute pressure
    if pressure + greatest > part2:
        exclusions = set(nodes[0] + (nodes[1],))
        exclusions.discard(start)
        this_graph = {
            source: {
                dest: cost for dest, cost in edge.items() if dest not in exclusions
            }
            for source, edge in graph_reduced.items()
            if source == start or source not in exclusions
        }

        results = explore(start, this_graph, pressures, start_time=new_time)
        this_pressure = max(results.values())
        part2 = max(this_pressure + pressure, part2)

print(part2)
