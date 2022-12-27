from utils import split_lines


def sign(x):
    return 0 if x == 0 else x // abs(x)


def negative_floor_div(x, divisor):
    return sign(x) * abs(x) // divisor


def mix(numbers):
    index = 0
    length = len(numbers)

    # insert after index
    # print(numbers)
    # breakpoint()
    while index < length:
        # print(numbers)
        # print(f"Current index {index}")
        # print("\n")
        if numbers[index].imag == 0:
            if numbers[index].real == 0:
                numbers[index] += 1j
            else:

                element = numbers[index]
                # if element == -2:
                #     breakpoint()
                element += 1j
                # Inserts right of positive index, left of negative
                shift = index + element.real

                target = int(shift % length)
                # If going right, offset since insertion is left
                target += element.real > 0
                # Account for elements right of initial index, shifted
                # left by pop at index
                # Insert left of 0 same as append
                if element.real < 0 and target == 0:
                    numbers.append(element)
                    numbers.pop(index)
                else:
                    numbers.insert(target, element)
                    # This is not bugged
                    numbers.pop(index + (target <= index))
        else:
            index += 1
        # print(numbers)
        # print("\n")
        # if index == 611:
        #     breakpoint()
        print(index)
    assert all(x.imag == 1 for x in numbers)
    return numbers


def negative_modulus_my_way_and_youll_like_it(x, modulus):
    return sign(x) * (abs(x) % modulus)


def decrypt(numbers):
    modulus = len(numbers)
    start = numbers.index(0)
    print([numbers[(start + x) % modulus].real for x in range(1000, 4000, 1000)])
    return sum(numbers[(start + x) % modulus].real for x in range(1000, 4000, 1000))


raw_input = split_lines("inputs/day20.txt")
numbers = [complex(int(num), 0) for num in raw_input]
# numbers = [1, 2, -3, 3, -2, 0, 4]
original = set(numbers)

mixed = mix(numbers)
mixed = [int(x.real) for x in mixed]
assert set(num.real for num in mixed) == original
part1 = int(decrypt(mixed))
print(part1)
