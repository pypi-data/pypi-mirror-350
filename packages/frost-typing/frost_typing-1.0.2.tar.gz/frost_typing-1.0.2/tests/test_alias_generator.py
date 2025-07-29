# -*- coding: utf-8 -*-
import pytest
import typing as tp
import frost_typing as ft


_any_one: tp.Any = 1


def _alias_gen(name: str) -> str:
    return name.title()


@pytest.mark.parametrize(
    "kw_field, alias_generator, kwargs, res",
    [
        ({"auto_alias": False}, _alias_gen, {"a": 1}, {"a": 1},),
        ({"auto_alias": True}, _alias_gen, {_alias_gen("a"): 1}, {_alias_gen("a"): 1}),
        ({"auto_alias": False}, ft.AliasGenerator(alias=_alias_gen), {"a": 1}, {"a": 1}),
        ({"auto_alias": True}, ft.AliasGenerator(alias=_alias_gen), {_alias_gen("a"): 1}, {"a": 1}),
        ({"auto_alias": False}, ft.AliasGenerator(serialization_alias=_alias_gen), {"a": 1}, {"a": 1}),
        ({"auto_alias": True}, ft.AliasGenerator(serialization_alias=_alias_gen), {"a": 1}, {_alias_gen("a"): 1}),
        ({"auto_alias": False}, ft.AliasGenerator(alias=_alias_gen, serialization_alias=_alias_gen), {"a": 1}, {"a": 1}),
        ({"auto_alias": True}, ft.AliasGenerator(alias=_alias_gen, serialization_alias=_alias_gen), {_alias_gen("a"): 1}, {_alias_gen("a"): 1}),
        ({"auto_alias": True, "alias": "test"}, ft.AliasGenerator(alias=_alias_gen, serialization_alias=_alias_gen), {"test": 1}, {_alias_gen("a"): 1}),
        ({"auto_alias": True, "serialization_alias": "test"}, ft.AliasGenerator(alias=_alias_gen, serialization_alias=_alias_gen), {_alias_gen("a"): 1}, {"test": 1}),
        ({"auto_alias": True, "alias": "test", "serialization_alias": "test"}, ft.AliasGenerator(alias=_alias_gen, serialization_alias=_alias_gen), {"test": 1}, {"test": 1}),
    ],
)
def test_auto_alias( kw_field: dict[str, tp.Any], alias_generator: tp.Any, kwargs: dict[str, tp.Any], res: dict[str, tp.Any]) -> None:
    class Model(ft.ValidModel):
        __config__ = ft.Config(alias_generator=alias_generator)
        a: tp.Annotated[int, ft.Field(**kw_field)]
    
    data = Model(**kwargs)
    assert data.as_dict() == res


@pytest.mark.parametrize(
    "alias_generator",
    [
        lambda x: _any_one,                                        # Invalid type
        lambda x: "12ewq",                                         # Invalid format
        lambda x: "Привет",                                        # Invalid format
        ft.AliasGenerator(alias=lambda x: _any_one),               # Invalid type
        ft.AliasGenerator(serialization_alias=lambda x: _any_one)  # Invalid type
    ],
)
def test_alias_generator(alias_generator: tp.Any) -> None:
    with pytest.raises((ValueError, TypeError)):
        class Model(ft.ValidModel):
            __config__ = ft.Config(alias_generator=alias_generator)
            a: int

    
if __name__ == "__main__":
    pytest.main([__file__])