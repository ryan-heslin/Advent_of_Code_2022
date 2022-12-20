import re

from utils import split_lines


def parse_line(line):
    pass


raw_input = split_lines("inputs/day19.txt")
resources = re.findall(r"[a-z]+(?=\srobot)", raw_input[0])
# Logic:
# If can build geode bot:
# Build geode bot
# else if can build obsidian bot
# build obsidian bot
# else if can build clay bot:
# build clay bot
# else
# pass
