from math import inf


def count_empty(board):
    xmin = ymin = inf
    xmax = ymax = -inf
    total = 0

    for k in board.keys():
        xmin = min(xmin, k.real)
        xmax = max(xmin, k.real)
        ymin = min(ymin, k.imag)
        ymax = max(xmin, k.imag)
        total += 1

    return ((xmax - xmin) * (ymax - ymin)) - total
