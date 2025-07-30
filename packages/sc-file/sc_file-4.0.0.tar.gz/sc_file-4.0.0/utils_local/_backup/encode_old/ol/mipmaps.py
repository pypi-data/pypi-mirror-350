import struct
import uuid
from pathlib import Path

import lz4.block  # type: ignore


ROOT = Path(__file__).parent.absolute()

PATH_INPUT = ROOT / "input.dds"
PATH_OUTPUT = ROOT / "output.ol"

# random texture id
# stalboy_diff: "90fb3eba776489c531084697de6a8914"
TEXTURE_ID = uuid.uuid4().hex.encode()


def unpack(file, fmt):
    size = struct.calcsize(str(fmt))
    data = file.read(size)
    return struct.unpack(fmt, data)[0]


def pack(fmt, *v):
    return struct.pack(str(fmt), *v)


def xorfourcc(fourcc):
    return bytes(byte ^ ord("g") for byte in fourcc) + b"G" * 12


def calc_mipmap_size(width, height, block_size):
    return max(1, ((width + 3) // 4)) * max(1, ((height + 3) // 4)) * block_size


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

    # read mipmaps (images)
    mipmap_w, mipmap_h = width, height
    mipmaps = []

    uncompressed_sizes = []
    compressed_sizes = []

    for _ in range(mipmaps_count):
        mipmap_size = calc_mipmap_size(mipmap_w, mipmap_h, block_size)  # mipmap size in bytes
        mipmap_data = fp.read(mipmap_size)  # image bytes

        # compress image with lz4
        lz4_data = lz4.block.compress(mipmap_data, store_size=False)

        # add compressed image and sizes to lists
        mipmaps.append(lz4_data)
        uncompressed_sizes.append(mipmap_size)
        compressed_sizes.append(len(lz4_data))

        # recount next mipmap size (width, height)
        mipmap_w = max(1, mipmap_w // 2)
        mipmap_h = max(1, mipmap_h // 2)


# write ol
with open(PATH_OUTPUT, "wb") as fp:
    fp.write(pack(">I", 0x0A9523FD))  # signature
    fp.write(pack(">I", width))
    fp.write(pack(">I", height))
    fp.write(pack(">I", mipmaps_count))
    fp.write(xorfourcc(fourcc))
    fp.write(b"\x00")

    for unsize in uncompressed_sizes:
        fp.write(pack(">I", unsize))

    for compsize in compressed_sizes:
        fp.write(pack(">I", compsize))

    fp.write(pack(">H", len(TEXTURE_ID)))
    fp.write(TEXTURE_ID)

    for mipmap in mipmaps:
        fp.write(mipmap)
