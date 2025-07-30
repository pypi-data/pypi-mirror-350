from concurrent.futures import ThreadPoolExecutor

from utils_local.stats import ModelsParser, TexturesParser
from utils_local.stats.misc import get_path


def main():
    try:
        path = get_path()
        print(path, "\n")

    except Exception as err:
        print(err)

    else:
        with ThreadPoolExecutor() as executor:
            executor.submit(TexturesParser(path).start)
            executor.submit(ModelsParser(path).start)


if __name__ == "__main__":
    main()
