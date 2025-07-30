# TODO: fix import structure, structs should be somewhere else
import io
import os

import pytest

from bare import (
    I32,
    I64,
    U8,
    Array,
    Data,
    Enum,
    Field,
    Int,
    Map,
    Str,
    Struct,
    UInt,
    Union,
    Void,
    array,
    data,
    map,
    optional,
    union,
    UnionVariant,
)

__all__ = []


class Nested(Struct):
    s = Field(Str)


class Example(Struct):
    testint = Field(Int)
    teststr = Field(Str)
    testuint = Field(U8)
    n = Field(Nested)
    # m = Field(Map(Str, UInt))


def test_example_struct():
    n = Nested(s="nested")
    ex = Example(testint=11, teststr="a test", n=n)
    assert hasattr(ex, "testint")
    assert hasattr(ex, "teststr")
    assert hasattr(ex, "n")
    assert hasattr(ex.n, "s")
    assert ex.testint == 11
    assert ex.teststr == "a test"
    assert ex.n.s == "nested"
    ex2 = Example(testint=12, teststr="another test")
    assert ex2.testint == 12
    assert ex2.teststr == "another test"
    # Check that the values in the original instance haven't been modified
    assert ex.testint == 11
    assert ex.teststr == "a test"


class C:
    s = Field(Str)


def test_assign_value():
    o = C()
    o.s = "some string"
    assert getattr(o, "s") == "some string"
    # assert isinstance(inspect.getmembers(C)[-1][1], Str)
    assert C.__dict__["s"].ty is Str


class ExampleMapStruct(Struct):
    m = Field(map(Str, Int))
    m2 = Field(map(Int, Str))
    m3 = Field(map(Str, Str))


def test_map():
    ex = ExampleMapStruct(m={}, m2={}, m3={})
    ex.m["test"] = 2
    ex.m2 = {0: "test"}
    ex.m3 = {"test": "test"}
    assert isinstance(ex.m, _ValidatedMap)
    assert isinstance(ex.m2, _ValidatedMap)
    assert isinstance(ex.m3, _ValidatedMap)
    assert ex.m2[0] == "test"
    assert ex.m["test"] == 2
    assert ex.m3["test"] == "test"
    with pytest.raises(ValidationError):
        ex.m2[0] = 0
    with pytest.raises(ValidationError):
        ex.m2 = {"test": "test"}
    with pytest.raises(ValidationError):
        ex.m3["3"] = 3
    map = Map(Str(), Str(), value={"test": "test"})
    assert map.value["test"] == "test"
    map2 = Map(Str, Str)
    map2.value["another"] = "test"
    assert map2.value["another"] == "test"


class MyArray(Array, inner=Int):
    ...


class ArrayTest(Struct):
    a = Field(MyArray)
    n = Field(array(Nested, size=1))


def test_array_struct():
    ex = ArrayTest()
    ex.a = [1, 2, 3]
    ex.n = [Nested(s="test")]
    assert ex.a == [1, 2, 3]
    with pytest.raises(TypeError):
        ex.a = ["a", "b", "c"]
    array(Int).validate([1, 2, -3])


class OptionalStruct(Struct):
    i = Field(Int)
    s = Field(optional(Str))
    nested = Field(optional(Nested))


def test_optional():
    ex = OptionalStruct(i=1, s=Void(), nested=Void())
    assert ex.s == Void()
    assert ex.nested == Void()
    ex.s = Str("test")
    assert ex.s == "test"
    with pytest.raises(TypeError):
        ex.s = 1  # type: ignore
    ex.s = Void()
    assert isinstance(ex.s, Void)

    ex.nested = Nested(s="test")
    assert ex.nested.s == "test"
    with pytest.raises(TypeError):
        ex.nested = "test"


class ExampleUnion(Union, variants=(Str, Int)):
    ...


class UnionTest(Struct):
    e = Field(ExampleUnion)
    b = Field(union(Str, Int))
    c = Field(union(OptionalStruct, ArrayTest))


def test_union():
    ex = UnionTest(
        e=Int(1), b=Str("test"), c=ArrayTest(a=[1], n=[Nested(s="s")])
    )  # MUST specify values for union types when creating an object
    assert ex.e == 1
    ex.e = Str("1")
    assert ex.e == "1"
    with pytest.raises(TypeError):
        ex.e = {"test": "test"}
    b = io.BytesIO(ex.pack())
    ex2 = UnionTest.unpack(b)
    assert ex.e == ex.e
    assert ex.b == ex.b
    assert ex.c.value.a.value == [1]
    assert ex.c.value.n[0].s == "s"
    assert ex.c.value.a.value == [1]


class EnumTest(Enum):
    TEST = 0
    TEST2 = 1


class EnumTestStruct(Struct):
    e = Field(EnumTest)


def test_enum():
    ex = EnumTestStruct(e=0)
    assert ex.e == 0
    with pytest.raises(TypeError):
        ex.e = 100


PublicKey = data(128)


class Time(Str):
    pass


class Department(Enum):
    ACCOUNTING = 0
    ADMINISTRATION = 1
    CUSTOMER_SERVICE = 2
    DEVELOPMENT = 3

    JSMITH = 99


class Address(Struct):
    address = Field(array(Str, size=4))
    city = Field(Str)
    state = Field(Str)
    country = Field(Str)


class Order(Struct):
    orderID = Field(I64)
    quantity = Field(I32)


class Customer(Struct):
    name = Field(Str)
    email = Field(Str)
    address = Field(Address)
    orders = Field(array(Order))
    metadata = Field(map(Str, Data))


class Employee(Struct):
    name = Field(Str)
    email = Field(Str)
    address = Field(Address)
    department = Field(Department)
    hireDate = Field(Time)
    publicKey = Field(optional(PublicKey))
    metadata = Field(map(Str, Data))


class TerminatedEmployee(Void):
    pass


class Person(Union, variants=(Customer, Employee, TerminatedEmployee)):
    ...


@pytest.mark.parametrize(
    "file", ["customer.bin", "employee.bin", "people.bin", "terminated.bin"]
)
def test_people(file):
    with open(os.path.join(os.path.dirname(__file__), "_examples", file), "br") as f:
        people = []
        while True:
            try:
                p = Person.unpack(f)
                people.append(p)
            except RuntimeError:
                break
        f.seek(0)
        f = f.read()
        buf = io.BytesIO()
        for person in people:
            buf.write(person.pack())
        assert buf.getvalue() == f


def test_varint():
    expected = b"\x18"
    i = Int(value=12)
    assert i.pack() == expected

    i = Int(value=12345)
    expected = b"\xf2\xc0\x01"
    assert i.pack() == expected
    i = Int(value=-12345678)
    expected = b"\x9b\x85\xe3\x0b"
    assert i.pack() == expected


def test_uvarint():
    expected = b"\xce\xc2\xf1\x05"
    i = UInt(value=12345678)
    assert i.pack() == expected


def test_string():
    expected = b"\x0d\x61\x20\x74\x65\x73\x74\x20\x73\x74\x72\x69\x6e\x67"
    s = Str(value="a test string")
    assert s.pack() == expected
    s = Str(value="")
    assert s.pack() == b"\x00"


@pytest.mark.parametrize(
    "value",
    [
        (
            Str("a test string"),
            b"\x0d\x61\x20\x74\x65\x73\x74\x20\x73\x74\x72\x69\x6e\x67\x0d\x61\x20\x74\x65\x73\x74\x20\x73\x74\x72\x69\x6e\x67\x0d\x61\x20\x74\x65\x73\x74\x20\x73\x74\x72\x69\x6e\x67\x0d\x61\x20\x74\x65\x73\x74\x20\x73\x74\x72\x69\x6e\x67",
        ),
        (
            Int(12345678),
            b"\x9c\x85\xe3\x0b\x9c\x85\xe3\x0b\x9c\x85\xe3\x0b\x9c\x85\xe3\x0b",
        ),
    ],
)
def test_fixed_array(value):
    a = array(value[0].__class__, size=4)([value[0]] * 4)
    assert a.pack() == value[1]


@pytest.mark.parametrize(
    "value",
    [
        (
            Str("a test string"),
            b"\x04\x0d\x61\x20\x74\x65\x73\x74\x20\x73\x74\x72\x69\x6e\x67\x0d\x61\x20\x74\x65\x73\x74\x20\x73\x74\x72\x69\x6e\x67\x0d\x61\x20\x74\x65\x73\x74\x20\x73\x74\x72\x69\x6e\x67\x0d\x61\x20\x74\x65\x73\x74\x20\x73\x74\x72\x69\x6e\x67",
        ),
        (Int(123456), b"\x04\x80\x89\x0f\x80\x89\x0f\x80\x89\x0f\x80\x89\x0f"),
    ],
)
def test_array(value):
    a = array(value[0].__class__)([value[0]] * 4)
    packed = a.pack()
    assert bytes(a.pack()) == value[1]
    buf = io.BytesIO(packed)
    unpacked = a.unpack(buf)
    assert unpacked == a


class B(Struct):
    c = Field(Int)


class X(Struct):
    a = Field(Str)
    b = Field(B)


def test_struct():
    s = X(a="a test string", b=B(c=12345))
    expected = b"\x0d\x61\x20\x74\x65\x73\x74\x20\x73\x74\x72\x69\x6e\x67\xf2\xc0\x01"
    assert s.pack() == expected
    buf = io.BytesIO(expected)
    unpacked = s.unpack(buf)
    assert unpacked == s


def test_map():
    expected = b"\x02\x04\x74\x65\x73\x74\x04\x74\x65\x73\x74\x07\x61\x6e\x6f\x74\x68\x65\x72\x04\x63\x61\x73\x65"
    anon_map = map(Str, Str)
    m = anon_map({"test": "test", "another": "case"})
    assert m.pack() == expected


def test_union_variant():
    MyUnion = union(UnionVariant(Str, 2), UInt)
    x = MyUnion(Str("hello"))
    fp = io.BytesIO(x.pack())
    assert fp.getbuffer()[0] == 0x2
    y = MyUnion.unpack(fp)
    assert y.value == Str("hello")
