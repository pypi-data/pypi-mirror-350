from pathlib import Path

from utils.unpack import generator

from scfile.cli.commands import convert_source_file


def main(assets: Path, output: Path) -> None:
    for src, dest in generator.assets(assets, output):
        convert_source_file(src, dest)
