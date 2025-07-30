import io
import bare
import pytest

__all__ = []


@pytest.mark.parametrize(
    "type_, good_values, bad_values",
    [
        (bare.UInt, [0, 1, 2**64 - 1], [-1, 2**64, 2**64 + 1]),
        (
            bare.Int,
            [-(2**63), -(2**63) + 1, 0, 2**63, 2**63 - 1],
            [-(2**63) - 1, 2**63 + 1],
        ),
        (bare.U8, [0, 1, 2**8 - 1], [-1, 2**8]),
        (bare.I8, [-(2**7), 0, 2**7 - 1], [-(2**7) - 1, 2**7]),
        (bare.U16, [0, 1, 2**16 - 1], [-1, 2**16]),
        (bare.I16, [-(2**15), 0, 2**15 - 1], [-(2**15) - 1, 2**15]),
        (bare.U32, [0, 1, 2**32 - 1], [-1, 2**32]),
        (bare.I32, [-(2**31), 0, 2**31 - 1], [-(2**31) - 1, 2**31]),
        (bare.U64, [0, 1, 2**64 - 1], [-1, 2**64]),
        (bare.I64, [-(2**63), 0, 2**63 - 1], [-(2**63) - 1, 2**63]),
    ],
)
def test_bounds(type_, good_values, bad_values):
    for value in good_values:
        x = type_(value)
        b = x.pack()
        x2 = type_.unpack(io.BytesIO(b))
        assert x == x2
    for value in bad_values:
        with pytest.raises(TypeError):
            type_(value)


def test_f32():
    x = bare.F32(123.5)
    b = x.pack()
    assert len(b) == 4
    x2 = bare.F32.unpack(io.BytesIO(b))
    assert x == x2


def test_f64():
    x = bare.F64(123.5)
    b = x.pack()
    assert len(b) == 8
    x2 = bare.F64.unpack(io.BytesIO(b))
    assert x == x2
