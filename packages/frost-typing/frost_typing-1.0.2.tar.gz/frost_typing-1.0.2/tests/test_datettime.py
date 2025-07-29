# -*- coding: utf-8 -*-
from typing import Union
from pytest import raises, mark
from datetime import date, time, datetime, timedelta, timezone
from frost_typing import parse_date, parse_datetime, parse_time


def _create_tz(hour=0, minutes=0) -> timezone:
    return timezone(timedelta(seconds=(hour * 60 + minutes) * 60))


@mark.parametrize(
    ("base", "res"),
    [
        ("2024-01-01", date(2024, 1, 1)),
        ("2024-1-01", date(2024, 1, 1)),
        ("2024-1-1", date(2024, 1, 1)),
        ("2024-W35-3", date(2024, 8, 28))
    ],
)
def test_positive_date(base: str, res: date) -> None:
    assert parse_date(base) == res
    assert parse_date(base.encode()) == res


@mark.parametrize(
    ("data",),
    [
        ("2024-1-1T",),
        ("2024-a-1 ",),
        ("2024-1-1 ",),
    ],
)
def test_negative_date(data: str) -> None:
    with raises(ValueError, match=f"Invalid isoformat string {data!r}"):
        parse_date(data)


@mark.parametrize(
    ("base", "res"),
    [
        ('11:30:59,123456', time(11, 30, 59, 123456)),
        ('113059,123456', time(11, 30, 59, 123456)),
        ('11:30:59.123456', time(11, 30, 59, 123456)),
        ('113059.123456', time(11, 30, 59, 123456)),
        ('11:30:59', time(11, 30, 59)),
        ('113059', time(11, 30, 59)),
        ('11:30', time(11, 30)),
        ('1130', time(11, 30)),
        ("9:1+3:0", time(9, 1, tzinfo=_create_tz(3))),
        ("9:1:2+3:0", time(9, 1, 2, tzinfo=_create_tz(3))),
        ("9:1:4.512+3:0", time(9, 1, 4, 512000, tzinfo=_create_tz(3))),
    ],
)
def test_positivetime(base: Union[str, bytes, bytearray], res: time) -> None:
    assert parse_time(base) == res


@mark.parametrize(
    ("base", "res"),
    [
        ("2018-04-29", datetime(2018, 4, 29, 0, 0)),
        ("2018-04", datetime(2018, 4, 1, 0, 0)),
        ("20180429", datetime(2018, 4, 29, 0, 0)),
        ("2009-W01-1", datetime(2008, 12, 29, 0, 0)),
        ("2009-W01", datetime(2008, 12, 29, 0, 0)),
        ("2009W011", datetime(2008, 12, 29, 0, 0)),
        ("2009W01", datetime(2008, 12, 29, 0, 0)),
        ("2024-W35-3", datetime(2024, 8, 28, 0, 0)),
        ("2024-1-01T10:00", datetime(2024, 1, 1, 10)),
        ("2024-1-1 10:00", datetime(2024, 1, 1, 10)),
        ("2024-W37T14:30:00", datetime(2024, 9, 9, 14, 30)),
        ("2024-1-01 10:00+03:00", datetime(2024, 1, 1, 10, tzinfo=_create_tz(3))),
        ("2024-1-01T10:00+02:35", datetime(2024, 1, 1, 10, tzinfo=_create_tz(2, 35)))
    ],
)
def test_datetime(base: str, res: datetime) -> None:
    assert parse_datetime(base) == res
