# PyBARE
[![builds.sr.ht status](https://builds.sr.ht/~chiefnoah/pybare.svg)](https://builds.sr.ht/~chiefnoah/pybare?)
[![Static
Badge](https://img.shields.io/badge/Docs-green?style=flat&logo=python)](https://pybare.ngp.computer)

A declarative implementation of the [BARE](https://baremessages.org/) message
format for Python 3.10+

---

pybare is a general purpose library for strongly typed primitives in Python that
supports serializing to and from BARE messages.

```shell
pip install pybare
```

## Goals

* Provide a declarative structure for defining types
* Validation on value updates
* Support streaming messages

## Status

pybare fully implements all BARE types for both encoding and decoding. This
includes reading multiple messages from the same `BinaryIO` stream.

It is well tested and in use on production systems.

## Gotchas

We use "Array" / "array" instead of "List" / "list" to avoid conflicts with Python's
common builtin type of the same name.

## Examples

An example that defines the types used as an example in the RFC may be found in
[`example.py`](./example.py)

pybare currently requires you define your structures by hand. Examples can be
found in the
[tests](https://git.sr.ht/~chiefnoah/pybare/tree/master/bare/test_encoder.py).

### Quickstart

The general convention is type identifiers start with a *capital* letter and anonymous
generating functions begin with a lowercase. This follows general "pythonic" style for
classes vs functions.

```python
from bare import Struct, map, Str, UInt, optional, data, array, Void, struct, U8

# Alternatively, class Data(size=64): ...
PubKey = data(64) # 512 bits

class User(Struct):
    username = Field(Str)
    userid = Field(Int)
    email = Field(optional(Str))
    keys = Field(map(Str, PubKey))
    repos = Field(array(Str)) # variable length array
    # anonymous array and struct
    friends = Field(array(struct(name=Str, age=U8)))


noah = User(username="chiefnoah", userid=1, email=Void(), keys={}, repos=[], friends=[])
noah.username == 'chiefnoah'
noah.username = 'someoneelse'
noah.username == 'someoneelse'
noah.userid == 1 # True
noah.username = 1 # raise: bare.ValidationError
noah.keys # {} (empty dict)
noah.keys['my key'] = bytes(64) #\x00\x00...
noah.keys['oops'] = bytes(1) # raise: bare.ValidationError
noah.email == Void() # True
noah.email = 12345 # raise: bare.ValidationError
noah.pack() # \x00\x01 ... (binary data)
```

Note, you **must** wrap the desired type in a `Field` to get its 'magic' behavior.
Class or instance fields that are not wrapped in a `Field` will be ignored by the `pack`
and `unpack` methods.

---

To contribute, send patches to [~chiefnoah/inbox@lists.sr.ht](mailto:~chiefnoah/inbox@lists.sr.ht)
