import datetime
import re
import sys
from collections.abc import Sequence

from iker.common.utils.funcutils import memorized, singleton

__all__ = [
    "basic_date_format",
    "basic_time_format",
    "basic_format",
    "extended_date_format",
    "extended_time_format",
    "extended_format",
    "iso_date_format",
    "iso_time_format",
    "iso_format",
    "iso_formats",
    "dt_utc_min",
    "dt_utc_max",
    "dt_utc_epoch",
    "dt_utc_infinity",
    "dt_utc_now",
    "dt_utc",
    "dt_to_ts",
    "dt_to_ts_us",
    "dt_from_ts",
    "dt_from_ts_us",
    "dt_parse",
    "dt_format",
    "dt_parse_iso",
    "dt_format_iso",
]


@singleton
def basic_date_format() -> str:
    return "%Y%m%d"


@memorized
def basic_time_format(with_ms: bool = False, with_tz: bool = False) -> str:
    fmt_str = "T%H%M%S"
    if with_ms:
        fmt_str = fmt_str + ".%f"
    if with_tz:
        fmt_str = fmt_str + "%z"
    return fmt_str


@memorized
def basic_format(with_ms: bool = False, with_tz: bool = False) -> str:
    return basic_date_format() + basic_time_format(with_ms, with_tz)


@singleton
def extended_date_format() -> str:
    return "%Y-%m-%d"


@memorized
def extended_time_format(with_ms: bool = False, with_tz: bool = False) -> str:
    fmt_str = "T%H:%M:%S"
    if with_ms:
        fmt_str = fmt_str + ".%f"
    if with_tz:
        fmt_str = fmt_str + "%:z"
    return fmt_str


@memorized
def extended_format(with_ms: bool = False, with_tz: bool = False) -> str:
    return extended_date_format() + extended_time_format(with_ms, with_tz)


iso_date_format = extended_date_format
iso_time_format = extended_time_format
iso_format = extended_format


@singleton
def iso_formats() -> list[str]:
    return [
        extended_format(True, False),
        extended_format(False, True),
        extended_format(True, True),
        extended_format(False, False),
        extended_date_format(),
        extended_time_format(True, False),
        extended_time_format(False, True),
        extended_time_format(True, True),
        extended_time_format(False, False),
        basic_format(True, False),
        basic_format(False, True),
        basic_format(True, True),
        basic_format(False, False),
        basic_date_format(),
        basic_time_format(True, False),
        basic_time_format(False, True),
        basic_time_format(True, True),
        basic_time_format(False, False),
    ]


@singleton
def dt_utc_min() -> datetime.datetime:
    return datetime.datetime.min.replace(tzinfo=datetime.timezone.utc)


@singleton
def dt_utc_max() -> datetime.datetime:
    return datetime.datetime.max.replace(tzinfo=datetime.timezone.utc)


@singleton
def dt_utc_epoch() -> datetime.datetime:
    return datetime.datetime(1970, 1, 1, 0, 0, 0, 0, tzinfo=datetime.timezone.utc)


dt_utc_infinity = dt_utc_max


def dt_utc_now() -> datetime.datetime:
    """
    Returns instance of current date time in UTC

    :return: current date time in UTC
    """
    return datetime.datetime.now(tz=datetime.timezone.utc)


def dt_utc(
    year: int,
    month: int = None,
    day: int = None,
    hour: int = 0,
    minute: int = 0,
    second: int = 0,
    microsecond: int = 0
) -> datetime.datetime:
    """
    Returns instance of the specified date time in UTC

    :param year: year part
    :param month: month part
    :param day: day part
    :param hour: hour part
    :param minute: minute part
    :param second: second part
    :param microsecond: microsecond part

    :return: specified date time in UTC
    """
    return datetime.datetime(year, month, day, hour, minute, second, microsecond, tzinfo=datetime.timezone.utc)


def dt_to_td(dt: datetime.datetime) -> datetime.timedelta:
    """
    Returns corresponding timedelta of the given datetime

    :param dt: the given datetime

    :return: timedelta from POSIX epoch
    """
    return dt.replace(tzinfo=datetime.timezone.utc) - dt_utc_epoch()


def dt_to_ts(dt: datetime.datetime) -> float:
    """
    Returns corresponding timestamp in seconds of the given datetime

    :param dt: the given datetime

    :return: timestamp in seconds from POSIX epoch
    """
    return dt_to_ts_us(dt) / 1.0e6


def dt_to_ts_us(dt: datetime.datetime) -> int:
    """
    Returns corresponding timestamp in microseconds of the given datetime

    :param dt: the given datetime

    :return: timestamp in microseconds from POSIX epoch
    """
    td = dt_to_td(dt)
    return (td.days * 86400 + td.seconds) * 1000000 + td.microseconds


def dt_from_td(td: datetime.timedelta) -> datetime.datetime:
    """
    Returns corresponding datetime in UTC of the given timedelta

    :param td: timedelta from POSIX epoch

    :return: the given datetime in UTC
    """
    return dt_utc_epoch() + td


def dt_from_ts(ts: float) -> datetime.datetime:
    """
    Returns corresponding datetime in UTC of the given timestamp in seconds

    :param ts: timestamp in seconds from POSIX epoch

    :return: the given datetime in UTC
    """
    return dt_from_ts_us(round(ts * 1.0e6))


def dt_from_ts_us(ts: int) -> datetime.datetime:
    """
    Returns corresponding datetime in UTC of the given timestamp in microseconds

    :param ts: timestamp in microseconds from POSIX epoch

    :return: the given datetime in UTC
    """
    return dt_from_td(datetime.timedelta(microseconds=ts))


basic_date_regex: re.Pattern[str] = re.compile(r"(\d{4})(\d{2})(\d{2})")
extended_date_regex: re.Pattern[str] = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
basic_time_regex: re.Pattern[str] = re.compile(r"T(\d{2})(\d{2})(\d{2})(\.\d{1,6})?")
extended_time_regex: re.Pattern[str] = re.compile(r"T(\d{2}):(\d{2}):(\d{2})(\.\d{1,6})?")
basic_tz_regexp: re.Pattern[str] = re.compile(r"([+-])(\d{2})(\d{2})")
extended_tz_regexp: re.Pattern[str] = re.compile(r"([+-])(\d{2}):(\d{2})")


def dt_parse(dt_str: str, fmt_str: str | Sequence[str]) -> datetime.datetime | None:
    """
    Null safely parses given string value of a datetime to the datetime instance

    :param dt_str: string value of the given datetime
    :param fmt_str: format string, or a list/tuple of format string candidates

    :return: datetime instance
    """
    if dt_str is None:
        return None

    if isinstance(fmt_str, str):
        for tz_directive in ["%z", "%:z"]:
            if tz_directive in fmt_str:
                if tz_directive == "%:z":
                    # Replaces ISO 8601 timezone format "%:z" (e.g., "+01:00") with "%z" (e.g., "+0100")
                    # because `datetime.strptime` does not support "%:z".
                    dt_str = extended_tz_regexp.sub(r"\1\2\3", dt_str)
                    fmt_str = fmt_str.replace("%:z", "%z")
                return datetime.datetime.strptime(dt_str, fmt_str)
        return datetime.datetime.strptime(dt_str, fmt_str).replace(tzinfo=datetime.timezone.utc)
    elif isinstance(fmt_str, Sequence):
        for s in fmt_str:
            try:
                return dt_parse(dt_str, s)
            except ValueError:
                pass
        raise ValueError(f"time data '{dt_str}' does not match the given formats")
    else:
        raise ValueError("malformed format")


def dt_format(dt: datetime.datetime, fmt_str: str) -> str | None:
    """
    Null safely formats the given datetime to a string value

    :param dt: the given datetime
    :param fmt_str: format string

    :return: string value of the given datetime
    """
    if dt is None or fmt_str is None:
        return None

    if dt.year < 1000 and "%Y" in fmt_str:
        year_str = str(dt.year).zfill(4)
        fmt_str = fmt_str.replace("%Y", year_str)

    if dt.year < 10 and "%y" in fmt_str:
        year_str = str(dt.year).zfill(2)
        fmt_str = fmt_str.replace("%y", year_str)

    # Manually handles the "%:z" timezone directive, since `datetime.strftime`
    # does not support it before Python 3.12
    if sys.version_info < (3, 12):
        if "%:z" in fmt_str:
            tz_str = basic_tz_regexp.sub(r"\1\2:\3", dt.strftime("%z"))
            fmt_str = fmt_str.replace("%:z", tz_str)

    return dt.strftime(fmt_str)


def dt_parse_iso(dt_str: str) -> datetime.datetime | None:
    return dt_parse(dt_str, iso_formats())


def dt_format_iso(dt: datetime.datetime) -> str | None:
    return dt_format(dt, iso_format())
