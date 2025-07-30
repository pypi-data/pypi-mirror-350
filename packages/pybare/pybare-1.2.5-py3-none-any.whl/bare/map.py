from __future__ import annotations

import io
from typing import Any, BinaryIO, Mapping, Type, TypeVar, _ProtocolMeta

from .baretype import BAREType
from .number import UInt

K = TypeVar("K")
V = TypeVar("V")
D = BAREType[Mapping[K, V]]

__all__ = ["Map", "map"]


class MapMeta(_ProtocolMeta, type):
    _key_type: Any
    _value_type: Any

    def __new__(
        cls,
        name,
        bases,
        namespace,
        key_type: type[BAREType[K]] | None = None,
        value_type: type[BAREType[V]] | None = None,
    ):
        key_type = key_type or namespace.get("_key_type", None)
        if key_type is None and name != "Map":
            raise TypeError("Map must have a key_type type specified.")
        value_type = value_type or namespace.get("_value_type", None)
        if value_type is None and name != "Map":
            raise TypeError("Map must have a value_type type specified.")
        namespace["_key_type"] = key_type
        namespace["_value_type"] = value_type
        return super().__new__(cls, name, bases, namespace)


class Map(BAREType[dict[K, V]], metaclass=MapMeta):
    """
    A BARE map type. The type used for keys is declared using the `key_type` metaclass kwarg,
    and the type used for values is declared using the `value_type` metaclass kwarg.

    An example:

    ```
    class MyMap(Map, key_type=UInt, value_type=Str):
        ...
    ```

    `Map` implements a dict-like interface and may be used as such. Both the types of
    keys and values are validated against their BARE types `validate` class method.

    All keys and values are normalized to their BARE type wrappers.
    """

    _values: dict

    def __init__(self, initial_values: Mapping[K, V]):
        self._values = {}
        for key, value in initial_values.items():
            if not isinstance(key, self._key_type):
                key = self._key_type(key)
            if not isinstance(value, self._value_type):
                value = self._value_type(value)
            self[key] = value

    def __getitem__(self, key):
        if not isinstance(key, self._key_type):
            key = self._key_type(key)
        return self._values[key].value

    def __setitem__(self, key, value):
        if not isinstance(key, self._key_type):
            key = self._key_type(key)
        if not isinstance(value, self._value_type):
            value = self._value_type(value)
        self._values[key] = value

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            self[k] = v

    def items(self):
        return self._values.items()

    @classmethod
    def validate(cls, value: Mapping) -> bool:
        for key, value in value.items():
            if not cls._key_type.validate(key) or not cls._value_type.validate(value):
                return False
        return True

    def pack(self) -> bytes:
        fp = io.BytesIO()
        fp.write(UInt(len(self._values)).pack())

        for key, value in self._values.items():  # type: ignore
            fp.write(key.pack())
            fp.write(value.pack())
        return fp.getbuffer()

    @classmethod
    def unpack(cls, fp: BinaryIO) -> Map:
        size = UInt.unpack(fp).value
        out = {}
        for _ in range(size):
            key = cls._key_type.unpack(fp)
            value = cls._value_type.unpack(fp)
            out[key] = value
        return cls(out)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Map):
            return other._values == self._values
        try:
            for other_key, other_value in other.values():
                if (
                    other_key not in self._values
                    and self._key_type(other_key) not in self._values
                ):
                    return False
                if other_value != self._values[other_key]:
                    return False
            return True
        except TypeError:
            pass
        return NotImplemented


def map(key_type: type[BAREType[K]], value_type: type[BAREType[V]]) -> Type[Map[K, V]]:
    """
    A function that defines and returns anonymous BARE `Map` subclass with
    the provided `key_type` type and and `value_type` type.


    Proper usage of this function is as follows:
    ```
    MyMap = map(Str, UInt)
    ```
    Note that the name of the class is unspecified and subject to change.
    """
    name = f"Map_{key_type.__name__}_{value_type.__name__}_anonymous"
    namespace = MapMeta.__prepare__(
        name, (Map,), key_type=key_type, value_type=value_type
    )
    AnonymousMap = MapMeta.__new__(
        MapMeta, name, (Map,), namespace, key_type=key_type, value_type=value_type
    )
    MapMeta.__init__(AnonymousMap, name, (Map,), namespace)  # type: ignore
    return AnonymousMap
