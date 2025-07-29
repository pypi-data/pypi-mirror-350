from typing import List
from typing import Tuple


def exclude_dict_empty_values(dictionary: dict):
    """
    빈 문자열 또는 None 값을 가진 key를 dict에서 제거
    """
    return {k: v for k, v in dictionary.items() if v != "" and v is not None}


def split_elements_per_unit(values: list, unit: int, remove_none=True):
    """
    주어진 리스트를 unit 갯수에 맞게 잘라 리스트로 삽입
    ie. ['a','b','c','d'] 를 unit 3을 적용 -> [['a','b','c'], ['d', None, None, None]]
    remove 옵션 적용시 None 은 제거됨.
    """
    total_length = len(values)
    extended_list = (
        values + [None] * (unit - (total_length % unit))
        if total_length % unit != 0
        else values
    )
    if remove_none:
        return [
            list(filter(bool, extended_list[i : i + unit]))
            for i in range(0, len(extended_list), unit)
        ]
    return [extended_list[i : i + unit] for i in range(0, len(extended_list), unit)]


def dict_list_to_map(key, values: List[dict]):
    """
    dict list를 dict 요소의 주어진 키에 대한 값을 기준으로 dict map으로 전환
    :param key: dict 내부의 키
    :param values: 대상값
    :return: 변환된 dict
    """
    return {obj[key]: obj for obj in values}


def omit(dictionary: dict, keys: list):
    """
    dict 에서 특정한 키를 제외하고 반환
    :param dictionary: 대상
    :param keys: 제외할 key
    :return: dict
    """
    return {key: dictionary[key] for key in dictionary if key not in keys}


def pick(dictionary: dict, keys: list):
    """
    dict 에서 특정한 키만 선택하여 반환
    :param dictionary: 대상
    :param keys: 선택할 key
    :return: dict
    """
    return {key: dictionary[key] for key in dictionary if key in keys}


def chunk_list(input_list: list, chunk_size: int):
    """
    입력받은 목록을 원하는 최대 사이즈 내에서 조각내어 반환
    :param input_list: 입력 목록
    :param chunk_size: 최대 사이즈
    :return: generator
    """
    for i in range(0, len(input_list), chunk_size):
        yield input_list[i : i + chunk_size]


def get_value(obj, key: str, default=None, raise_exception=False):
    """
    Dict 타입 혹은 instance 를 받아 키에 해당하는 값을 반환
    :param obj: Dict or Any object
    :param key: 탐색할 키
    :param default: 기본값
    :param raise_exception: True 인 경우 키의 값이 없을 때 KeyError or AttributeError raise
    :return: value
    """
    if isinstance(obj, dict):
        return obj[key] if raise_exception else obj.get(key, default)
    return getattr(obj, key) if raise_exception else getattr(obj, key, default)


def extract_terminal_strings(data: dict):
    """
    Dict 타입의 값을 받아 재귀탐색하여 말단의 문자열들을 모아 List로 반환
    :param data: Dict
    :return: List[str]
    """
    terminal_strings = []

    def extract_strings_from_dict(d):
        for key, value in d.items():
            if isinstance(value, dict):
                extract_strings_from_dict(value)
            elif isinstance(value, str):
                terminal_strings.append(value)

    extract_strings_from_dict(data)
    return terminal_strings


def ordered_unique_tuple(values: Tuple) -> Tuple:
    """
    중복된 값을 제거하고 순서를 유지한 튜플을 반환
    """
    return tuple(dict.fromkeys(values))
