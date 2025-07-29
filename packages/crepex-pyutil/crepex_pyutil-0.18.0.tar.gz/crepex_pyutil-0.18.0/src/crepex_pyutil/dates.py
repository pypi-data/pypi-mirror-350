from datetime import datetime, timedelta, timezone, tzinfo


def is_aware(value: datetime):
    """
    Determine if a given datetime.datetime is aware.

    The concept is defined in Python's docs:
    https://docs.python.org/library/datetime.html#datetime.tzinfo

    Assuming value.tzinfo is either None or a proper datetime.tzinfo,
    value.utcoffset() implements the appropriate logic.
    """
    return value.utcoffset() is not None


def make_aware(value: datetime, tz: tzinfo):
    if is_aware(value):
        raise ValueError("make_aware expects a naive datetime, got %s" % value)
        # This may be wrong around DST changes!
    return value.replace(tzinfo=tz)


def get_tzinfo(utc_offset=9):
    """
    timezone 정보 가져오기
    :param utc_offset: utc 기준시간. 기본값은 KST(+9)
    """
    return timezone(timedelta(hours=utc_offset))


def get_local_datetime(utc_offset=9):
    """
    Timezone이 지정된 datetime 현재시간
    :param utc_offset: utc 기준시간. 기본값은 KST(+9)
    """
    tz = get_tzinfo(utc_offset=utc_offset)
    return datetime.now().replace(tzinfo=tz)


def get_datetime_from_timestamp(second: str, aware=True, utc_offset=9):
    """
    String Type timestamp 를 형식에 맞는 Datetime 으로 변환\n
    :param second: Timestamp since the Epoch
    :param aware: Make aware 여부
    :param utc_offset: utc 기준시간. 기본값은 KST(+9)
    :return: Datetime
    """
    ts = float(second)

    if len(second) == 13:
        ts = ts / 1000

    dt = datetime.fromtimestamp(ts)

    if aware:
        tz = get_tzinfo(utc_offset=utc_offset)
        return make_aware(dt, tz)
    return dt


def get_datetime_from_iso_string(iso_string: str, aware=True, utc_offset=9):
    """
    ISO 형식의 문자열을 Datetime 으로 변환
    :param iso_string: ISO 형식의 문자열
    :param aware: Make aware 여부
    :param utc_offset: utc 기준시간. 기본값은 KST(+9)
    :return: Datetime 객체
    """
    dt = datetime.fromisoformat(iso_string)
    if aware and not dt.tzinfo:
        tz = get_tzinfo(utc_offset=utc_offset)
        return make_aware(dt, tz)
    return dt


def make_timestamp(dt: datetime, millisecond=True):
    """
    datetime 객체의 timestamp 변환
    :param dt: 대상
    :param millisecond: 밀리초 단위 변환 여부
    """
    timestamp = int(dt.timestamp())
    if millisecond:
        return timestamp * 1000
    return timestamp


def get_weekday_range(dt: datetime):
    """
    주어진 날짜의 주간 시작일과 종료일을 반환
    :param dt: 기준일
    :return: 시작일, 종료일 tuple
    """
    start = (dt - timedelta(days=dt.weekday())).replace(hour=0, minute=0, second=0)
    end = (start + timedelta(days=6)).replace(hour=23, minute=59, second=59)
    return start, end


def time_string_to_milliseconds(time_string):
    """
    "시:분:초" 형식의 문자열을 millisecond 단위의 정수로 변경하여 반환
    :param time_string: 시간 문자열
    :return: millisecond 정수
    """
    hours, minutes, seconds = time_string.split(":")
    total_milliseconds = (
        int(hours) * 3600000 + int(minutes) * 60000 + int(seconds) * 1000
    )
    return total_milliseconds
