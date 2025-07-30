from pathlib import Path

from utils_local.stats import Parser, consts


def get_path():
    return Path(input("Enter path to assets:") or consts.DEFAULT_TARGET)


def start_parse(parser: type[Parser]) -> None:
    try:
        path = get_path()
        print(path, "\n")

    except Exception as err:
        print(err)

    else:
        parser(path).start()
