import pytest
from bytestruct.core import make_struct_class, ByteStruct


def test_basic_raw_field():
    layout = [
        ("magic", 4, "raw"),
    ]
    MyStruct = make_struct_class("MyStruct", layout)

    data = b"ABCD" + b"extra"
    s = MyStruct(data)

    assert s.magic == b"ABCD"
    assert s[0] == b"ABCD"


def test_uint_le():
    layout = [
        ("value", 4, "uint_le"),
    ]
    NumStruct = make_struct_class("NumStruct", layout)

    # 0x12345678 little-endian → bytes: 78 56 34 12
    data = bytes([0x78, 0x56, 0x34, 0x12])
    s = NumStruct(data)

    assert s.value == 0x12345678
    assert s[0] == 0x12345678


def test_int_be():
    layout = [
        ("signed", 2, "int_be"),
    ]
    SignedStruct = make_struct_class("SignedStruct", layout)

    # -1234 in big-endian 16-bit: 0xFB2E
    data = bytes([0xFB, 0x2E])
    s = SignedStruct(data)

    assert s.signed == -1234


def test_short_data_raises():
    layout = [
        ("a", 4, "raw"),
        ("b", 4, "uint_le"),
    ]
    ShortStruct = make_struct_class("ShortStruct", layout)

    data = b"1234"  # only 4 bytes, need 8
    with pytest.raises(ValueError, match="Data too short"):
        ShortStruct(data)


def test_name_not_found():
    layout = [("hello", 4, "raw")]
    S = make_struct_class("S", layout)
    s = S(b"abcd")

    with pytest.raises(AttributeError):
        _ = s.world


def test_repr_smoke():
    layout = [("sig", 2, "raw"), ("size", 4, "uint_le")]
    S = make_struct_class("S", layout)
    s = S(b"BM" + (123).to_bytes(4, "little"))

    repr_str = repr(s)
    assert "S(" in repr_str
    assert "sig=" in repr_str
    assert "size=" in repr_str
