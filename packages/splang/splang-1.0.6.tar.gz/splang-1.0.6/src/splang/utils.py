import math
def get_last_second(duration_min):
    """
    Extract the last digit of the seconds part of a "mm:ss" string.
    e.g. "5:32" -> 2
    """
    try:
        return int(duration_min.split(':')[1][-1])
    except Exception:
        raise ValueError(f"Invalid duration_min '{duration_min}'")


def get_first_second(duration_min):
    """
    Extract the first digit of the seconds part of a "mm:ss" string.
    e.g. "5:32" -> 3
    """
    try:
        return int(duration_min.split(':')[1][0])
    except Exception:
        raise ValueError(f"Invalid duration_min '{duration_min}'")
    
def process_ms(duration_ms):
    totalSec = math.floor(duration_ms / 1000 + 0.5)
    minutes = totalSec // 60
    seconds = totalSec % 60
    first_seconds = seconds // 10
    last_seconds = seconds % 10
    return f"{minutes}:{first_seconds}{last_seconds}"

def get_first_ascii_character(string):
    for char in string:
        if char.isascii():
            return char
    return "¿"