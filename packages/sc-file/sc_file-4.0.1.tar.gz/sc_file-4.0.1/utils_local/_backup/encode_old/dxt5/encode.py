import lz4.block  # type: ignore
import struct

def unpack(file, fmt):
    size = struct.calcsize(str(fmt))
    data = file.read(size)
    return struct.unpack(fmt, data)[0]

def pack(fmt, *v):
    return struct.pack(str(fmt), *v)

def xorfourcc(fourcc):
    return bytes(byte ^ ord("g") for byte in fourcc) + b"G"*12

with open("source.dds", "rb") as fp:
    fp.read(12) # skip signature, size and flags

    height = unpack(fp, "I")
    width = unpack(fp, "I")

    fp.read(8) # skip linear_size and depth

    mipmaps_count = unpack(fp, "I")

    fp.read(44) # skip reserved
    fp.read(8) # skip size and flags

    fourcc = unpack(fp, "4s")

    if fourcc == b"\x00\x00\x00\x00":
        raise Exception("Unsupported format")

    fp.read(84) # skip remaining header

    image = fp.read()

with open("output.ol", "wb") as fp:
    fp.write(pack(">I", 0x0A9523FD))
    fp.write(pack(">I", height))
    fp.write(pack(">I", width))
    fp.write(pack(">I", mipmaps_count))
    fp.write(xorfourcc(fourcc))
    fp.write(lz4.block.compress(image, store_size=True))
