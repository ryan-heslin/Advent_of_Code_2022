from collections import defaultdict

from utils.utils import split_lines


def mix(numbers):
    index = 0
    length = len(numbers)
    modulus = length - 1

    while index < length:
        if numbers[index].imag == 0:

            element = numbers.pop(index)
            element += 1j
            # Inserts right of positive index, left of negative
            shift = index + element.real

            target = int(shift % modulus)
            if target == 0 and element.real < 0:
                numbers.append(element)
            else:
                numbers.insert(target, element)
        else:
            index += 1
    assert all(x.imag == 1 for x in numbers)
    return numbers


def mix_ordered(numbers, order):
    length = len(numbers)
    modulus = length - 1

    for num in order:

        index = numbers.index(num)
        element = numbers.pop(index)
        # Inserts right of positive index, left of negative
        shift = index + element.real

        target = int(shift % modulus)
        # Insert left of 0 same as append
        if target == 0 and element.real < 0:
            numbers.append(element)
        else:
            numbers.insert(target, element)
    return numbers


def decrypt(numbers):
    modulus = len(numbers)
    start = numbers.index(0)
    return sum(numbers[(start + x) % modulus].real for x in range(1000, 4000, 1000))


raw_input = split_lines("inputs/day20.txt")
numbers = [complex(int(num), 0) for num in raw_input]

mixed = [int(x.real) for x in mix(numbers.copy())]
part1 = int(decrypt(mixed))
print(part1)


key = 811589153
new_numbers = [(x * key) + 0j for x in numbers]
counts = defaultdict(lambda: 0)
initial = [None] * len(numbers)
for i, num in enumerate(new_numbers):
    counts[num] += 1
    initial[i] = complex(num, counts[num])

new_numbers = initial.copy()
order = initial.copy()
for _ in range(10):
    new_numbers = mix_ordered(new_numbers, order)

result = [int(x.real) for x in new_numbers]
part2 = int(decrypt(result))
print(part2)
