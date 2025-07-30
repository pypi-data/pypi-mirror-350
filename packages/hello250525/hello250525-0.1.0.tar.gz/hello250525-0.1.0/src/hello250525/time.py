import time


def get_current_time(d: int = 0) -> int:
    if d:
        return int(time.time())

    return time.time()


