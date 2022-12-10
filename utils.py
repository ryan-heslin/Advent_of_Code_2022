def create_processor(func):
    def result(path):
        with open(path) as f:
            return func(f)

    return result


split_lines = create_processor(lambda f: f.read().splitlines())
