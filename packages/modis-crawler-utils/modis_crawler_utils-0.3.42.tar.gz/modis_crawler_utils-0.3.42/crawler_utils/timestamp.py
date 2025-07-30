import time


def ensure_seconds(timestamp):
    if timestamp > time.time() + 315360000:  # seconds in 10 years
        return timestamp / 1000
    else:
        return timestamp