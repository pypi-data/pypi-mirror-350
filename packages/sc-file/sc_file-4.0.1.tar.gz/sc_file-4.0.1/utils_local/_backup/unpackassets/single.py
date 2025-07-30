from pathlib import Path

from rich import print
from utils.unpackassets.conf import ASSETS_PATH, OUTPUT_PATH

from scfile import convert
from scfile.consts import SUPPORTED_SUFFIXES
from scfile.exceptions.base import ScFileException


def get_output_path(path: Path):
    return Path(OUTPUT_PATH, path.relative_to(ASSETS_PATH).parent)


def create_output_dir(path: Path):
    output = get_output_path(path)
    output.mkdir(exist_ok=True, parents=True)
    return output


def convert_one_file(source: Path):
    output = create_output_dir(source)
    try:
        convert.detect(source, output)

    except ScFileException as err:
        print("[b red]ERROR:[/]", err)

    except Exception as err:
        print("[b red]UNKNOWN ERROR:[/]", source.relative_to(ASSETS_PATH), "-", err)


def main():
    for suffix in SUPPORTED_SUFFIXES:
        for path in ASSETS_PATH.rglob(f"**/*.{suffix}"):
            convert_one_file(path)


if __name__ == "__main__":
    main()
