# Written in 10 minutes flat, and looks like it too.
with open("inputs/day1.txt") as f:
    raw_input = f.read().splitlines()

most = -1
cur = 0
all = []

for line in raw_input:
    if line == "":
        most = max(cur, most)
        all.append(cur)
        cur = 0
    else:
        cur += int(line)
print(most)

print(sum(sorted(all, key=lambda x: -x)[:3]))
