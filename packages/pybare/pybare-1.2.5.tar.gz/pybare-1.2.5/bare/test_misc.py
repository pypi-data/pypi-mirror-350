import bare
from bare import Enum, UInt, Void, Str
import io
import pytest

__all__ = []


class MyEnum(Enum):
    A = 1
    B = 2


def test_enum_basic():
    b = MyEnum.A.pack()
    a = MyEnum.unpack(io.BytesIO(b))
    assert a is MyEnum.A

    with pytest.raises(ValueError):
        b = UInt(3).pack()
        MyEnum.unpack(io.BytesIO(b))


class MyVoid(Void):
    ...


def test_custom_void():
    x = MyVoid()
    b = x.pack()
    x2 = MyVoid.unpack(io.BytesIO(b))
    assert x == x2
    assert b == b""


def test_void():
    x = Void()
    b = x.pack()
    x2 = Void.unpack(io.BytesIO(b))
    assert x == x2
    assert len(b) == 0


def test_str():
    x = Str("Hello, world")
    b = x.pack()
    x2 = Str.unpack(io.BytesIO(b))
    assert x == x2
    assert b == b"\x0cHello, world"
