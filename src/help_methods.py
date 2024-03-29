import random


def get_random_int(minimum=0, maximum=9999999, step=1) -> int:
    return random.randrange(minimum, maximum, step)
