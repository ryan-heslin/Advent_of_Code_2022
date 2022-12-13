# Mostly copied from https://en.wikipedia.org/wiki/Merge_sort
def merge_sort(m):
    length = len(m)
    if length <= 1:
        return m

    left = []
    right = []
    split = length // 2
    left = m[:split]
    right = m[split:]

    # // Recursively sort both sublists.
    left = merge_sort(left)
    right = merge_sort(right)

    # // Then merge the now-sorted sublists.
    return merge(left, right)


def merge(left, right):
    result = []
    while left and right:
        is_sorted = compare(left[0], right[0])
        if is_sorted or is_sorted is None:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))

    if left:
        result.extend(left)
    elif right:
        result.extend(right)
    return result


def decide(left, right):
    if left != right:
        return left < right
    else:
        return None


def compare(left, right):

    # if isinstance(left, int) or isinstance(right, int):
    #     breakpoint()
    if isinstance(left, int) and isinstance(right, int):
        return decide(left, right)
    elif isinstance(left, int):
        left = [left]
    elif isinstance(right, int):
        right = [right]

    for l, r in zip(left, right):

        result = compare(l, r)
        if result is not None:
            return result

    # Tiebreaker: shorter list
    return decide(len(left), len(right))


with open("inputs/day13.txt") as f:
    raw_input = f.read().rstrip("\n")

processed = raw_input.split("\n\n")
processed = [[eval(el) for el in pair.split("\n")] for pair in processed]

correct = [compare(pair[0], pair[1]) for pair in processed]
part1 = sum(i + 1 if res else 0 for i, res in enumerate(correct))
print(part1)

dividers = [[[2]], [[6]]]

singletons = list(zip(*processed))
singletons = list(singletons[0]) + list(singletons[1])
singletons.extend(dividers)

ordered = merge_sort(singletons)
indices = [ordered.index(x) + 1 for x in dividers]
part2 = indices[0] * indices[1]
print(part2)
