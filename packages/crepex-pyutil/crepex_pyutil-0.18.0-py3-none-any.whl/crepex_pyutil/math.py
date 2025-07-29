from typing import Union


def round_by_position(value: Union[int, float], position=-1):
    """
    자릿수 기준 반올림
    기본값은 10자리 단위 반올림
    ex. 22 -> 20, 255 -> 260, 254 -> 250
    """
    return int(round(float(value), position))
