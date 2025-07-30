from bare import map, Map, Str, Int
import bare
import io

import pytest

__all__ = []


class MyMap(Map, key_type=Str, value_type=Int):
    ...


def test_basic_map():
    x = MyMap({"Hello": 123, "abc": 456})
    b = x.pack()
    x2 = MyMap.unpack(io.BytesIO(b))
    assert x == x2
    assert x["Hello"] == 123
    assert x["abc"] == 456


def test_anonymous_map():
    MyMap = map(Str, Int)
    x = MyMap({"Hello": 123, "abc": 456})
    b = x.pack()
    x2 = MyMap.unpack(io.BytesIO(b))
    assert x == x2
    assert x["Hello"] == 123
    assert x["abc"] == 456


def test_nested_map():
    InnerMap = map(Str, Str)

    class NestedMap(Map, key_type=Str, value_type=InnerMap):
        ...

    x = NestedMap({"outer": {"hello": "world"}})
    b = x.pack()
    x2 = NestedMap.unpack(io.BytesIO(b))
    assert x == x2


class MyEnum(bare.Enum):
    A = 1
    B = 2


@pytest.mark.parametrize(
    "key_type,value_type,data",
    [
        (Str, Str, {"hello": "world"}),
        (bare.UInt, bare.Int, {123: -123}),
        (bare.U8, bare.U8, {1: 2}),
        (bare.I8, bare.I8, {1: -2}),
        (bare.U16, bare.U16, {1: 2}),
        (bare.I16, bare.I16, {1: -2}),
        (bare.U32, bare.U32, {1: 2}),
        (bare.I32, bare.I32, {1: -2}),
        (bare.U64, bare.U64, {1: 2}),
        (bare.I64, bare.I64, {1: -2}),
        (bare.UInt, bare.UInt, {1: 2}),
        (bare.Int, bare.Int, {1: -2}),
        (bare.Bool, bare.Bool, {True: False}),
        (bare.Bool, bare.Bool, {True: False}),
    ],
)
def test_all_types(key_type, value_type, data):
    anon_map = map(key_type, value_type)
    x = anon_map(data)
    b = x.pack()
    x2 = anon_map.unpack(io.BytesIO(b))
    assert x == x2
