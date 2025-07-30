from pathlib import Path
from typing import Optional

from scfile.file import OlDecoder
from utils_local.stats import Parser, Table

from .tables import ERRORS, TEXTUTES


class TexturesParser(Parser):
    @property
    def tables(self) -> list[Table]:
        return [TEXTUTES, ERRORS]

    def decode(self, path: Path) -> Optional[OlDecoder]:
        try:
            with OlDecoder(path) as decoder:
                decoder.decode()

        except Exception as err:
            ERRORS.writer.writerow([self.get_directory(path), path.stem, err])
            pass

        else:
            return decoder

    def parse(self) -> None:
        for path in Path(self.target).rglob("*.ol"):
            decoder = self.decode(path)

            if not decoder:
                continue

            self.add_texture(path, decoder)

    def add_texture(self, path: Path, decoder: OlDecoder) -> None:
        if not decoder.data:
            return

        directory = self.get_directory(path)

        TEXTUTES.writer.writerow(
            [
                directory,
                path.stem,
                decoder.filesize,
                decoder.fourcc.decode(errors="replace"),
                decoder.width,
                decoder.height,
                decoder.mipmap_count,
                decoder.texture_id.decode(),
            ]
        )
