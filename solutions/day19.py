from collections import deque
from math import ceil
from math import inf

from utils import split_lines

# Can I do it without re?
def parse_line(line):
    ID, costs = line.split(": ")
    ID = int(ID.split(" ")[-1])
    costs = costs.split(". ")
    result = {}

    for sentence in costs:
        words = sentence.split(" ")
        # That this bot type gathers
        material = words[1]
        resources = words[4:]
        result[material] = {
            resources[i + 1].rstrip("."): int(resources[i])
            for i in range(0, len(resources), 3)
        }
    return ID, result


# Number of minutes to produce next bot of type, inclusive
def find_bot_time(state, costs):
    # Actual bot type not necessary
    greatest = -inf
    for resource in costs.keys():
        # Can never get enough of resource with no robots
        if state[resource][0] == 0:
            return inf
        difference = max(costs[resource] - state[resource][1], 0)
        greatest = max(ceil(difference / state[resource][0]), greatest)
    return greatest + 1


# Advance until bot construction time, or end of sequence
def update_to_time(state, time, bot_type, costs):
    result = {
        resource: (value[0], value[1] + (value[0] * time))
        for resource, value in state.items()
        if resource != "time"
    }
    result["time"] = state["time"] + time

    # Add new bot, subtract cost
    result[bot_type] = (result[bot_type][0] + 1, result[bot_type][1])
    for resource, qty in costs.items():
        result[resource] = (result[resource][0], result[resource][1] - qty)

    return result


def highest_cost(di):
    result = {}
    for subdict in di.values():
        for k, v in subdict.items():
            if k != "geode":
                result[k] = max(v, result.get(k, -inf))
    return result


def compute_geodes(costs, max_time):

    highest_costs = highest_cost(costs)
    start = {material: (0, 0) for material in costs.keys()}
    start["ore"] = (1, 1)
    start["time"] = 1
    # start["targets"] = ("geode", "obsidian", "clay", "ore")
    best = -inf
    Q = deque([start])

    # Each state represennts *end* of minute
    while Q:
        current = Q.popleft()
        # print(current)
        # print("\n")
        # Takes minute to build, another before it starts working
        time_left = max_time - current["time"]
        assert time_left >= 0
        # print(current)
        # Discard if no hope of beating best geodes
        if (
            current["geode"][1]
            + sum(range(current["geode"][0] + 1, current["geode"][0] + time_left + 1))
            <= best
        ):
            continue

        targets = ("geode",) + tuple(
            k for k in ("ore", "clay", "obsidian") if current[k][0] < highest_costs[k]
        )

        if time_left > 0:
            built = False
            for resource in targets:
                completion_time = find_bot_time(current, costs[resource])
                # print(completion_time)
                if completion_time <= time_left:
                    built = True
                    Q.appendleft(
                        update_to_time(
                            current,
                            completion_time,
                            bot_type=resource,
                            costs=costs[resource],
                        )
                    )
            if not built:
                # No time left to build bots
                best = max(
                    (current["geode"][1] + (time_left * current["geode"][0])), best
                )
        else:  # At max time
            assert current["time"] == max_time
            best = max(current["geode"][1], best)
    return best


raw_input = split_lines("inputs/day19.txt")
processed = dict(parse_line(line) for line in raw_input)

part1 = sum(id * compute_geodes(costs, 24) for id, costs in processed.items())
print(part1)

qualities = tuple(compute_geodes(processed[i], 32) for i in range(1, 4))
part2 = qualities[0] * qualities[1] * qualities[2]
print(part2)
