# -*- coding: utf-8 -*-
# mypy: ignore-errors
import pytest
import typing as tp
import frost_typing as ft


def test_config() -> None:
    class Base(ft.DataModel):
        __config__ = ft.Config(repr=False)

        null: int
        first: int

    data = Base(1, 2)
    assert repr(data) == "Base()"


def test_config_inheritance() -> None:
    class Base(ft.DataModel):
        __config__ = ft.Config(repr=False)

    class Model(Base):
        __config__ = ft.Config(init=False)

    assert Model.__config__.init is False
    assert Model.__config__.repr is False


def test_config_get() -> None:
    def gen(name: str) -> str:
        return name.title()

    config = ft.Config(True, False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, gen, "title", [1, 2])
    assert config.init is True
    assert config.repr is False
    assert config.hash is True
    assert config.dict is False
    assert config.json is True
    assert config.strict is False
    assert config.kw_only is True
    assert config.frozen is False
    assert config.comparison is True
    assert config.class_lookup is False
    assert config.frozen_type is True
    assert config.fail_on_extra_init is False
    assert config.validate_private is True
    assert config.auto_alias is False
    assert config.allow_inf_nan is True
    assert config.num_to_str is False
    assert config.alias_generator is gen
    assert config.title == "title"
    assert config.examples == [1, 2]


def test_config_get_default() -> None:
    config = ft.Config()
    assert config.init is True
    assert config.repr is True
    assert config.hash is True
    assert config.dict is True
    assert config.json is True
    assert config.strict is False
    assert config.kw_only is False
    assert config.frozen is False
    assert config.comparison is True
    assert config.class_lookup is True
    assert config.frozen_type is False
    assert config.fail_on_extra_init is False
    assert config.validate_private is True
    assert config.auto_alias is True
    assert config.num_to_str is False
    assert config.allow_inf_nan is True


def test_field_get() -> None:
    field = ft.Field(
        0, True, False, True, False, True, False, True, False, True, False, True, "alias", "title", [], "serialization_alias", str, {"test": "test"}
    )

    assert field.default == 0
    assert field.init is True
    assert field.repr is False
    assert field.hash is True
    assert field.dict is False
    assert field.json is True
    assert field.kw_only is False
    assert field.frozen is True
    assert field.comparison is False
    assert field.class_lookup is True
    assert field.frozen_type is False
    assert field.auto_alias is True
    assert field.alias == "alias"
    assert field.title == "title"
    assert field.examples == []
    assert field.serialization_alias == "serialization_alias"
    assert field.default_factory is str
    assert field.json_schema_extra == {"test": "test"}


def test_field_get_default() -> None:
    field = ft.Field()
    with pytest.raises(AttributeError):
        field.default

    assert field.init is True
    assert field.repr is True
    assert field.hash is True
    assert field.dict is True
    assert field.json is True
    assert field.kw_only is False
    assert field.frozen is False
    assert field.comparison is True
    assert field.class_lookup is True
    assert field.frozen_type is False
    assert field.auto_alias is True
    assert field.alias is None
    assert field.title is None
    assert field.examples is None
    assert field.serialization_alias is None
    assert field.default_factory is None
    assert field.json_schema_extra is None


def test_field_init() -> None:
    class Model(ft.DataModel):
        a: ft.field(int, init=False, default=1)
        b: ft.field(int, init=True)

    with pytest.raises(TypeError, match=r"__init__\(\) missing 1 required positional arguments: 'b'"):
        Model()


def test_valid_model_field_init() -> None:
    class Model(ft.ValidModel):
        a: ft.field(int, init=False, default=1)
        b: ft.field(int, init=True)

    with pytest.raises(ft.ValidationError):
        Model()


@pytest.mark.parametrize("base", [ft.DataModel, ft.ValidModel])
def test_field_init_default(base: tp.Type[tp.Any]) -> None:
    class Model(base):
        a: ft.field(int, init=False, default=1)
        b: ft.field(int, init=True)

    model = Model(b=2)
    assert model.a == 1
    assert model.b == 2


@pytest.mark.parametrize("base", [ft.DataModel, ft.ValidModel])
def test_field_init_default_factory(base: tp.Type[tp.Any]) -> None:
    class Model(base):
        a: ft.field(int, init=False, default_factory=int)
        b: ft.field(int, init=True)

    model = Model(b=2)
    assert model.a == 0
    assert model.b == 2


@pytest.mark.parametrize("base", [ft.DataModel, ft.ValidModel])
def test_field_repr(base: tp.Type[tp.Any]) -> None:
    class Model(base):
        a: ft.field(int, default=1)
        b: ft.field(int, default=2, repr=False)

    assert repr(Model()) == "Model(a=1)"


@pytest.mark.parametrize("base", [ft.DataModel, ft.ValidModel])
def test_field_hash(base: tp.Type[tp.Any]) -> None:
    class Model(base):
        a: ft.field(int, hash=False)
        b: ft.field(int, default=2)

    assert hash(Model(a=1)) == hash(Model(a=2))


@pytest.mark.parametrize("base", [ft.DataModel, ft.ValidModel])
def test_field_dict(base: tp.Type[tp.Any]) -> None:
    class Model(base):
        a: ft.field(int, dict=False)
        b: ft.field(int, default=2)

    assert Model(a=1).as_dict() == {"b": 2}


@pytest.mark.parametrize("base", [ft.DataModel, ft.ValidModel])
def test_field_json(base: tp.Type[tp.Any]) -> None:
    class Model(base):
        a: ft.field(int, json=False)
        b: ft.field(int, default=2)

    assert Model(a=1).as_json() == b'{"b":2}'


def test_field_kw_only() -> None:
    class Model(ft.DataModel):
        a: ft.field(int, kw_only=True)
        b: ft.field(int)

    data = Model(2, a=1)
    assert data.a == 1
    assert data.b == 2

    with pytest.raises(TypeError):
        Model(1, 2)


@pytest.mark.parametrize("base", [ft.DataModel, ft.ValidModel])
def test_field_frozen(base: tp.Type[tp.Any]) -> None:
    class Model(base):
        a: ft.field(int, frozen=True)

    data = Model(a=1)
    assert data.a == 1
    with pytest.raises(AttributeError):
        data.a = 2
    assert data.a == 1


@pytest.mark.parametrize("base", [ft.DataModel, ft.ValidModel])
def test_field_comparison(base: tp.Type[tp.Any]) -> None:
    class Model(base):
        a: ft.field(int, comparison=False)
        b: ft.field(int, default=1)

    assert Model(a=2) == Model(a=3)
    assert Model(a=2) <= Model(a=3)
    assert Model(a=2) >= Model(a=3)
    assert not (Model(a=2) != Model(a=3))


@pytest.mark.parametrize("base", [ft.DataModel, ft.ValidModel])
def test_field_class_lookup(base: tp.Type[tp.Any]) -> None:
    class Model(base):
        a: ft.field(int, class_lookup=True, init=False) = 1
        b: ft.field(int, class_lookup=False, init=False) = 2

    data = Model()
    assert data.a == 1

    with pytest.raises(AttributeError):
        data.b

    assert Model.a == 1
    assert Model.b == 2


@pytest.mark.parametrize("base", [ft.DataModel, ft.ValidModel])
def test_field_frozen_type(base: tp.Type[tp.Any]) -> None:
    class Model(base):
        a: ft.field(int, frozen_type=True) = 1
        b: ft.field(int, frozen_type=False) = 2

    assert Model.b == 2
    Model.b = 3
    assert Model.b == 3

    assert Model.a == 1
    with pytest.raises(AttributeError):
        Model.a = 4
    assert Model.a == 1


@pytest.mark.parametrize("base", [ft.DataModel, ft.ValidModel])
def test_field_default(base: tp.Type[tp.Any]) -> None:
    default = []

    class Model(base):
        a: ft.field(int, default=default)

    data = Model()
    assert data.a is not default
    assert data.a == default


@pytest.mark.parametrize(
    "base, config, is_raise", [
        (ft.DataModel, ft.Config(fail_on_extra_init=True), True),
        (ft.DataModel, ft.Config(fail_on_extra_init=False), False),
        (ft.DataModel, ft.DataModel.__config__, True),
        (ft.DataModel, ft.Config(), False),
        (ft.ValidModel, ft.Config(fail_on_extra_init=True), True),
        (ft.ValidModel, ft.Config(fail_on_extra_init=False), False),
        (ft.ValidModel, ft.ValidModel.__config__, False),
        (ft.ValidModel, ft.Config(), False),
    ]
)
def test_fail_on_extra_init(base: tp.Type[tp.Any], config: ft.Config, is_raise: bool) -> None:
    class Test(base):
        __config__ = config
        a: int
        
    if is_raise:
        with pytest.raises(TypeError, match=r"Test.__init__\(\) got an unexpected keyword argument 'b'"):
            Test(a=1, b=2)
    else:
        Test(a=1, b=2)


@pytest.mark.parametrize(
    "base, config", [
        (ft.DataModel, ft.Config(fail_on_extra_init=True)),
        (ft.DataModel, ft.Config(fail_on_extra_init=False)),
        (ft.DataModel, ft.DataModel.__config__),
        (ft.DataModel, ft.Config()),
        (ft.ValidModel, ft.Config(fail_on_extra_init=True)),
        (ft.ValidModel, ft.Config(fail_on_extra_init=False)),
        (ft.ValidModel, ft.ValidModel.__config__),
        (ft.ValidModel, ft.Config()),
    ]
)
def test_fail_on_extra_init_from_object(base: tp.Type[tp.Any], config: ft.Config) -> None:
    class Test(base):
        __config__ = config
        a: int

    assert Test.from_attributes({"a": 1, "b": 2}) == Test(a=1)


if __name__ == "__main__":
    pytest.main([__file__])
