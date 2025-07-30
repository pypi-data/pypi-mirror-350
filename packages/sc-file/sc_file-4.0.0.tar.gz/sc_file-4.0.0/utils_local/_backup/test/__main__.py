from pathlib import Path

from scfile import convert
from scfile.file import McsaDecoder


ROOT = Path(__file__).parent.absolute()


def data(filename: str):
    return ROOT / "data" / filename


def decode(src):
    with McsaDecoder(src) as decoder:
        return decoder.decode()


def main():
    convert.mcsa_to_dae(ROOT / "centurion.mcsa")


if __name__ == "__main__":
    main()
