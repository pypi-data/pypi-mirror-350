# mypy: ignore-errors
import pytest
from enum import Enum
import frost_typing as ft
from typing import Annotated, TypedDict, Optional, Generic, TypeVar, Union, Any

try:
    ft.json_schema(int)
    skip_json_schema = False
except NotImplementedError:
    skip_json_schema = True


class TestForwardRef(metaclass=ft.MetaModel):
    a: "_TestForwardRef"


class _TestForwardRef(ft.DataModel): ...


class Point(TypedDict):
    x: int
    y: int


@pytest.mark.skipif(skip_json_schema, reason="Json Schema is not included in the compilation")
@pytest.mark.parametrize(
    ("hint", "schema"),
    [
        (Any, {}),
        (..., {}),
        (str, {"type": "string"}),
        (int, {"type": "integer"}),
        (float, {"type": "number"}),
        (bytes, {"format": "binary", "type": "string"}),
        (bytearray, {"format": "binary", "type": "string"}),
        (list[int], {"type": "array", "items": {"type": "integer"}}),
        (tuple[int], {"type": "array", "items": {"type": "integer"}}),
        (Optional[int], {"anyOf": [{"type": "integer"}, {"type": "null"}]}),
        (Union[int, str], {"anyOf": [{"type": "integer"}, {"type": "string"}]}),
        (set[int], {"items": {"type": "integer"}, "type": "array", "uniqueItems": True}),
        (frozenset[int], {"items": {"type": "integer"}, "type": "array", "uniqueItems": True}),
        (
            Annotated[list[int], ft.SequenceConstraints(min_length=1, max_length=10)],
            {"type": "array", "items": {"type": "integer"}, "maxLength": 10, "minLength": 1},
        ),
        (dict[str, int], {"type": "object", "additionalProperties": {"type": "integer"}}),
        (list[Union[str, bool]], {"type": "array", "items": {"anyOf": [{"type": "string"}, {"type": "boolean"}]}}),
        (list[Union[str, int]], {"type": "array", "items": {"anyOf": [{"type": "string"}, {"type": "integer"}]}}),
        (Annotated[str, ft.StringConstraints(pattern=r"^\d+$")], {"type": "string", "pattern": "^\\d+$"}),
        (
            Point,
            {
                "type": "object",
                "title": "Point",
                "required": ["x", "y"],
                "properties": {"x": {"type": "integer", "title": "X"}, "y": {"type": "integer", "title": "Y"}},
            },
        ),
    ],
)
def test_base(hint: Any, schema: dict["str", Any]) -> None:
    assert ft.json_schema(hint) == schema


@pytest.mark.skipif(skip_json_schema, reason="Json Schema is not included in the compilation")
def test_base_model() -> None:
    class SEnum(str, Enum):
        TYPE = "type"
        NAME = "name"

    class Model(ft.DataModel):
        null: int
        first: Annotated[str, ft.Field("first")] = "first"
        second: Annotated[str, ft.Field("second")] = "second"
        third: SEnum

    assert ft.json_schema(SEnum) == {"type": "string", "enum": ["type", "name"], "title": "SEnum"}
    assert Model.json_schema() == {
        "type": "object",
        "required": ["null", "third"],
        "properties": {
            "null": {"type": "integer", "title": "Null"},
            "first": {"type": "string", "title": "First", "default": "first"},
            "second": {"type": "string", "title": "Second", "default": "second"},
            "third": {"$ref": "#/$defs/SEnum"},
        },
        "title": "Model",
        "$defs": {"SEnum": {"type": "string", "enum": ["type", "name"], "title": "SEnum"}},
    }
    assert ft.json_schema(TestForwardRef) == {
        "type": "object",
        "required": ["a"],
        "properties": {"a": {"$ref": "#/$defs/_TestForwardRef"}},
        "title": "TestForwardRef",
        "$defs": {"_TestForwardRef": {"type": "object", "properties": {}, "title": "_TestForwardRef"}},
    }


@pytest.mark.skipif(skip_json_schema, reason="Json Schema is not included in the compilation")
def test_annotated() -> None:
    class AnnotatedNestedModel(ft.DataModel):
        first: Annotated[list, ft.SequenceConstraints(min_length=3)]

    assert AnnotatedNestedModel.json_schema() == {
        "type": "object",
        "required": ["first"],
        "properties": {"first": {"type": "array", "items": {}, "minLength": 3, "title": "First"}},
        "title": "AnnotatedNestedModel",
    }

    class AnnotatedStringModel(ft.DataModel):
        first: Annotated[str, ft.StringConstraints(min_length=3, max_length=10, pattern=r"^\d+$")]

    AnnotatedStringModel.json_schema() == {
        "type": "object",
        "required": ["first"],
        "properties": {"first": {"type": "string", "maxLength": 10, "minLength": 3, "pattern": "^\\d+$", "title": "First"}},
        "title": "AnnotatedStringModel",
    }

    class AnnotatedComparisonModel(ft.DataModel):
        first: Annotated[int, ft.ComparisonConstraints(gt=1, ge=2, lt=2, le=4)]

    AnnotatedComparisonModel.json_schema() == {
        "type": "object",
        "required": ["first"],
        "properties": {"first": {"type": "integer", "ge": 2, "gt": 1, "le": 4, "lt": 2, "title": "First"}},
        "title": "AnnotatedComparisonModel",
    }


@pytest.mark.skipif(skip_json_schema, reason="Json Schema is not included in the compilation")
@pytest.mark.parametrize("obj,ex", (("int1", NameError),))
def test_json_schema_negative(obj: Any, ex: Any) -> None:
    with pytest.raises(ex):
        ft.json_schema(obj)


@pytest.mark.skipif(skip_json_schema, reason="Json Schema is not included in the compilation")
def test_generic() -> None:
    T = TypeVar("T")
    V = TypeVar("V")
    C = TypeVar("C")

    class Sub(ft.ValidModel, Generic[T, V, C]):
        a: T
        b: V
        c: C

    class Test(ft.ValidModel, Generic[V, C, T]):
        sub_a: Sub[V, C, T]
        sub_v: Sub[T, C, V]
        sub_c: Sub[T, V, C]

    assert Test.json_schema() == {
        "$defs": {
            "Sub[~T, ~C, ~V]": {"properties": {"a": {}, "b": {}, "c": {}}, "required": ["a", "b", "c"], "title": "Sub[~T, ~C, ~V]", "type": "object"},
            "Sub[~T, ~V, ~C]": {"properties": {"a": {}, "b": {}, "c": {}}, "required": ["a", "b", "c"], "title": "Sub[~T, ~V, ~C]", "type": "object"},
            "Sub[~V, ~C, ~T]": {"properties": {"a": {}, "b": {}, "c": {}}, "required": ["a", "b", "c"], "title": "Sub[~V, ~C, ~T]", "type": "object"},
        },
        "properties": {
            "sub_a": {"$ref": "#/$defs/Sub[~V, ~C, ~T]"},
            "sub_c": {"$ref": "#/$defs/Sub[~T, ~V, ~C]"},
            "sub_v": {"$ref": "#/$defs/Sub[~T, ~C, ~V]"},
        },
        "required": ["sub_a", "sub_v", "sub_c"],
        "title": "Test",
        "type": "object",
    }

    assert Test[int, str, bool].json_schema() == {
        "$defs": {
            "Sub[bool, int, str]": {
                "properties": {"a": {"title": "A", "type": "boolean"}, "b": {"title": "B", "type": "integer"}, "c": {"title": "C", "type": "string"}},
                "required": ["a", "b", "c"],
                "title": "Sub[bool, int, str]",
                "type": "object",
            },
            "Sub[bool, str, int]": {
                "properties": {"a": {"title": "A", "type": "boolean"}, "b": {"title": "B", "type": "string"}, "c": {"title": "C", "type": "integer"}},
                "required": ["a", "b", "c"],
                "title": "Sub[bool, str, int]",
                "type": "object",
            },
            "Sub[int, str, bool]": {
                "properties": {"a": {"title": "A", "type": "integer"}, "b": {"title": "B", "type": "string"}, "c": {"title": "C", "type": "boolean"}},
                "required": ["a", "b", "c"],
                "title": "Sub[int, str, bool]",
                "type": "object",
            },
        },
        "properties": {
            "sub_a": {"$ref": "#/$defs/Sub[int, str, bool]"},
            "sub_c": {"$ref": "#/$defs/Sub[bool, int, str]"},
            "sub_v": {"$ref": "#/$defs/Sub[bool, str, int]"},
        },
        "required": ["sub_a", "sub_v", "sub_c"],
        "title": "Test[int, str, bool]",
        "type": "object",
    }


if __name__ == "__main__":
    pytest.main([__file__])
