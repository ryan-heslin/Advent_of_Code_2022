from collections import deque

from utils import split_lines

numbers = split_lines("inputs/day25.txt")

previous = sum = 0
powers = {}
translations = {"=": -2, "-": -1, "0": 0, "1": 1, "2": 2}

for num in numbers:
    for i, digit in enumerate(reversed(num)):
        power = powers.get(i, 5**i)
        powers[i] = power
        sum += translations[digit] * powers[i]

print(sum)

i = last_divisor = 1
result = deque([])
remaining = sum
digits = {0: "0", 1: "1", 2: "2", 3: "=", 4: "-"}

while remaining != 0:
    divisor = powers.get(i, 5**i)
    powers[i] = divisor
    leftover = remaining % divisor
    digit = leftover // last_divisor
    result.appendleft(digits[digit])

    if digit == 3 or digit == 4:
        remaining += leftover
    else:
        remaining -= leftover
    last_divisor = divisor
    i += 1

part1 = "".join(result)
print(part1)
