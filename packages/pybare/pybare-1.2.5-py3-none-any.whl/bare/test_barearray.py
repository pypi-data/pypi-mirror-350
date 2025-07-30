from bare import Array, array, UInt
from bare.baretype import BAREType
from typing import Type
import bare
import pytest
import io

__all__ = []


def test_2d_array_unsized():
    class InnerArray(Array, inner=UInt):
        ...

    class My2DArray(Array, inner=InnerArray):
        ...

    input = [[1, 2], [3, 4]]
    x = My2DArray(input)
    b = x.pack()
    x2 = My2DArray.unpack(io.BytesIO(b))
    assert x2 == x
    assert x2 == input


def test_anonymous_array_unsized():
    AnonymousArray = array(UInt)
    input = [1, 2, 3]
    x = AnonymousArray(input)
    b = x.pack()
    x2 = AnonymousArray.unpack(io.BytesIO(b))
    assert x2 == x
    assert x2 == input


def test_anonymous_array_sized():
    AnonymousArray = array(UInt, 3)
    input = [1, 2, 3]
    x = AnonymousArray(input)
    b = x.pack()
    x2 = AnonymousArray.unpack(io.BytesIO(b))
    assert x2 == x
    assert x2 == input
    with pytest.raises(ValueError):
        x.value = [1, 2, 3, 4]

    with pytest.raises(ValueError):
        AnonymousArray([1, 2, 3, 4])


def test_array_sized():
    class MyArry(Array, inner=UInt, size=3):
        ...

    input = [1, 2, 3]
    x = MyArry(input)
    b = x.pack()
    x2 = MyArry.unpack(io.BytesIO(b))
    assert x2 == x
    assert x2 == input
    with pytest.raises(ValueError):
        x.value = [1, 2, 3, 4]
    with pytest.raises(ValueError):
        MyArry([1, 2, 3, 4])


@pytest.mark.parametrize(
    "inner,data",
    [
        (bare.I8, [1, -1]),
        (bare.U8, [1, 5]),
        (bare.I16, [-1, 10000]),
        (bare.U16, [1, 100]),
        (bare.I32, [1, 100]),
        (bare.U32, [1, 100]),
        (bare.I64, [1, 100]),
        (bare.U64, [1, 100]),
        (bare.F32, [1.0, 2.0]),
        (bare.F64, [1.1, 2.2]),
        (bare.UInt, [1, 2, 3]),
        (bare.Int, [-1, 2, -3]),
        (bare.Str, ["Hello", "world"]),
        (bare.Bool, [False, True]),
        (bare.map(bare.Str, bare.Str), [{"Hello": "world"}, {"abc": "123"}]),
        (bare.union(bare.Str, bare.UInt), [bare.Str("hello"), bare.UInt(123)]),
    ],
)
def test_all_types(inner: Type[BAREType], data: list):
    anon_array = array(inner)
    x = anon_array(data)
    b = x.pack()
    x2 = anon_array.unpack(io.BytesIO(b))
    assert x == x2
