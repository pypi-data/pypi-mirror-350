import struct
import uuid
from pathlib import Path

import lz4.block  # type: ignore


ROOT = Path(__file__).parent.absolute()

PATH_INPUT = ROOT / "input.dds"
PATH_OUTPUT = ROOT / "output.ol"

# random texture id
TEXTURE_ID = uuid.uuid4().hex.encode()


def unpack(file, fmt):
    size = struct.calcsize(str(fmt))
    data = file.read(size)
    return struct.unpack(fmt, data)[0]


def pack(fmt, *v):
    return struct.pack(str(fmt), *v)


def xorfourcc(fourcc):
    return bytes(byte ^ ord("g") for byte in fourcc) + b"G" * 12


# read dds
with open(PATH_INPUT, "rb") as fp:
    fp.read(12)  # skip signature, size and flags

    height = unpack(fp, "I")
    width = unpack(fp, "I")

    fp.read(8)  # skip linear_size and depth

    mipmaps_count = unpack(fp, "I")

    fp.read(44)  # skip reserved
    fp.read(8)  # skip size and flags

    fourcc = unpack(fp, "4s")

    fp.seek(128)  # skip remaining header

    match fourcc:
        case b"DXT1":
            block_size = 8
        case b"DXT3" | b"DXT5":
            block_size = 16
        case _:
            raise Exception(f"Format {fourcc} unsupported.")

    # read first mipmap image
    mipmap_size = ((width + 3) // 4) * ((height + 3) // 4) * block_size
    base_image = fp.read(mipmap_size)


# lz4 uncompressed size for first mipmap
uncompressed_size = len(base_image)

# compressed to lz4 block mipmap image
compressed_image = lz4.block.compress(base_image, store_size=False)

# lz4 compressed size for first mipmap
compressed_size = len(compressed_image)

# write ol
with open(PATH_OUTPUT, "wb") as fp:
    fp.write(pack(">I", 0x0A9523FD))  # signature
    fp.write(pack(">I", width))
    fp.write(pack(">I", height))
    fp.write(pack(">I", 1))  # mipmaps count
    fp.write(xorfourcc(fourcc))
    fp.write(b"\x00")
    fp.write(pack(">I", uncompressed_size))
    fp.write(pack(">I", compressed_size))
    fp.write(pack(">H", len(TEXTURE_ID)))
    fp.write(TEXTURE_ID)
    fp.write(compressed_image)
