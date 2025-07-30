from __future__ import annotations

import io
from enum import EnumMeta, IntEnum
from typing import Any, BinaryIO

from .baretype import BAREType
from .number import UInt

__all__ = ["Enum", "Void", "Str"]


class Enum(IntEnum, metaclass=EnumMeta):
    """
    A BARE enum type. It is a subclass of `IntEnum` and is used to represent
    a BARE enum type.

    An example:

    ```
    class MyEnum(Enum):
        A = 1
        B = 2
        C = 3

    print(MyEnum.A)  # prints 1
    print(MyEnum.B)  # prints 2
    print(MyEnum.C)  # prints 3

    print(MyEnum.A is MyEnum.B)  # prints False
    print(MyEnum.A == 1)  # prints True
    ```
    """

    def pack(self) -> bytes:
        return UInt(self.value).pack()

    @classmethod
    def unpack(cls, fp: BinaryIO) -> Enum:
        x = UInt.unpack(fp).value
        return cls(x)

    @classmethod
    def validate(cls, value: Any) -> bool:
        if isinstance(value, UInt):
            try:
                cls(value.value)
                return True
            except ValueError:
                return False
        elif isinstance(value, int):
            try:
                cls(value)
                return True
            except ValueError:
                return False
        elif isinstance(value, cls):
            return True
        else:
            return False


class Void(BAREType[None]):
    """
    A Void type. It is similar to the `None` type, but is used to represent
    a BARE void type.

    If should *generally* be used directly, but is also used implicitly in `option`.
    """

    def __init__(self):
        ...

    def pack(self) -> bytes:
        return bytes()

    @classmethod
    def unpack(cls, fp: BinaryIO) -> Void:
        return cls()

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Void):
            return True
        return NotImplemented

    @classmethod
    def validate(cls, value: Any) -> bool:
        return value is None or isinstance(value, Void) or value is Void

    def __hash__(self):
        return hash(self.__class__)


class Str(BAREType[str]):
    """
    A BARE string type.

    It should generally be used directly.

    An example:
    ```
    x = Str("Hello")
    x.pack()  # prints b'\x05Hello'
    Str.unpack(x.pack())  # => Str("Hello")
    ```
    """

    value: str

    def __init__(self, value: str):
        if not self.validate(value):
            raise TypeError(f"Str must wrap a python str. Got {type(value)}")
        if isinstance(value, self.__class__):
            self.value = value.value
        else:
            self.value = value

    def pack(self) -> bytes:
        fp = io.BytesIO()
        encoded = self.value.encode("utf-8")
        fp.write(UInt(len(encoded)).pack())
        fp.write(encoded)
        return fp.getbuffer()

    @classmethod
    def validate(cls, value: str) -> bool:
        return isinstance(value, (str, cls))

    @classmethod
    def unpack(cls, fp: BinaryIO) -> Str:
        size = UInt.unpack(fp).value
        buf = fp.read(size)
        if len(buf) != size:
            raise EOFError
        return cls(buf.decode("utf-8"))

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Str):
            return other.value == self.value
        elif isinstance(other, str):
            return other == self.value
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.__class__)

    def __repr__(self) -> str:
        name = self.__class__.__name__
        return f'{name}("{self.value})"'
