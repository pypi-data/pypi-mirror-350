from bare import Data, data
import io

__all__ = []


def test_data_sized():
    class SizedData(Data, size=5):
        ...

    x = SizedData(b"12345")
    b = x.pack()
    assert len(b) == 5
    x2 = SizedData.unpack(io.BytesIO(b))
    assert x == x2


def test_data_unsized():
    class SizedData(Data):
        ...

    x = SizedData(b"12345")
    b = x.pack()
    assert len(b) == 6
    x2 = SizedData.unpack(io.BytesIO(b))
    assert x == x2


def test_data_raw():
    x = Data(b"12345")
    b = x.pack()
    assert len(b) == 6
    x2 = Data.unpack(io.BytesIO(b))
    assert x == x2
