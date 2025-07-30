from pathlib import Path

from scfile.consts import SUPPORTED_SUFFIXES


def assets(base_assets: Path, base_output: Path):
    for suffix in SUPPORTED_SUFFIXES:
        for path in base_assets.rglob(f"**/*.{suffix}"):
            yield (path, base_output / path.relative_to(base_assets).parent)
