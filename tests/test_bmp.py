import pytest
from bytestruct.core import make_struct_class

# Typical BMP v3 header layout (Windows Bitmap, 54 bytes)
BMP_LAYOUT = [
    ("signature",     2, "raw"),         # "BM"
    ("file_size",     4, "uint_le"),
    ("reserved1",     2, "raw"),         # usually 0
    ("reserved2",     2, "raw"),         # usually 0
    ("data_offset",   4, "uint_le"),     # normally 54 for v3
    # BITMAPINFOHEADER starts here
    ("header_size",   4, "uint_le"),     # 40 for v3
    ("width",         4, "int_le"),      # can be negative for top-down
    ("height",        4, "int_le"),
    ("planes",        2, "uint_le"),
    ("bit_count",     2, "uint_le"),
    ("compression",   4, "uint_le"),
    ("image_size",    4, "uint_le"),
    ("x_pixels_per_m",4, "uint_le"),
    ("y_pixels_per_m",4, "uint_le"),
    ("clr_used",      4, "uint_le"),
    ("clr_important", 4, "uint_le"),
]

BmpHeader = make_struct_class("BmpHeader", BMP_LAYOUT)


def test_realistic_bmp_header():
    # Real example bytes from a small uncompressed BMP (54 bytes header)
    # signature BM, file_size 310, offset 54, width 2, height 2, bit_count 24, no compression
    header_bytes = bytes([
        0x42, 0x4D,                         # signature "BM"
        0x36, 0x01, 0x00, 0x00,             # file_size = 310
        0x00, 0x00,                         # reserved1
        0x00, 0x00,                         # reserved2
        0x36, 0x00, 0x00, 0x00,             # data_offset = 54
        0x28, 0x00, 0x00, 0x00,             # header_size = 40
        0x02, 0x00, 0x00, 0x00,             # width = 2
        0x02, 0x00, 0x00, 0x00,             # height = 2
        0x01, 0x00,                         # planes = 1
        0x18, 0x00,                         # bit_count = 24
        0x00, 0x00, 0x00, 0x00,             # compression = 0 (BI_RGB)
        0x00, 0x00, 0x00, 0x00,             # image_size = 0
        0x00, 0x00, 0x00, 0x00,             # x_pixels_per_m = 0
        0x00, 0x00, 0x00, 0x00,             # y_pixels_per_m = 0
        0x00, 0x00, 0x00, 0x00,             # clr_used = 0
        0x00, 0x00, 0x00, 0x00,             # clr_important = 0
    ])

    bmp = BmpHeader(header_bytes)

    # Assertions
    assert bmp.signature == b"BM"
    assert bmp.file_size == 310
    assert bmp.data_offset == 54
    assert bmp.header_size == 40
    assert bmp.width == 2
    assert bmp.height == 2
    assert bmp.planes == 1
    assert bmp.bit_count == 24
    assert bmp.compression == 0
    assert bmp.image_size == 0

    # Check index access too
    assert bmp[0] == b"BM"
    assert bmp[1] == 310
    assert bmp[5] == 40   # header_size

    # repr doesn't crash
    assert "BmpHeader" in repr(bmp)
    assert "signature=b'BM'" in repr(bmp)
    assert "width=2" in repr(bmp)


def test_bmp_from_real_file():
    # Adjust path to your sample image
    bmp_path = "tests/sample.bmp"          # ← put your file here or use absolute path

    with open(bmp_path, "rb") as f:
        header_data = f.read(54)           # BMP v3 header is 54 bytes

    bmp = BmpHeader(header_data)

    assert bmp.signature == b"BM"
    assert bmp.data_offset == 54           # most common value
    assert bmp.bit_count in (1, 4, 8, 16, 24, 32)
    assert bmp.compression in (0, 1, 2, 3)   # BI_RGB, BI_RLE8, etc.
