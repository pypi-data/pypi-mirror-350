from bare import Union, Str, Int, union, UnionVariant
import bare
import io
import pytest

__all__ = []


class MyUnion(Union, variants=(Str, Int)):
    ...


def test_union_basic():
    x = MyUnion(Str("Hello"))
    b = x.pack()
    assert b == b"\x00\x05Hello"
    x2 = MyUnion.unpack(io.BytesIO(b))
    assert x == x2
    with pytest.raises(TypeError):
        x = MyUnion(True)
    with pytest.raises(TypeError):
        MyUnion.unpack(io.BytesIO(b"\x02\x05Hello"))

    x = MyUnion(Int(16))
    b = x.pack()
    assert b == b"\x01\x20"
    x2 = MyUnion.unpack(io.BytesIO(b))
    assert x == x2


def test_anonymous_union():
    MyUnion = union(Str, Int)
    x = MyUnion(Str("Hello"))
    b = x.pack()
    assert b == b"\x00\x05Hello"
    x2 = MyUnion.unpack(io.BytesIO(b))
    assert x == x2
    with pytest.raises(TypeError):
        x = MyUnion(True)


def test_explicit_discriminant_implicit_following():
    class MyUnion(Union, variants=(UnionVariant(Str, 4), Int)):
        ...

    x = MyUnion(Str("Hello"))
    b = x.pack()
    assert b == b"\x04\x05Hello"
    x2 = MyUnion.unpack(io.BytesIO(b))
    assert x == x2
    with pytest.raises(TypeError):
        x = MyUnion(True)
    with pytest.raises(TypeError):
        MyUnion.unpack(io.BytesIO(b"\x02\x05Hello"))

    x = MyUnion(Int(16))
    b = x.pack()
    assert b == b"\x05\x20"
    x2 = MyUnion.unpack(io.BytesIO(b))
    assert x == x2


def test_explicit_discriminant_all_cases():
    class MyUnion(Union, variants=(UnionVariant(Str, 4), UnionVariant(Int, 10))):
        ...

    x = MyUnion(Str("Hello"))
    b = x.pack()
    assert b == b"\x04\x05Hello"
    x2 = MyUnion.unpack(io.BytesIO(b))
    assert x == x2
    with pytest.raises(TypeError):
        x = MyUnion(True)
    with pytest.raises(TypeError):
        MyUnion.unpack(io.BytesIO(b"\x02\x05Hello"))

    x = MyUnion(Int(16))
    b = x.pack()
    assert b == b"\x0a\x20"
    x2 = MyUnion.unpack(io.BytesIO(b))
    assert x == x2


class AllPrimativeTypes(
    Union,
    variants=(
        Str,
        Int,
        bare.UInt,
        bare.Bool,
        bare.F32,
        bare.F64,
        bare.U8,
        bare.I8,
        bare.U16,
        bare.I16,
        bare.U32,
        bare.I32,
        bare.U64,
        bare.I64,
        bare.Data,
        bare.Void,
    ),
):
    ...


@pytest.mark.parametrize(
    "value,discriminant",
    [
        (Str("Hello"), 0),
        (Int(123), 1),
        (bare.UInt(123), 2),
        (bare.Bool(True), 3),
        (bare.F32(123.5), 4),
        (bare.F64(123.5), 5),
        (bare.U8(123), 6),
        (bare.I8(123), 7),
        (bare.U16(123), 8),
        (bare.I16(123), 9),
        (bare.U32(123), 10),
        (bare.I32(123), 11),
        (bare.U64(123), 12),
        (bare.I64(123), 13),
        (bare.Data(b"123"), 14),
        (bare.Void(), 15),
    ],
)
def test_union_all_primative_types(value, discriminant):
    x = AllPrimativeTypes(value)
    b = x.pack()
    assert b[0] == discriminant
    x2 = AllPrimativeTypes.unpack(io.BytesIO(b))
    assert x == x2
