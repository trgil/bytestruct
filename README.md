# bytestruct

 ![Author](https://img.shields.io/badge/Author-Gil_Treibush-brightgreen) ![License](https://img.shields.io/badge/License-MIT-blue.svg) ![Version](https://img.shields.io/badge/Version-0.2.0-violet)

**bytestruct** is a lightweight, explicit Python library for parsing and viewing fixed binary layouts (headers, structs, protocol frames) with named field access — without magic or heavy dependencies.

It provides a simple way to:

- Define a binary layout once using plain numbers + clear type names
- Create a class that gives **named attribute access** (`header.file_size`)
- Work with **zero-copy views** over raw bytes via `memoryview`
- Keep full control over the underlying buffer

Inspired by C structs, but stays very Pythonic and minimal.

## Why bytestruct?

Parsing binary data in Python often ends up with manual `struct.unpack()`, slicing, and offset math — which is error-prone and hard to maintain.

**bytestruct** offers a clean middle ground:

- Declarative layout (once per format)
- Readable field access instead of tuple unpacking
- No metaclass magic or runtime surprises
- Zero dependencies beyond the standard library (`struct`, `typing`)

## Installation

(Once you publish it to PyPI — for now just clone & install locally)

```bash
git clone https://github.com/trgil/bytestruct.git
cd bytestruct
pip install -e .
```

---

## Design philosophy

bytestruct is guided by a few core principles:

### Explicit over magical
No metaclass tricks, no hidden mutation, no implicit parsing rules. Every byte has a known offset and size.

### Declarative layouts
Binary formats are *described*, not imperatively parsed. Layouts live at the class level and are immutable once defined.

### Raw bytes are first-class
You always have direct access to the underlying buffer. bytestruct never takes control away from you.

### Struct-compatible thinking
Field definitions map cleanly to Python’s `struct` module. Endianness, size, and alignment behave exactly as expected.

### Lightweight by default
bytestruct is intentionally minimal. Advanced features are added carefully, without turning the library into a framework.

---

## Core concepts

### Fields
A **Field** describes a single region of binary data:

- field name
- binary format (struct-compatible)
- size (derived automatically)
- offset (explicit or auto-computed)

Fields are *metadata only* — they do not store data.

### Binary structures
A **binary structure** combines:

- a class-level layout (fields + offsets)
- an instance-level byte buffer

Instances behave like structured views over raw binary data.

---

## Example

```python
from bytestruct import make_struct_class

BMP_LAYOUT = [
    ("signature",   2, "raw"),         # 2 bytes raw → bytes object
    ("file_size",   4, "uint_le"),     # little-endian unsigned 32-bit int
    ("reserved1",   2, "raw"),
    ("reserved2",   2, "raw"),
    ("data_offset", 4, "uint_le"),
]

BmpHeader = make_struct_class("BmpHeader", BMP_LAYOUT)

# Parse from bytes (e.g. from file)
with open("image.bmp", "rb") as f:
    header_bytes = f.read(54)          # BMP v3 header is typically 54 bytes
    bmp = BmpHeader(header_bytes)

print(bmp.signature)     # b'BM'
print(bmp.file_size)     # e.g. 12345678 (int)
print(bmp.data_offset)   # e.g. 54 (int)

# Also supports index access
print(bmp[0])            # same as bmp.signature
print(bmp[1])            # same as bmp.file_size

# repr is useful for debugging
print(bmp)
# BmpHeader(signature=b'BM', file_size=12345678, reserved1=b'\x00\x00', ...)
```

No unpacking tuples. No manual slicing. No ambiguity.

---

## Intended use cases

bytestruct is well suited for:

- File headers (BMP, WAV, ELF, ZIP, custom formats)
- Binary protocol frames
- Memory-mapped binary data
- Embedded or low-level tooling
- Reverse engineering and format exploration

It is **not** intended to replace:

- Full binary parsing frameworks
- Schema-driven serialization systems
- Bit-level compression codecs

---

## Project status

bytestruct is currently **early-stage and intentionally evolving slowly**. The API is designed with long-term stability in mind, and features are added only when they fit the core philosophy.

Planned areas of future exploration include:

- Nested structures
- Field arrays
- Optional validation hooks
- Safer string decoding helpers
- Better debugging and visualization tools

---

## License

bytestruct is released under the **MIT License**.

You are free to use it in personal, open-source, or commercial projects.
