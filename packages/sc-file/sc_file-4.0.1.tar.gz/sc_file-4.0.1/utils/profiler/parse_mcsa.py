from scfile.formats.mcsa.decoder import McsaDecoder

from .profiler import MODEL_OPTONS, MODEL_PATH, profiler


def decode():
    with McsaDecoder(file=MODEL_PATH, options=MODEL_OPTONS) as mcsa:
        mcsa.decode()


def main():
    profiler(decode)


if __name__ == "__main__":
    main()
