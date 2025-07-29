from typing import Annotated, Type, Any
import pytest
import frost_typing as ft


class Base(ft.DataModel):
    null: str


class Model(Base):
    third: str
    first: Annotated[str, ft.Field("first")] = "first"
    second: Annotated[str, ft.Field("second")] = "second"


@pytest.fixture(scope="function")
def theft() -> Type[Any]:
    class Theft:
        null: str
        third: str
        first: Annotated[str, ft.Field("first")]
        second: Annotated[str, ft.Field("second")]

        def __init__(self, null, third, first="first", second="second"):
            self.null = null
            self.first = first
            self.second = second
            self.third = third

    return Theft


def test_slots() -> None:
    from weakref import ref

    class _ModelDict(ft.DataModel):
        __slots__ = ("__dict__",)
        first: Annotated[str, ft.Field("first")]
        second: Annotated[str, ft.Field("second")]

    class ModelDict(_ModelDict):
        third: str

    class ModelDictWeakref(_ModelDict):
        __slots__ = ("__weakref__",)
        third: str

    class ModelWeakref(ft.DataModel):
        __slots__ = ("__weakref__",)
        third: str
        first: Annotated[str, ft.Field("first")]
        second: Annotated[str, ft.Field("second")]

    dict_model = ModelDict(third="third")  # type: ignore
    dict_model.new_attr = "new_attr"  # type: ignore
    assert dict_model.first == "first"
    assert dict_model.second == "second"
    assert dict_model.third == "third"
    assert dict_model.__dict__ == {"new_attr": "new_attr"}

    weakref_model = ModelWeakref(third="third")  # type: ignore
    assert weakref_model.first == "first"
    assert weakref_model.second == "second"
    assert weakref_model.third == "third"
    assert ref(weakref_model)

    dict_weakref_model = ModelDictWeakref(third="third")  # type: ignore
    assert dict_weakref_model.first == "first"
    assert dict_weakref_model.second == "second"
    assert dict_weakref_model.third == "third"
    assert ref(dict_weakref_model)


def multiple_inheritance() -> None:
    class ModelDict(dict, ft.DataModel):  # type: ignore
        first: Annotated[str, ft.Field("first")]
        second: Annotated[str, ft.Field("second")]
        third: str

    data = ModelDict()  # type: ignore
    data.third = "third"
    data["new_attr"] = "new_attr"
    assert data.first == "first"
    assert data.second == "second"
    assert data.third == "third"
    assert data["new_attr"] == "new_attr"

    class ModelDictR(ft.DataModel, dict):  # type: ignore
        first: Annotated[str, ft.Field("first")]
        second: Annotated[str, ft.Field("second")]
        third: str

    datar = ModelDictR(third="third")  # type: ignore
    datar["new_attr"] = "new_attr"
    assert datar.first == "first"
    assert datar.second == "second"
    assert datar.third == "third"
    assert data["new_attr"] == "new_attr"

    class ModelDictW(dict, ft.DataModel):  # type: ignore
        __slots__ = ("__weakref__",)
        first: Annotated[str, ft.Field("first")]
        second: Annotated[str, ft.Field("second")]
        third: str

    dataw = ModelDictW()  # type: ignore
    dataw.third = "third"
    dataw["new_attr"] = "new_attr"
    assert dataw.first == "first"
    assert dataw.second == "second"
    assert dataw.third == "third"
    assert dataw["new_attr"] == "new_attr"


def test_meta() -> None:
    class MetaTest(dict, metaclass=ft.MetaModel):  # type: ignore
        first: str

    data = MetaTest()  # type: ignore
    data.first = "first"
    data["dict"] = "dict"
    assert data.first == "first"
    assert data["dict"] == "dict"


def test_theft(theft: Any) -> None:
    obj = theft(null="null", third="third")
    theft.__hash__ = Model.__hash__

    with pytest.raises(TypeError, match="descriptor '__hash__' requires a 'frost_typing.DataModel' object but received a 'Theft'"):
        hash(obj)

    theft.as_dict = Model.as_dict
    with pytest.raises(TypeError, match="descriptor 'as_dict' for 'frost_typing.DataModel' objects doesn't apply to a 'Theft' object"):
        obj.as_dict()

    theft.__init__ = Model.__init__
    with pytest.raises(TypeError, match="descriptor '__init__' requires a 'frost_typing.DataModel' object but received a 'Theft'"):
        theft(null="null", third="third")


def test_removed_obj() -> None:
    obj = Model(null="null", third="third")

    del obj.null
    with pytest.raises(AttributeError, match="'Model' object has no attribute 'null'"):
        obj.null

    assert obj.first == "first"

    del obj.third
    with pytest.raises(AttributeError, match="'Model' object has no attribute 'third'"):
        obj.third

    assert obj.second == "second"


def test_set_type() -> None:
    class _Model(ft.DataModel):
        null: str
        first: str
        second: str
        third: str

    _Model.null = "null"
    _Model.first = "first"
    _Model.third = "third"
    _Model.second = "second"

    assert _Model.null == "null"
    assert _Model.first == "first"
    assert _Model.third == "third"
    assert _Model.second == "second"


def test_missing() -> None:
    with pytest.raises(TypeError, match=r"__init__\(\) missing 1 required positional arguments: 'null'"):
        Model(third="third")  # type: ignore

    with pytest.raises(TypeError, match=r"__init__\(\) missing 2 required positional arguments: 'null' and 'third'"):
        Model()  # type: ignore


def test_theft_comparisons(theft: Any) -> None:
    obj = theft(null="null", third="third")

    theft.__eq__ = Model.__eq__
    with pytest.raises(TypeError, match="descriptor '__eq__' requires a 'frost_typing.DataModel' object but received a 'Theft'"):
        obj == obj

    theft.__ne__ = Model.__ne__
    with pytest.raises(TypeError, match="descriptor '__ne__' requires a 'frost_typing.DataModel' object but received a 'Theft'"):
        obj != obj

    theft.__lt__ = Model.__lt__
    with pytest.raises(TypeError, match="descriptor '__lt__' requires a 'frost_typing.DataModel' object but received a 'Theft'"):
        obj < obj

    theft.__le__ = Model.__le__
    with pytest.raises(TypeError, match="descriptor '__le__' requires a 'frost_typing.DataModel' object but received a 'Theft'"):
        obj <= obj

    theft.__gt__ = Model.__gt__
    with pytest.raises(TypeError, match="descriptor '__gt__' requires a 'frost_typing.DataModel' object but received a 'Theft'"):
        obj > obj

    theft.__ge__ = Model.__ge__
    with pytest.raises(TypeError, match="descriptor '__ge__' requires a 'frost_typing.DataModel' object but received a 'Theft'"):
        obj >= obj


def test_from_attributes() -> None:
    data = Model(null="null", third="third")
    assert Model.from_attributes(data) == data


def test_computed_field() -> None:
    class TestsComputedField(ft.DataModel):
        _cnt: Annotated[int, ft.Field(default=0, init=False, repr=False, dict=False, json=False)]
        x: int
        y: int
        z: int

        @ft.computed_field(field=ft.Field(repr=False))
        def volume(self) -> int:
            # Fields are cached
            assert not self._cnt
            self._cnt += 1
            return self.x * self.y * self.z

    data = TestsComputedField(1, 2, 3)  # type: ignore
    assert data.volume == 6
    assert data.volume == 6

    with pytest.raises(AttributeError, match=r"'TestsComputedField' object attribute 'volume' is read-only"):
        data.volume = 1

    assert repr(data) == "TestsComputedField(x=1, y=2, z=3)"
    assert data.as_dict() == {"x": 1, "y": 2, "z": 3, "volume": 6}
    assert data.as_json() == b'{"x":1,"y":2,"z":3,"volume":6}'


def test_redefinition() -> None:
    class Base(ft.DataModel):
        a: int

    class Sub(Base):
        a: int

    assert len(Sub.__schemas__) == 1
    assert Sub.__schemas__[0].type is int
    assert Base.__basicsize__ == 24
    assert Sub.__basicsize__ == 24


def test_field_serializer_redefinition() -> None:
    class Base(ft.DataModel):
        a: int

        @ft.field_serializer("a")
        def a_serializer(self, a: int) -> str:
            return str(a)

    base = Base(a=1)
    assert base.as_dict() == {"a": "1"}
    assert base.as_json() == b'{"a":"1"}'

    class Sub(Base):
        ...

    sub = Sub(a=1)
    assert sub.as_dict() == {"a": "1"}
    assert sub.as_json() == b'{"a":"1"}'

    class Redefinition(Sub):
        @ft.field_serializer("a")
        def a_serializer(self, a: int) -> str:
            return f"redefinition_{a}"

    redefinition = Redefinition(a=1)
    assert redefinition.as_dict() == {"a": "redefinition_1"}
    assert redefinition.as_json() == b'{"a":"redefinition_1"}'


@pytest.mark.parametrize(
    ("kwargs", "params", "res"),
    [
        ({"a": 1, "b": 2, "c": 3}, {"by_alias": False}, b'{"a":1,"b":2,"c":3}'),
        ({"a": 1, "b": 2, "c": None}, {"exclude_none": True}, b'{"a_a":1,"b":2}'),
        ({"a": 1, "b": 2, "c": 3}, {"exclude": {"a"}}, b'{"b":2,"c":3}'),
        ({"a": 1, "b": 2, "c": 3}, {"exclude": None}, b'{"a_a":1,"b":2,"c":3}'),
        ({"a": 1, "b": 2, "c": 3}, {"include": {"a"}}, b'{"a_a":1}'),
        ({"a": 1, "b": 2, "c": 3}, {"include": None}, b'{"a_a":1,"b":2,"c":3}'),
    ],
)
def test_as_json(kwargs: dict[str, Any], params: dict[str, Any], res: Any) -> None:
    class Base(ft.DataModel):
        a: Annotated[Any, ft.Field(serialization_alias="a_a")]
        b: Any
        c: Any

    assert Base(**kwargs).as_json(**params) == res


@pytest.mark.parametrize(
    ("kwargs", "params", "res"),
    [
        ({"a": 1, "b": 2, "c": 3}, {"by_alias": False}, {"a": 1, "b": 2, "c": 3}),
        ({"a": 1, "b": 2, "c": None}, {"exclude_none": True}, {"a_a": 1, "b": 2}),
        ({"a": 1, "b": 2, "c": 3}, {"exclude": {"a"}}, {"b": 2, "c": 3}),
        ({"a": 1, "b": 2, "c": 3}, {"exclude": None}, {"a_a": 1, "b": 2, "c": 3}),
        ({"a": 1, "b": 2, "c": 3}, {"include": {"a"}}, {"a_a": 1}),
        ({"a": 1, "b": 2, "c": 3}, {"include": None}, {"a_a": 1, "b": 2, "c": 3}),
    ],
)
def test_as_dict(kwargs: dict[str, Any], params: dict[str, Any], res: Any) -> None:
    class Base(ft.DataModel):
        a: Annotated[Any, ft.Field(serialization_alias="a_a")]
        b: Any
        c: Any

    assert Base(**kwargs).as_dict(**params) == res


def test_as_json_exclude_unset() -> None:
    class Base(ft.DataModel):
        a: Any
        b: Any
        c: Annotated[Any, ft.Field(init=False)]

    assert Base(a=1, b=2).as_json(exclude_unset=True) == b'{"a":1,"b":2}'  # type: ignore


def test_as_dict_exclude_unset() -> None:
    class Base(ft.DataModel):
        a: Any
        b: Any
        c: Annotated[Any, ft.Field(init=False)]

    assert Base(a=1, b=2).as_dict(exclude_unset=True) == {"a": 1, "b": 2}  # type: ignore


def test_override_new() -> None:
    class TestSub(ft.DataModel):
        def __new__(cls) -> "TestSub":
            return super().__new__(cls)

    assert TestSub() == ft.DataModel.__new__(TestSub)

    class TestMeta(metaclass=ft.MetaModel):
        def __new__(cls) -> "TestMeta":
            return super().__new__(cls)

    assert TestMeta()


def test_override_init() -> None:
    class TestSub(ft.DataModel):
        __slots__ = ("__dict__", )

        def __init__(self, *args, **kwargs) -> None:
            self.a = 1  # type: ignore

    assert TestSub().a == 1  # type: ignore

    class TestMeta(metaclass=ft.MetaModel):
        a: int

        def __init__(self, a: int) -> None:
            self.a = a

    assert TestMeta(a=1).a == 1


if __name__ == "__main__":
    pytest.main([__file__])
