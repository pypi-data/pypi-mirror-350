from __future__ import annotations

import io
import struct
from typing import Any, BinaryIO, Generic, TypeVar

from .baretype import BAREType

T = TypeVar("T")

__all__ = [
    "UInt",
    "Int",
    "F64",
    "F32",
    "U8",
    "Bool",
    "I8",
    "U16",
    "I16",
    "U32",
    "I32",
    "U64",
    "I64",
]


class NumberMixin(Generic[T], BAREType[T]):
    def __init__(self, value: T):
        if not self.__class__.validate(value):  # type: ignore
            raise TypeError(
                f"value {value} is invalid for type {self.__class__.__name__}"
            )
        self.value = value

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, NumberMixin):
            return self.value == other.value
        else:
            return self.value == other

    def __hash__(self) -> int:
        return hash(self.__class__) + hash(self.value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"


class UInt(NumberMixin[int], BAREType[int]):
    """
    An unsigned varint BARE type. When serialized, it encodes itself
    as a LEB128 unsigned varint.

    An example:
    ```
    x = UInt(10)
    x.pack()  # prints b'\x0a'
    fp = io.Bytes(x.pack())
    UInt.unpack(fp)  # => UInt(10)
    ```
    """

    def pack(self) -> bytes:
        buf = io.BytesIO()
        _write_varint(buf, self.value, False)
        return buf.getvalue()

    @classmethod
    def unpack(cls, fp: BinaryIO) -> UInt:
        return cls(_read_varint(fp, False))

    @classmethod
    def validate(cls, value: int) -> bool:
        if isinstance(value, cls):
            return True
        try:
            value = int(value)
            return 0 <= value and value < (1 << 64)
        except (ValueError, TypeError):
            return False

    def __hash__(self):
        return hash(self.__class__)


class Int(NumberMixin[int]):
    """
    An unsigned varint BARE type. When serialized, it encodes itself
    as a LEB128 unsigned varint.

    An example:

    ```
    x = Int(-10)
    x.pack()  # prints b'\x14'
    fp = io.Bytes(x.pack())
    Int.unpack(fp)  # => UInt(-10)
    ```
    """

    def pack(self) -> bytes:
        buf = io.BytesIO()
        _write_varint(buf, self.value, True)
        return buf.getvalue()

    @classmethod
    def unpack(cls, fp: BinaryIO) -> Int:
        return cls(_read_varint(fp, True))

    @classmethod
    def validate(cls, value: int) -> bool:
        if isinstance(value, cls):
            return True
        try:
            value = int(value)
            return -(1 << 63) <= value and value <= (1 << 63)
        except (ValueError, TypeError):
            return False

    def __hash__(self):
        return hash(self.__class__) + hash(self.value)


class F64(NumberMixin[float]):
    """
    A double-precision floating point BARE type.

    An example:
    ```
    x = F64(123.5)
    x.pack()  # prints b'\x00\x00\x00\x00\x00\xe0^@'
    fp = io.Bytes(x.pack())
    F64.unpack(fp)  # => F64(123.5)
    ```
    """

    def pack(self) -> bytes:
        return struct.pack("<d", self.value)

    @classmethod
    def unpack(cls, fp: BinaryIO) -> F64:
        buf = fp.read(struct.calcsize("<d"))
        return cls(struct.unpack("<d", buf)[0])

    @classmethod
    def validate(cls, value: Any) -> bool:
        if isinstance(value, cls):
            return True
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False


class F32(NumberMixin[float]):
    """
    A single-precision floating point BARE type.

    An example:

    ```
    x = F32(123.5)
    x.pack()  # prints b'\x00\x00\xf7B'
    fp = io.Bytes(x.pack())
    F64.unpack(fp)  # => F64(123.5)
    ```
    """

    def pack(self) -> bytes:
        return struct.pack("<f", self.value)

    @classmethod
    def unpack(cls, fp: BinaryIO) -> F32:
        buf = fp.read(struct.calcsize("<f"))
        return cls(struct.unpack("<f", buf)[0])  # type: ignore

    @classmethod
    def validate(cls, value: float) -> bool:
        if isinstance(value, cls):
            return True
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False


class U8(NumberMixin[int]):
    """
    An unsigned 8-bit integer BARE type.
    """

    def pack(self) -> bytes:
        return struct.pack("<B", self.value)

    @classmethod
    def unpack(cls, fp: BinaryIO) -> U8:
        buf = fp.read(struct.calcsize("<B"))
        return cls(struct.unpack("<B", buf)[0])  # type: ignore

    @classmethod
    def validate(cls, value: int) -> bool:
        if isinstance(value, cls):
            return True
        try:
            value = int(value)
            return 0 <= value and value < (1 << 8)
        except (ValueError, TypeError):
            return False


class Bool(NumberMixin[bool]):
    """
    A boolean BARE type, encoded as a single byte.
    """

    def pack(self) -> bytes:
        return struct.pack("<?", self.value)

    @classmethod
    def unpack(cls, fp: BinaryIO) -> Bool:
        buf = fp.read(struct.calcsize("<?"))
        return cls(struct.unpack("<?", buf)[0])  # type: ignore

    @classmethod
    def validate(cls, value: bool) -> bool:
        return isinstance(value, (bool, cls))


class I8(NumberMixin[int]):
    """
    A signed 8-bit integer BARE type.
    """

    def pack(self) -> bytes:
        return struct.pack("<b", self.value)

    @classmethod
    def unpack(cls, fp: BinaryIO) -> I8:
        buf = fp.read(struct.calcsize("<b"))
        return cls(struct.unpack("<b", buf)[0])  # type: ignore

    @classmethod
    def validate(cls, value: int) -> bool:
        if isinstance(value, cls):
            return True
        try:
            value = int(value)
            return -(1 << 7) <= value and value < (1 << 7)
        except (ValueError, TypeError):
            return False


class U16(NumberMixin[int]):
    """
    An unsigned 16-bit integer BARE type.
    """

    def pack(self) -> bytes:
        return struct.pack("<H", self.value)

    @classmethod
    def unpack(cls, fp: BinaryIO) -> U16:
        buf = fp.read(struct.calcsize("<H"))
        return cls(struct.unpack("<H", buf)[0])  # type: ignore

    @classmethod
    def validate(cls, value: int) -> bool:
        if isinstance(value, cls):
            return True
        try:
            value = int(value)
            return 0 <= value and value < (1 << 16)
        except (ValueError, TypeError):
            return False


class I16(NumberMixin[int]):
    """
    A signed 16-bit integer BARE type.
    """

    def pack(self) -> bytes:
        return struct.pack("<h", self.value)

    @classmethod
    def unpack(cls, fp: BinaryIO) -> I16:
        buf = fp.read(struct.calcsize("<h"))
        return cls(struct.unpack("<h", buf)[0])  # type: ignore

    @classmethod
    def validate(cls, value: int) -> bool:
        if isinstance(value, cls):
            return True
        try:
            value = int(value)
            return -(1 << 15) <= value and value < (1 << 15)
        except (ValueError, TypeError):
            return False


class U32(NumberMixin[int]):
    """
    An unnsigned 32-bit integer BARE type.
    """

    def pack(self) -> bytes:
        return struct.pack("<L", self.value)

    @classmethod
    def unpack(cls, fp: BinaryIO) -> U32:
        buf = fp.read(struct.calcsize("<L"))
        return cls(struct.unpack("<L", buf)[0])  # type: ignore

    @classmethod
    def validate(cls, value: int) -> bool:
        if isinstance(value, cls):
            return True
        try:
            value = int(value)
            return 0 <= value and value < (1 << 32)
        except (ValueError, TypeError):
            return False


class I32(NumberMixin[int]):
    """
    A signed 32-bit integer BARE type.
    """

    def pack(self) -> bytes:
        return struct.pack("<l", self.value)

    @classmethod
    def unpack(cls, fp: BinaryIO) -> I32:
        buf = fp.read(struct.calcsize("<l"))
        return cls(struct.unpack("<l", buf)[0])  # type: ignore

    @classmethod
    def validate(cls, value: int) -> bool:
        if isinstance(value, cls):
            return True
        try:
            value = int(value)
            return -(1 << 31) <= value and value < (1 << 31)
        except (ValueError, TypeError):
            return False


class U64(NumberMixin[int]):
    """
    An unsigned 64-bit integer BARE type.
    """

    def pack(self) -> bytes:
        return struct.pack("<Q", self.value)

    @classmethod
    def unpack(cls, fp: BinaryIO) -> U64:
        buf = fp.read(struct.calcsize("<Q"))
        return cls(struct.unpack("<Q", buf)[0])  # type: ignore

    @classmethod
    def validate(cls, value: int) -> bool:
        if isinstance(value, cls):
            return True
        try:
            value = int(value)
            return 0 <= value and value < (1 << 64)
        except (ValueError, TypeError):
            return False

    def __hash__(self):
        return hash(self.__class__)


class I64(NumberMixin[int]):
    """
    A signed 64-bit integer BARE type.
    """

    def pack(self) -> bytes:
        return struct.pack("<q", self.value)

    @classmethod
    def unpack(cls, fp: BinaryIO) -> I64:
        buf = fp.read(struct.calcsize("<q"))
        return cls(struct.unpack("<q", buf)[0])  # type: ignore

    @classmethod
    def validate(cls, value: int) -> bool:
        if isinstance(value, cls):
            return True
        try:
            value = int(value)
            return -(1 << 63) <= value and value < (1 << 63)
        except (ValueError, TypeError):
            return False


# This is adapted from https://git.sr.ht/~martijnbraam/bare-py/tree/master/bare/__init__.py#L29
def _write_varint(fp: BinaryIO, val: int, signed=True) -> int:
    written = 0
    if signed:
        if val < 0:
            val = (2 * abs(val)) - 1
        else:
            val = 2 * val
    while val >= 0x80:
        written += fp.write(struct.pack("<B", (val & 0xFF) | 0x80))
        val >>= 7

    return written + fp.write(struct.pack("<B", val))


def _read_varint(fp: BinaryIO, signed=True) -> int:
    output = 0
    offset = 0
    while True:
        try:
            b = fp.read(1)[0]
        except IndexError:
            raise RuntimeError("Not enough bytes in buffer to decode")
        if b < 0x80:
            value = output | b << offset
            if signed:
                sign = value % 2
                value = value // 2
                if sign:
                    value = -(value + 1)
            return value
        output |= (b & 0x7F) << offset
        offset += 7
