from __future__ import annotations
import io
from typing import Any, BinaryIO, Optional, Type, TypeVar, _ProtocolMeta

from .baretype import BAREType
from .number import UInt

ByteString = TypeVar("ByteString", bytes, bytearray, memoryview)


class DataMeta(_ProtocolMeta, type):
    def __new__(
        cls,
        name,
        bases,
        namespace,
        *,
        size: Optional[int] = None,
    ):
        if size is None and name != "Data":
            size = namespace.get("_size", None)
        namespace["_size"] = size
        return super().__new__(cls, name, bases, namespace)


class Data(BAREType[bytes], metaclass=DataMeta):
    """
    Represents a BARE data type, which is effectively an alias for an array of u8s.

    As with the `Array` type, a `size` kwarg may be specified to make the new subclass
    a fixed-size data type.

    An example:

    ```
    class MyData(Data, size=10):
        ...
    ```

    """

    _size: Optional[int]

    def __init__(self, value: bytes):
        if self._size and len(value) != self._size:
            raise ValueError(
                f"Bytes was not expected size ({self._size}). Got {len(value)}"
            )
        self.value = value

    def pack(self) -> bytes:
        fp = io.BytesIO()
        if not self._size:
            fp.write(UInt(len(self.value)).pack())
        fp.write(self.value)
        return fp.getbuffer()

    @classmethod
    def validate(cls, value: ByteString) -> bool:
        return isinstance(value, (bytes, bytearray, memoryview))

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    @classmethod
    def unpack(cls, fp: BinaryIO) -> Data:
        size = cls._size or UInt.unpack(fp).value
        buf = fp.read(size)
        return cls(buf)


def data(size: int) -> Type[Data]:
    """
    A function that defines and returns anonymous BARE `Data` subclass with
    the provided `size` argument.

    Proper usage of this function is as follows:

    ```
    MyData = data(10)
    ```
    """
    size_name = f"_size_{size}"
    name = f"Data_{size_name}_anonymous"
    namespace = DataMeta.__prepare__(name, (Data,), size=size)
    AnonymousData = DataMeta.__new__(DataMeta, name, (Data,), namespace, size=size)
    DataMeta.__init__(AnonymousData, name, (Data,), namespace)  # type: ignore
    return AnonymousData
