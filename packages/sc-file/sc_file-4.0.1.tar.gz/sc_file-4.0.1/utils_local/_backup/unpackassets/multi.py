from concurrent.futures import ProcessPoolExecutor

from scfile.consts import SUPPORTED_SUFFIXES
from utils.unpackassets.conf import ASSETS_PATH
from utils.unpackassets.single import convert_one_file


def main():
    with ProcessPoolExecutor() as executor:
        for suffix in SUPPORTED_SUFFIXES:
            for path in ASSETS_PATH.rglob(f"**/*.{suffix}"):
                executor.submit(convert_one_file, path)


if __name__ == "__main__":
    main()
