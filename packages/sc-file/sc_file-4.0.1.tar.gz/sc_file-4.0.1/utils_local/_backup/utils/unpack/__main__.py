from pathlib import Path

import click

from utils.unpack import default, multithread
from utils.unpack.consts import DEFAULT


@click.command()
@click.argument(
    "assets",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=DEFAULT.ASSETS,
)
@click.argument(
    "output",
    type=click.Path(file_okay=False, writable=True, path_type=Path),
    default=DEFAULT.OUTPUT,
)
@click.option(
    "--threads/--no-threads",
    default=DEFAULT.MULTITHREAD,
    help="Use multithreaded processing",
)
def main(assets: Path, output: Path, threads: bool):
    if threads:
        multithread.main(assets=assets, output=output)

    else:
        default.main(assets=assets, output=output)


if __name__ == "__main__":
    main()
