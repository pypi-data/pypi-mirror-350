from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from utils.unpack import generator

from scfile.cli.commands import convert_source_file


def main(assets: Path, output: Path) -> None:
    with ThreadPoolExecutor() as executor:
        for src, dest in generator.assets(assets, output):
            executor.submit(convert_source_file, src, dest)
