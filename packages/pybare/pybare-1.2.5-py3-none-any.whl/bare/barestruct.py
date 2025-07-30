from __future__ import annotations

import io
from typing import Any, BinaryIO, Dict, Type, TypeVar, _ProtocolMeta

from .baretype import BAREType
from .util import Field

__all__ = ["Struct", "struct"]


T = TypeVar("T")


class StructMeta(_ProtocolMeta, type):
    def __new__(cls, clsname, bases, clsdict):
        fields = {}
        has_fields = False
        for name, attr in clsdict.items():
            if isinstance(attr, Field):
                has_fields = True
                attr.name = name
                attr.attr = f"_{name}"
                fields[name] = attr.ty
        if not has_fields and clsname != "Struct":
            raise TypeError(
                f"Struct class {clsname} does not have any Fields defined. "
                "You must define at least one field"
            )
        clsdict["_fields"] = fields
        return super().__new__(cls, clsname, bases, clsdict)


class Struct(BAREType, metaclass=StructMeta):
    """
    A BARE struct type. Declare fields using the `Field` type. Each field is serialized
    in the same order as declared in the subclass.

    Fields that are not wrapped in a `Field` type will be ignored for
    (de)serierialization.

    An example:

    ```
    class MyStruct(Struct):
        a = Field(UInt)
        b = Field(Str)
        c = Field(map(Str, Int))
    ```

    An `__init__` is generated based on the `Field` declarations. This may be
    overridden, but please remember to call `super().__init__` in your
    implementation.

    Fields may be accessed as normal:
    ```
    my_struct = MyStruct(a=1, b="hello", c={"a": 1, "b": 2})
    print(my_struct.a)  # prints 1
    print(my_struct.b)  # prints "hello"
    print(my_struct.c)  # prints {"a": 1, "b": 2}
    ```

    Assignments will be validated against their BARE types `validate` class method.
    """

    _fields: dict[str, type]

    def __init__(self, **kwargs):
        name = self.__class__.__name__
        for key, value in kwargs.items():
            if key not in self._fields:
                raise ValueError(f"Got unexpected field for Struct {name}: {key}")
            if not isinstance(value, self._fields[key]):
                value = self._fields[key](value)
            setattr(self, key, value)
        missing_fields = set(kwargs.keys()) - set(self._fields.keys())
        if len(missing_fields) > 0:
            raise ValueError(
                f"Missing fields for {name}.__init__. "
                f"Expected: {', '.join(missing_fields)}"
            )

    def pack(self: Struct) -> bytes:
        buf = io.BytesIO()
        for name, ty in self._fields.items():
            val = getattr(self, name)
            # coerce to the wrapped type
            if not isinstance(val, ty):
                val = ty(val)
            buf.write(ty.pack(val))
        return buf.getbuffer()

    @classmethod
    def unpack(cls, fp: BinaryIO) -> Struct:
        fields = {}
        for name, ty in cls._fields.items():
            fields[name] = ty.unpack(fp)
        return cls(**fields)

    @classmethod
    def validate(cls, value: Any) -> bool:
        if not isinstance(value, cls):
            return False
        for name, ty in cls._fields.items():
            if not ty.validate(getattr(value, name)):
                return False
        return True

    def __repr__(self) -> str:
        clsname = self.__class__.__name__
        fields = []
        for name, field in self._fields.items():
            fields.append(f"{name}={getattr(self, name)}")
        return f"{clsname}({', '.join(fields)})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            for name in self._fields.keys():
                if getattr(self, name) != getattr(other, name):
                    return False
            return True
        return NotImplemented


def struct(**kwargs: Type[BAREType]) -> Type[Struct]:
    """
    A function that defines and returnes an anonymous BARE `Struct` subclass with the
    provided `kwargs` as fields. The name of each kwarg becomes the field name, with the
    value being the field type. The field type is implicitly wrapped in a `Field`.Field

    Proper usage of this function is as follows:

    ```
    MyStruct = struct(a=UInt, b=Str)
    ```

    Note that the name of the class is unspecified, use at your own risk.
    """
    name = "Struct_{}_anonymous".format("_".join(kwargs.keys()))
    namespace = StructMeta.__prepare__(name, (Struct,))
    namespace.update({field: Field(ty) for field, ty in kwargs.items()})  # type: ignore
    AnonymousStruct = StructMeta.__new__(StructMeta, name, (Struct,), namespace)
    StructMeta.__init__(AnonymousStruct, name, (Struct,), namespace)
    return AnonymousStruct
