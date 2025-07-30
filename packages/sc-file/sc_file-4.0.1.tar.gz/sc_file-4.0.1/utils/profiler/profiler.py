import cProfile
import pstats
from pathlib import Path
from typing import Callable

from scfile.core.context import UserOptions


ROOT = Path(__file__).parent.absolute()
DATA = ROOT / "data"
OUTPUT = ROOT / "out"

TEXTURE_PATH = DATA / "texture.ol"

MODEL_PATH = DATA / "model.mcsa"
MODEL_OPTONS = UserOptions(parse_skeleton=True)


def profiler(func: Callable, *args, **kwargs):
    with cProfile.Profile(subcalls=True, builtins=True) as profile:
        func(*args, **kwargs)

    OUTPUT.mkdir(parents=True, exist_ok=True)

    stats = pstats.Stats(profile)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.reverse_order()
    stats.dump_stats(OUTPUT / "dump.prof")
    stats.print_stats(r"\((?!\_).*\)$")
