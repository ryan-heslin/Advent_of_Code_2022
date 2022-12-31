def create_processor(func):
    def result(path):
        with open(path) as f:
            return func(f)

    return result


def l1(x, y):
    return sum(abs(xi - yi) for xi, yi in zip(x, y))


split_lines = create_processor(lambda f: f.read().splitlines())
