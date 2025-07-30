import cProfile
import pstats
from pathlib import Path

from scfile.core.formats.mcsa.decoder import McsaDecoder
from scfile.core.formats.obj.encoder import ObjEncoder


ROOT = Path(__file__).parent.absolute()


def decode(src: Path):
    with McsaDecoder(src) as decoder:
        return decoder.decode()


def main():
    src = ROOT / "test.mcsa"

    with cProfile.Profile(subcalls=True, builtins=True) as profile:
        with McsaDecoder(src) as decoder:
            data = decoder.decode()

        with ObjEncoder(data) as obj, open("test.obj", "wb") as fp:
            obj.encode()
            fp.write(obj.content())

        # convert.mcsa_to_dae(src, ROOT / "test.dae")
        # convert.mcsa_to_dae(src, ROOT / "test.dae")
        # convert.mcsa_to_obj(src, ROOT / "test.obj")
        # convert.mcsa_to_dae(src, ROOT / "test.dae")
        # convert.mcsa_to_ms3d(src, ROOT / "test.ms3d")
        # convert.mcsa_to_obj(src, ROOT / "test.obj")
        # convert.mcsa_to_ms3d_ascii(src, ROOT / "test.txt")
        pass

    results = pstats.Stats(profile)
    results.sort_stats(pstats.SortKey.TIME)
    results.reverse_order()
    results.dump_stats(ROOT / "dump.prof")
    results.print_stats(r"\((?!\_).*\)$")


if __name__ == "__main__":
    main()
