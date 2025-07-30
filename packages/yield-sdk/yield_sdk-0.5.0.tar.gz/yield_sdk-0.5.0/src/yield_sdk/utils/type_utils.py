import datetime as dt
import re


def expect_boolean(data: object) -> bool:
    if not isinstance(data, bool):
        raise TypeError(f"Expected bool, got {type(data).__name__}")

    return data


def expect_integer(data: object) -> int:
    if not isinstance(data, int):
        raise TypeError(f"Expected int, got {type(data).__name__}")

    return data


def expect_string(data: object) -> str:
    if not isinstance(data, str):
        raise TypeError(f"Expected str, got {type(data).__name__}")

    return data


def expect_date(data: object) -> dt.date:
    s = expect_string(data)
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", s)
    if m is None:
        raise ValueError(f"Invalid date: {s}")

    return dt.date(int(m[1]), int(m[2]), int(m[3]))


def expect_time(data: object) -> dt.datetime:
    s = expect_string(data)

    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=dt.timezone.utc)


def expect_record(data: object) -> dict[str, object]:
    if not isinstance(data, dict):
        raise TypeError(f"Expected dict, got {type(data).__name__}")

    return data # type: ignore
