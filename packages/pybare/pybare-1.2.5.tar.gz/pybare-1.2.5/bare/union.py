from __future__ import annotations

import io
from typing import Any, BinaryIO, Generic, Iterable, Type, TypeVar

from .misc import Void
from .number import UInt
from .baretype import BAREType

__all__ = ["Union", "UnionVariant", "optional", "union"]


def build_discriminants(variants: tuple[Any, ...]) -> dict[Any, int]:
    discriminants = {}
    disc = 0
    for variant in variants:
        if isinstance(variant, UnionVariant):
            disc = variant.discriminant
            variant = variant.variant
        discriminants[variant] = disc
        disc += 1
    return discriminants


class UnionMeta(type):
    def __new__(cls, clsname, bases, namespace, variants: tuple[Any, ...]):
        variants_map = {}
        # build type -> discriminant map
        discriminants = build_discriminants(variants)
        for ty, discisc in discriminants.items():
            variants_map[discisc] = ty
        namespace["_variants"] = variants_map
        namespace["_discriminants"] = discriminants
        return super().__new__(cls, clsname, bases, namespace)


T = TypeVar("T")


class UnionValidator(Generic[T]):
    def __init__(self, ty: set[type]):
        self.ty = ty

    def __get__(self, inst, _=None) -> T | Iterable[type]:
        if inst is None:
            return tuple(self.ty)
        return inst.__dict__["_inner"]

    def __set__(self, inst, value: T):
        if type(value) not in self.ty:
            union_member_error(type(value), self.ty)
        inst.__dict__["_inner"] = value


class Union(metaclass=UnionMeta, variants=()):
    """
    A validated and tagged BARE Union type. Variants are specified as a tuple of types
    passed as the metaclass kwargs. An explicit discriminant may be specified by
    wrapping the type in a `UnionVariant` object.

    For example:

    ```
    class MyUnion(Union, variants=(Str, Int)):
        ...
    ```

    NOTE: You *must* specify the wrapped BARE type when performing assignments, as the
    underlying type cannot be safely coerced into the BARE type.

    For example:

    ```
    x = MyUnion(Str("test"))  # will work
    x = MyUnion(123)  # will raise a TypeError
    ```

    The wrapped value may be access using `.value`, note that it is not unwrapped
    implicitly (you will always recieve the BARE type wrapper, ex. UInt(123)
    as opposed to 123)
    """

    # TODO: type annotations based on this
    value: Any
    _variants: dict[int, type]
    _discriminants: dict[type, int]

    def __init__(self, value: Any, *_args, **_kwargs):
        self.value = UnionValidator(self._variants)
        if value is None:
            # coerce None to Void for sanity
            value = Void()
        if not self.validate(value):
            union_member_error(value, self._variants.values())
        self.value = value

    def pack(self: Union) -> bytes:
        buf = io.BytesIO()
        ty = type(self.value)
        discriminant = self._type_to_discriminant(ty)
        buf.write(UInt(discriminant).pack())
        buf.write(self.value.pack())

        return buf.getbuffer()

    @classmethod
    def unpack(cls, fp: BinaryIO) -> Union:
        discriminant = UInt.unpack(fp).value
        if discriminant not in cls._variants:
            raise TypeError(
                f"Got unexpected discriminant for {cls.__name__}: {discriminant}"
            )
        ty = cls._variants[discriminant]
        return cls(ty.unpack(fp))

    @classmethod
    def validate(cls, value: Any) -> bool:
        if isinstance(value, cls):
            return True
        return type(value) in cls._variants.values()

    def __eq__(self, other: Any) -> bool:
        if type(other) in self._discriminants:
            return self.value == other
        elif isinstance(other, self.__class__):
            return other.value == self.value
        for ty in self._variants.values():
            if ty.validate(other):
                return other == ty(other)
        return NotImplemented

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"

    def _type_to_discriminant(self, ty: type) -> int:
        try:
            return self._discriminants[ty]
        except KeyError:
            union_member_error(ty, self._variants.values())
            raise


class UnionVariant(Generic[T]):
    """
    Represents a variant of a union with an explici discriminator.
    Use in any place you would otherwise use a BARE type when defining variants
    of a `Union`

    For example:

    ```
    class MyUnion(Union, variants=(UnionVariant(Str, 3), Int)):
        ...
    ```
    """

    def __init__(self, variant, discriminant: int):
        self.variant = variant
        self.discriminant = discriminant


def union_member_error(t: type, variants: Iterable[type]):
    variants = " | ".join([x.__name__ for x in variants])
    raise TypeError(
        f"Type {t} is not a valid variant for this union. "
        f"Valid options include {variants}"
    )


def union(*variants: tuple[type[BAREType[Any]], ...]) -> type[Union]:
    """
    A function that defines and returns an anonymous Union type. The varargs
    are passed as variants to the Union type.

    The name of the class is undefined.

    For example:

    ```
    MyUnion = union(UnionVariant(Str, 3), Int)
    ```
    """
    name = "Union_anonymous"
    namespace = UnionMeta.__prepare__(name, (), variants=variants)
    AnonymousUnion = UnionMeta.__new__(
        UnionMeta, name, (Union,), namespace, variants=variants
    )
    UnionMeta.__init__(AnonymousUnion, name, (Union,), namespace, variants=variants)  # type: ignore
    return AnonymousUnion


def optional(maybe: Type[T]) -> Type[Union]:
    """
    A simplified version of `union` that implicitly includes a `Void` variant and
    accepts a single type as an argument.

    For example:

    ```
    MyOptional = optional(Str)
    ```

    would be equivalent to:
        class MyOptional(Union, variants=(Void, Str)):
            ...
    """
    name = f"Optional_{maybe.__name__}"
    variants = (
        Void,
        maybe,
    )
    namespace = UnionMeta.__prepare__(name, (), variants=variants)
    AnonymousUnion = UnionMeta.__new__(
        UnionMeta, name, (Union,), namespace, variants=variants
    )
    UnionMeta.__init__(AnonymousUnion, name, (Union,), namespace, variants=variants)
    return AnonymousUnion
