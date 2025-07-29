# -*- coding: utf-8 -*-
import pytest
import datetime
import frost_typing as ft
from uuid import UUID
from enum import Enum
from math import isnan
from typing import Any, Annotated


DATA = [
    ("", b'""'),
    ("\n\r\t", b'"\\n\\r\\t"'),
    (1, b"1"),
    (-1, b"-1"),
    (None, b"null"),
    (float("Infinity"), b"Infinity"),
    (float("-Infinity"), b"-Infinity"),
    (True, b"true"),
    (False, b"false"),
    ({}, b"{}"),
    ({"test": 1}, b'{"test":1}'),
    ({"test": []}, b'{"test":[]}'),
    ([{"test": [1]}], b'[{"test":[1]}]'),
]

CONTROL_CHARS = [(chr(c), '"\\u{c:04X}"'.format(c=c).encode()) for c in range(0x00, 0x08)]
CONTROL_CHARS.extend((chr(c), f'"\\u{c:04X}"'.encode()) for c in range(0x0E, 0x20))
CONTROL_CHARS.append(("\x7F", b'"\\u007F"'))


@pytest.mark.parametrize(("obj", "json"), DATA)
def test_json(obj: Any, json: bytes) -> None:
    assert ft.dumps(obj) == json
    assert ft.loads(json) == obj


@pytest.mark.parametrize(
    "obj",
    [
        "П@!",
        "😀!\n",
        "ts1.\\",
        "Text with emojis 😊🔥🌍",
        "𝒜𝓃𝒸𝒾𝑒𝓃𝓉 𝓊𝓃𝒾𝒸𝑜𝒹𝑒 𝓈𝓎𝓂𝒷𝑜𝓁𝓈",
        "Тестовый текст with some English words",
        "混合されたテキスト (Japanese mixed with English)",
        "Zahlen: 1234567890, спецсимволы: !@#$%^&*()_+-=[]{}",
        "できる？:あぁ……ごめん✋\nトプ画をみて:照れますがな😘✨\n一言:お前は一生もんのダチ💖",
        "合わない\n好きなところ:ぶすでキモいとこ😋✨✨\n思い出:んーーー、ありすぎ😊❤️\nLINE交換",
        "@aym0566x \n\n名前:前田あゆみ\n第一印象:なんか怖っ！\n今の印象:とりあえずキモい。噛み",
        "無言フォローはあまり好みません ゲームと動画が好きですシモ野郎ですがよろしく…最近はMGSとブレイブルー、音ゲーをプレイしてます",
    ],
)
def test_dumps_loads(obj: Any) -> None:
    assert ft.loads(ft.dumps(obj)) == obj


@pytest.mark.parametrize("char,json", CONTROL_CHARS)
def test_control_chars(char: str, json: bytes) -> None:
    assert ft.dumps(char) == json
    assert ft.loads(json) == char


@pytest.mark.parametrize("base", [10**20])
def test_negative_dumps(base: Any) -> None:
    with pytest.raises(ft.JsonEncodeError):
        ft.dumps(base)


@pytest.mark.parametrize("base", [b"1.", b"{1: 1}", b'{"test": 1,}', b"[1, 2,]", b"[1] ,", b"Null"])
def test_negative_loads(base: bytes) -> None:
    with pytest.raises(ft.JsonDecodeError):
        ft.loads(base)


class EnumStr(str, Enum):
    test = "TEST"


class EnumInt(int, Enum):
    test = 0


class SubUUID(UUID):...


class TestAsJson:
    def __as_json__(self) -> str:
        return "__as_json__"


@pytest.mark.parametrize(
    "base,res",
    [
        (1.1e-6, b"1.1e-6"),
        (1.1e6, b"1.1e6"),
        (1.1e5, b"1.1e5"),
        (1.1e-5, b"1.1e-5"),
        (1.1e-4, b"1.1e-4"),
        (1.1e4, b"1.1e4"),
        (0.0, b"0.0"),
        (1.1, b"1.1"),
        (1e10, b'1e10'),
        (1.1e10, b"1.1e10"),
        (-1.1e-6, b"-1.1e-6"),
        (-1.1e6, b"-1.1e6"),
        (-1.1e-4, b"-1.1e-4"),
        (-1.1e4, b"-1.1e4"),
        (-1.1, b"-1.1"),
        (-1e10, b'-1e10'),
        (1.1e10, b"1.1e10"),
        (EnumInt.test, b'0'),
        (EnumStr.test, b'"TEST"'),
        (TestAsJson(), b'"__as_json__"'),
        (datetime.date(2000, 1, 1), b'"2000-01-01"'),
        (datetime.time(1, 1, 1, 1), b'"01:01:01:000001"'),
        (datetime.datetime(2000, 1, 1, 1, 1, 1, 1), b'"2000-01-01T01:01:01:000001"'),
        (UUID("3e0cbe09-e9af-4b00-a8fe-a8f7181ad138"), b'"3e0cbe09-e9af-4b00-a8fe-a8f7181ad138"'),
        (SubUUID("3e0cbe09-e9af-4b00-a8fe-a8f7181ad138"), b'"3e0cbe09-e9af-4b00-a8fe-a8f7181ad138"'),
    ],
)
def test_dumps(base: float, res: bytes) -> None:
    assert ft.dumps(base) == res


def test_nan() -> None:
    assert isnan(ft.loads(b"NaN"))
    assert ft.dumps(float("Nan")) == b"NaN"


@pytest.mark.parametrize(
    ("kwargs", "params", "res"),
    [
        ({"a": 1, "b": 2, "c": 3}, {"by_alias": False}, b'{"a":1,"b":2,"c":3}'),
        ({"a": 1, "b": 2, "c": None}, {"exclude_none": True}, b'{"a_a":1,"b":2}'),
    ],
)
def test_as_json(kwargs: dict[str, Any], params: dict[str, Any], res: Any) -> None:
    class Base(ft.DataModel):
        a: Annotated[Any, ft.Field(serialization_alias="a_a")]
        b: Any
        c: Any

    assert ft.dumps(Base(**kwargs), **params) == res


def test_as_json_exclude_unset() -> None:
    class Base(ft.DataModel):
        a: Annotated[Any, ft.Field(init=False)]
        b: Any
        c: Any

    assert ft.dumps(Base(b=2, c=3), exclude_unset=True) == b'{"b":2,"c":3}'  # type: ignore


if __name__ == "__main__":
    pytest.main([__file__])
