from utils import split_lines


def sign(x):
    return 0 if x == 0 else x // abs(x)


def negative_floor_div(x, divisor):
    return sign(x) * abs(x) // divisor


def mix(numbers):
    index = total = 0
    length = len(numbers)
    handled = set()

    # insert after index
    print(numbers)
    while index < length:
        # print(numbers)
        # print(f"Current index {index}")
        # print("\n")
        if numbers[index].imag == 0:
            if numbers[index].real == 0:
                numbers[index] += 1j
            else:

                element = numbers.pop(index)
                # if element == -2:
                #     breakpoint()
                # element += 1j
                # Inserts rihgt of positive index, left of negative
                shift = index + element.real
                target = int(negative_modulus_my_way_and_youll_like_it(shift, length))
                # Account for elements right of initial index, shifted
                # left by pop at index
                target += (
                    target > 0 and (shift + index) > length and target <= index
                ) or (target < 0 and (length + target) <= index)
                # Wrap backward
                if target == 0:
                    numbers.append(element)
                    numbers[-1] += 1j
                else:
                    numbers.insert(target, element)
                    numbers[target - (target < 0)] += 1j
        else:
            index += 1
    return numbers


def negative_modulus_my_way_and_youll_like_it(x, modulus):
    return sign(x) * (abs(x) % modulus)


def decrypt(numbers):
    modulus = len(numbers)
    start = numbers.index(0)
    return sum(numbers[(start + x) % modulus].real for x in range(1000, 4000, 1000))


# raw_input = split_lines("inputs/day20.txt")
# numbers = [complex(int(num), 0) for num in raw_input]
numbers = [1, 2, -3, 3, -2, 0, 4]
original = set(numbers)

mixed = mix(numbers)
mixed = [x.real for x in mixed]
assert set(num.real for num in mixed) == original
part1 = int(decrypt(mixed))
print(part1)
