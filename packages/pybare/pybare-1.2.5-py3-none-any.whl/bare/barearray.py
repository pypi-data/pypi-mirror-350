from __future__ import annotations
import io
from collections import UserList
from typing import (
    Any,
    BinaryIO,
    ClassVar,
    Generic,
    Iterable,
    Optional,
    Type,
    TypeVar,
    _ProtocolMeta,
)

from .baretype import BAREType
from .number import UInt

T = TypeVar("T")
A = TypeVar("A", bound=BAREType)


__all__ = ["Array", "array"]


class ArrayMeta(_ProtocolMeta, type):
    def __new__(
        cls,
        name,
        bases,
        namespace,
        *,
        inner: Type[BAREType[Any]] | None = None,
        size: Optional[int] = None,
    ):
        inner_type = inner or namespace.get("_type", None)
        if inner_type is None and name != "Array":
            raise TypeError("Array must have an inner type")
        namespace["_type"] = inner_type
        if size is None and name != "Array":
            size = namespace.get("_size", None)
        namespace["_size"] = size
        namespace["value"] = ArrayValidator(inner_type, size)
        return super().__new__(cls, name, bases, namespace)


class ArrayValidator(Generic[T, A]):
    ty: Type[A]
    size: int | None

    def __init__(self, ty: Type[A], size: int | None = None):
        self.ty = ty
        self.size = size

    def __get__(self, inst, _objtype=None) -> list[T] | Type[BAREType[A]]:
        if inst is None:
            return self.ty
        return getattr(inst, "_inner")

    def __set__(self, inst, value: Iterable[T]):
        _value = []
        for v in value:
            if not self.ty.validate(v):
                breakpoint()
                raise TypeError(
                    f"type {type(v)} is invalid for field of BARE type {self.ty}"
                )
            if not isinstance(v, self.ty):
                _value.append(self.ty(v))  # type: ignore
            else:
                _value.append(v)  # type: ignore
        if self.size and len(_value) != self.size:
            raise ValueError(
                f"Array size mismatch. Expected {self.size}, got {len(_value)}"
            )
        inst.__dict__["_inner"] = _value


class Array(Generic[T, A], BAREType[T], metaclass=ArrayMeta):
    """
    A BARE array type. It's inner type must be a BARE type defined in this package and
    must be supplied as a metaclass argument to a subclass of the `Array` class using
    the `inner` kwarg.

    A `size` kwarg may also be specified, which will make the new subclass a fixed-size
    array, which does not encode the length of the array in the serialized data.

    An example that uses both of these:
    ```
    class MyArray(Array, inner=UInt, size=10):
        ...
    ```

    You do *not* need to specify any fields or methods on the subclass, though you may.
    The above class `MyArray` is a fixed size array of 10 `UInt` values.
    """

    _type: ClassVar[Type[BAREType]]
    _size: int | None
    value: list[A]

    def __init__(self, value: Iterable[T | A]):
        inner = []
        for v in value:
            if not isinstance(v, self.__class__._type):
                v = self.__class__._type(v)
            else:
                v = v
            inner.append(v)
        self.value = inner

    def __getitem__(self, key: int):
        return self.value[key]

    def append(self, value: T | A):
        """
        Appends a value to the end of the array. The value is validated against
        the expected type for this `Array`.

        If the `Array` is of fixed-size, appending will result in a `ValueError` being
        raised.

        @value: The value to append to the array
        """
        if self._size and len(self.value) >= self._size:
            raise ValueError("Appending to fixed sized array is unsupported.")
        if not isinstance(value, self.__class__._type):
            # mypy isn't smart enough to tell what type this is
            value = self.__class__._type(value)  # type: ignore
        self.value.append(value)  # type: ignore

    def __iter__(self):
        return iter(self.value)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Array):
            return other.value == self.value
        try:
            values = list(iter(other))
            for other_value, self_value in zip(values, self.value):
                if other_value != self_value:
                    return False
            return True
        except TypeError:
            pass
        return NotImplemented

    def pack(self) -> bytes:
        fp = io.BytesIO()
        if self._size is None:
            fp.write(UInt(len(self._inner)).pack())

        size = self._size or len(self._inner)
        for i in range(size):
            fp.write(self._inner[i].pack())
        return fp.getbuffer()

    @classmethod
    def unpack(cls, fp: BinaryIO) -> Array:
        size = cls._size or UInt.unpack(fp).value
        out = []
        for _ in range(size):
            out.append(cls._type.unpack(fp))
        return cls(out)

    @classmethod
    def validate(cls, value: Iterable[T]) -> bool:
        value = list(value)
        if cls._size:
            if len(value) != cls._size:
                return False
        for v in value:
            if not cls._type.validate(v):
                return False
        return True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self.value)})"


def array(
    inner: Type[BAREType[Any]], size: Optional[int] = None
) -> Type[Array[Any, A]]:
    """
    A function that defines and returns anonymous BARE `Array` subclass with
    the provided `inner` type and (optional) `size` arguments.


    Proper usage of this function is as follows:

    ```
    MyArray = array(UInt, size=10)
    ```

    Note that the name of the class is unspecified, use at your own risk.
    """
    size_name = f"_size_{size}" if size else ""
    name = f"Array_{inner.__name__}{size_name}_anonymous"
    namespace = ArrayMeta.__prepare__(name, (Array,), inner=inner, size=size)
    AnonymousArray = ArrayMeta.__new__(
        ArrayMeta, name, (Array,), namespace, inner=inner, size=size
    )
    ArrayMeta.__init__(AnonymousArray, name, (Array,), namespace)  # type: ignore
    return AnonymousArray
