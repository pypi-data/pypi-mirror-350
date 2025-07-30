from time import time


def _millis() -> float:
    """
    Returns the current time in milliseconds.
    """
    return round(time() * 1000)
