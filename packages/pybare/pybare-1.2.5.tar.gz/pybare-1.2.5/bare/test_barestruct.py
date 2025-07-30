import io
from bare import Struct, UInt, Str, Field, struct

__all__ = []


def test_struct_basic():
    class MyStruct(Struct):
        a = Field(UInt)
        b = Field(Str)
        c: int

    x = MyStruct(a=123, b="Hello")
    b = x.pack()
    x2 = MyStruct.unpack(io.BytesIO(b))
    assert x == x2


def test_nested_struct():
    class InnerStruct(Struct):
        i = Field(UInt)

    class MyStruct(Struct):
        inner = Field(InnerStruct)

    x = MyStruct(inner=InnerStruct(i=123))
    b = x.pack()
    x2 = MyStruct.unpack(io.BytesIO(b))
    assert x == x2


def test_anonymous_struct():
    MyStruct = struct(name=Str, age=UInt)
    x = MyStruct(name="Noah", age=27)
    b = x.pack()
    x2 = MyStruct.unpack(io.BytesIO(b))
    assert x == x2
