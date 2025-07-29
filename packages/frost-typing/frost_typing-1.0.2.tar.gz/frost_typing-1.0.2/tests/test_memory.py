# mypy: ignore-errors
import gc
try:
    import psutil
except ImportError:
    psutil = None  # type: ignore

import pytest
import asyncio
import frost_typing as ft
from typing import Callable, Generic, TypedDict, TypeVar, Type, Any, Annotated, Union, Literal
from functools import wraps

try:
    ft.json_schema(int)
    skip_json_schema = False
except NotImplementedError:
    skip_json_schema = True

MAX_INCREASE = 4194304  # 4MiB
FIXTURE = '{"a":[124261, 146134.1235], "b": true, "c": null, "d": "東京"}'


def memory_check(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        proc = psutil.Process()
        gc.collect()
        mem = proc.memory_info().rss

        res = func(*args, **kwargs)

        gc.collect()
        assert proc.memory_info().rss <= mem + MAX_INCREASE
        return res
    return wrapper


@pytest.mark.skipif(psutil is None, reason="psutil not installed")
@memory_check
def test_memory_loads() -> None:
    for _ in range(100_000):
        val = ft.loads(FIXTURE)
        assert val


@pytest.mark.skipif(psutil is None, reason="psutil not installed")
@memory_check
def test_memory_dumps() -> None:
    fixture = ft.loads(FIXTURE)
    assert fixture
    for _ in range(100_000):
        val = ft.dumps(fixture)
        assert val


@pytest.mark.skipif(psutil is None, reason="psutil not installed")
@memory_check
def test_memory_dumps_ex() -> None:
    class Unsupported:
        ...

    data = Unsupported()
    i = 0
    n = 100_000
    for _ in range(n):
        try:
            ft.dumps(data)
        except ft.JsonEncodeError:
            i += 1

    assert i == n


@pytest.mark.skipif(psutil is None, reason="psutil not installed")
@memory_check
def test_memory_loads_ex() -> None:
    class Unsupported:
        ...

    i = 0
    n = 100_000
    for _ in range(n):
        try:
            ft.loads(b"")
        except ft.JsonDecodeError:
            i += 1

    assert i == n


@pytest.mark.skipif(psutil is None, reason="psutil not installed")
@memory_check
def test_memory_dumps_redefined() -> None:
    class Redefined:
        def __as_json__(self) -> str:
            return "test"

    data = Redefined()
    for _ in range(100_000):
        ft.dumps(data)


@pytest.mark.skipif(psutil is None, reason="psutil not installed")
@pytest.mark.parametrize(
    "base,method,kwargs,res",
    [
        (ft.ValidModel, "as_dict", {}, {"a": "1", "b": "test_test", "c": {"data": (1.2, 2.3)}}),
        (ft.ValidModel, "as_dict", {"as_json": True}, {"a": "1", "b": "test_test", "c": {"data": [1.2, 2.3]}}),
        (ft.ValidModel, "as_json", {}, b'{"a":"1","b":"test_test","c":{"data":[1.2,2.3]}}'),
        (ft.DataModel, "as_dict",  {}, {"a": "1", "b": "test_test", "c": {"data": (1.2, 2.3)}}),
        (ft.DataModel, "as_dict",  {"as_json": True}, {"a": "1", "b": "test_test", "c": {"data": [1.2, 2.3]}}),
        (ft.DataModel, "as_json",  {}, b'{"a":"1","b":"test_test","c":{"data":[1.2,2.3]}}'),
    ],
)
@memory_check
def test_memory_dumps_model(base: Type[Any], method: str, kwargs: dict[str, Any], res: Any) -> None:
    class Redefined(base):
        a: int
        b: str
        c: tuple[float, ...]

        @ft.field_serializer("a")
        def a_serializer(self, a: int) -> str:
            return str(a)

        @ft.field_serializer("b")
        def b_serializer(self, b: str) -> str:
            return f'test_{b}'

        @ft.field_serializer("c")
        def c_serializer(self, c: list[float]) -> dict[str, list[float]]:
            return {"data": c}

    data = Redefined(a=1, b="test", c=(1.2, 2.3))
    for _ in range(100_000):
        assert getattr(data, method)(**kwargs) == res


@pytest.mark.skipif(psutil is None, reason="psutil not installed")
@memory_check
def test_memory_nested_valid() -> None:
    class Sub(ft.ValidModel):
        a: int

    class Redefined(ft.ValidModel):
        sub: Sub

    for _ in range(10_000):
        Redefined(sub={"a": 1})


@pytest.mark.skipif(psutil is None, reason="psutil not installed")
@memory_check
def test_memory_overloaded_nested_valid() -> None:
    class Sub(ft.ValidModel):
        a: int
        @classmethod
        def __frost_validate__(cls, val: Any, ctx: ft.ContextManager) -> "Sub":
            return super().__frost_validate__(val, ctx)

    class Redefined(ft.ValidModel):
        sub: Sub

    for _ in range(10_000):
        Redefined(sub={"a": 1})


@pytest.mark.skipif(psutil is None, reason="psutil not installed")
@pytest.mark.parametrize("base", [ft.ValidModel, ft.DataModel])
@memory_check
def test_memory_meta(base: Type[Any]) -> None:
    for _ in range(10_000):
        class Redefined(base):
            a: int
            b: str
            c: list[float]

            @ft.field_serializer("a")
            def a_serializer(self, a: int) -> str:
                return str(a)

            @ft.field_serializer("b")
            def b_serializer(self, b: str) -> str:
                return f'test_"{b}"'

            @ft.field_serializer("c")
            def c_serializer(self, c: list[float]) -> dict[str, list[float]]:
                return {"data": c}


@pytest.mark.skipif(psutil is None, reason="psutil not installed")
@memory_check
def test_memory_valid_meta() -> None:
    for _ in range(10_000):
        class Redefined(ft.ValidModel):
            a: int
            b: str
            c: list[float]

            @ft.field_validator("a", mode="before")
            @classmethod
            def a_validate(cls, a: int) -> int:
                return a

            @ft.field_validator("b", mode="before")
            @classmethod
            def b_validate(cls, b: str) -> str:
                return b

            @ft.field_validator("c", mode="before")
            @classmethod
            def c_validate(cls, c: list[float]) -> list[float]:
                return c

            @ft.field_serializer("a")
            def a_serializer(self, a: int) -> str:
                return str(a)

            @ft.field_serializer("b")
            def b_serializer(self, b: str) -> str:
                return f'test_"{b}"'

            @ft.field_serializer("c")
            def c_serializer(self, c: list[float]) -> dict[str, list[float]]:
                return {"data": c}


@pytest.mark.skipif(psutil is None, reason="psutil not installed")
@pytest.mark.parametrize("base", [ft.ValidModel, ft.DataModel])
@memory_check
def test_memory_init(base: Type[Any]) -> None:
    class Sub(base):
        a: int
        b: str
        c: float
        d: bytes
        f: bytearray

    class Validation(base):
        sub: Sub
        list_: list[int]
        tuple_: tuple[int, ...]
        set_: set[int]
        frozenset_: frozenset[int]
        dict_: dict[str, int]

    for _ in range(10_000):
        Validation(
            sub={"a": 1, "b": "b", "c": 1.1, "d": "d", "f": "f"},
            list_=(1, 2, 3),
            tuple_=[1, 2, 3],
            set_=(1, 2, 3),
            frozenset_=(1, 2, 3),
            dict_={"test": 1},
        )


@pytest.mark.skipif(psutil is None, reason="psutil not installed")
@memory_check
def test_memory_validation_ex() -> None:
    class Sub(ft.ValidModel):
        a: int
        b: str
        c: float
        d: bytes
        f: bytearray

    class Validation(ft.ValidModel):
        sub: Sub
        list_: list[int]
        tuple_: tuple[int, ...]
        set_: set[int]
        frozenset_: frozenset[int]
        dict_: dict[str, int]

    n = 1
    i = 0
    for _ in range(n):
        try:
            Validation(
                sub={"a": "1.1", "b": 1, "c": "a", "d": 1, "f": 2},
                list_=["a"],
                tuple_=["a"],
                set_=["a"],
                frozenset_=["a"],
                dict_=["a"],
            )
        except ft.ValidationError:
            i += 1
    assert n == i


@pytest.mark.skipif(psutil is None, reason="psutil not installed")
@memory_check
def test_memory_func_create_validator() -> None:
    for _ in range(10_000):
        @ft.validated_func
        def test(a: int, b: str) -> None: ...


@pytest.mark.skipif(psutil is None, reason="psutil not installed")
@memory_check
def test_memory_validated_func() -> None:
    class Sub(ft.ValidModel):
        a: int
        b: str
        c: float
        d: bytes
        f: bytearray

    @ft.validated_func
    def test(
        sub: Sub, list_: list[int], tuple_: tuple[int, ...], set_: set[int], frozenset_: frozenset[int], dict_: dict[str, int]
    ) -> None: ...

    for _ in range(10_000):
        test(
            sub={"a": 1, "b": "b", "c": 1.1, "d": "d", "f": "f"},
            list_=(1, 2, 3),
            tuple_=[1, 2, 3],
            set_=(1, 2, 3),
            frozenset_=(1, 2, 3),
            dict_={"test": 1},
        )


@pytest.mark.skipif(psutil is None, reason="psutil not installed")
@pytest.mark.parametrize(
    "args,kwargs,res,err",
    [
        (("1", "1"), {}, 2, False),
        (("", ""), {}, 2, True),
        ((), {"a": "1", "b": "1"}, 2, False),
        ((), {"a": "", "b": ""}, 2, True),
    ]
)
@memory_check
def test_memory_validated_func_async(args: Any, kwargs: dict[str, Any], res: Any, err: bool) -> None:
    @ft.validated_func
    async def func(a: int, b: int) -> int:
        return str(a + b)

    async def test() -> None:
        for _ in range(10_000):
            try:
                assert res == await func(*args, **kwargs)
                assert not err
            except ft.ValidationError: ...

    asyncio.run(test())


@pytest.mark.skipif(psutil is None, reason="psutil not installed")
@memory_check
def test_memory_validated_func_ex() -> None:
    class Sub(ft.ValidModel):
        a: int
        b: str
        c: float
        d: bytes
        f: bytearray

    @ft.validated_func
    def test(
        sub: Sub, list_: list[int], tuple_: tuple[int, ...], set_: set[int], frozenset_: frozenset[int], dict_: dict[str, int]
    ) -> None: ...

    i = 0
    n = 10_000
    for _ in range(n):
        try:
            test(
                sub={"a": "1.1", "b": 1, "c": "a", "d": 1, "f": 2},
                list_=["a"],
                tuple_=["a"],
                set_=["a"],
                frozenset_=["a"],
                dict_=["a"],
            )
        except ft.ValidationError:
            i += 1
    assert n == i


@pytest.mark.skipif(psutil is None, reason="psutil not installed")
@memory_check
def test_memory_func_constraint() -> None:
    for _ in range(10_000):
        ft.con_comparison(int, gt=1, ge=2, lt=1, le=3)
        ft.con_sequence(list, min_length=10, max_length=12)
        ft.con_string(str, strip_whitespace=True, min_length=10, max_length=12, pattern=r"\d+$")
        ft.field(int, default=1, default_factory=int, alias="test", examples=[1, 2])


@pytest.mark.skipif(psutil is None, reason="psutil not installed")
@memory_check
def test_memory_data_model_from_attributes() -> None:
    class Test(ft.DataModel):
        a: list[int]
        b: set[int]

    for _ in range(10_000):
        data1 = Test([1, 2, 3], {1, 2, 3})
        data2 = Test.from_attributes(data1)
        assert data1 == data2


@pytest.mark.skipif(psutil is None, reason="psutil not installed")
@memory_check
def test_memory_valid_model_from_attributes() -> None:
    class Test(ft.ValidModel):
        a: list[int]
        b: set[int]

    for _ in range(10_000):
        data1 = Test(a=[1, 2, 3], b={1, 2, 3})
        data2 = Test.from_attributes(data1)
        assert data1 == data2


@pytest.mark.skipif(psutil is None, reason="psutil not installed")
@memory_check
def test_memory_sequence_create_type() -> None:
    T = TypeVar("T")

    for _ in range(10_000):
        class Test(ft.ValidModel, Generic[T]):
            a: list[T]
            b: set[T]


@pytest.mark.skipif(psutil is None, reason="psutil not installed")
@memory_check
def test_memory_sequence_func_create_type() -> None:
    T = TypeVar("T")

    for _ in range(10_000):
        @ft.validated_func[T]
        def test(a: list[T], b: set[T]) -> set[T]:
            return b


@pytest.mark.skipif(psutil is None, reason="psutil not installed")
@memory_check
def test_memory_generic() -> None:
    T = TypeVar("T")

    class Test(ft.ValidModel, Generic[T]):
        a: list[T]
        b: set[T]

    for _ in range(10_000):
        data = Test[int](a=["1", "2"], b={"1", "2"})
        assert data.a == [1, 2]
        assert data.b == {1, 2}


@pytest.mark.skipif(psutil is None, reason="psutil not installed")
@memory_check
def test_memory_generic_func() -> None:
    T = TypeVar("T")

    @ft.validated_func[T]
    def test(a: list[T], b: set[T]) -> set[T]:
        return b

    for _ in range(10_000):
        res = test[int](a=["1", "2"], b={"1", "2"})
        assert res == {1, 2}


@pytest.mark.skipif(psutil is None, reason="psutil not installed")
@pytest.mark.skipif(skip_json_schema, reason="Json Schema is not included in the compilation")
@memory_check
def test_memory_json_schema() -> None:
    T = TypeVar("T")
    V = TypeVar("V")

    class Sub(ft.ValidModel, Generic[T]):
        q: frozenset[T]
        w: dict[T, T]
        e: bytearray
        r: tuple[T]
        t: list[T]
        y: set[T]
        u: bytes
        i: float
        o: bool
        p: int
        a: str
        s: T

    class Test(ft.ValidModel, Generic[T, V]):
        sub_t: Sub[T]
        sub_v: Sub[V]

    for _ in range(10_000):
        Test[int, str].json_schema()


@pytest.mark.skipif(psutil is None, reason="psutil not installed")
@memory_check
def test_memory_typed_dict() -> None:
    class Point(TypedDict):
        x: int
        y: int
        z: int

    adapter = ft.TypeAdapter(Point)
    for _ in range(10_000):
        assert adapter.validate({"x": "1", "y": "1", "z": "1"}) == {"x": 1, "y": 1, "z": 1}


@pytest.mark.skipif(psutil is None, reason="psutil not installed")
@memory_check
def test_memory_typed_dict_err() -> None:
    class Point(TypedDict):
        x: int
        y: int
        z: int

    adapter = ft.TypeAdapter(Point)
    for _ in range(10_000):
        try:
            adapter.validate({})
        except ft.ValidationError:
            ...




@pytest.mark.parametrize(
    "kw,res",
    [
        ({"dicr_type": "BOOLEAN", "val": True}, True),
        ({"dicr_type": "BOOLEAN", "val": False}, False),
        ({"dicr_type": "STRING", "val": "string"}, "string"),
        ({"dicr_type": "INTEGER", "val": "-1"}, -1),
        ({"dicr_type": "INTEGER", "val": "1"}, 1),
        ({"dicr_type": "INTEGER", "val": 1}, 1),
    ],
)
@pytest.mark.skipif(psutil is None, reason="psutil not installed")
@memory_check
def test_memory_discriminator(kw: dict[str, Any], res: Any) -> None:
    class DiscriminatorTest(ft.ValidModel):
        dicr_type: Literal["BOOLEAN", "INTEGER", "STRING"]
        val: Annotated[
            Union[int, str, bool],
            ft.Discriminator(
                discriminator="dicr_type",
                mapping={
                    "BOOLEAN": bool,
                    "INTEGER": int,
                    "STRING": str,
                },
            ),
        ]
    for _ in range(10_000):
        data = DiscriminatorTest(**kw)
        assert data.val == res


if __name__ == "__main__":
    pytest.main([__file__])
