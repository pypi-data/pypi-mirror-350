from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional

from .table import Table


class Parser(ABC):
    def __init__(self, target: Path, relative: Optional[Path] = None):
        self.target = target
        self.relative = relative or target

        self.open()

    @property
    @abstractmethod
    def tables(self) -> list[Table]:
        pass

    def open(self) -> None:
        for table in self.tables:
            table.open()

    def close(self) -> None:
        for table in self.tables:
            table.close()

    def add_headers(self) -> None:
        for table in self.tables:
            table.add_header()

    @abstractmethod
    def decode(self, path: Path) -> Any:
        pass

    @abstractmethod
    def parse(self) -> None:
        pass

    def get_directory(self, path: Path) -> str:
        return path.relative_to(self.relative).parent.as_posix()

    def start(self):
        self.add_headers()
        self.parse()
        self.close()
