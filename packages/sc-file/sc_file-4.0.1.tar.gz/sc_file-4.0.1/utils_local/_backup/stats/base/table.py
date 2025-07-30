import csv
from dataclasses import dataclass
from pathlib import Path

from utils_local.stats import consts


@dataclass
class Table:
    group: str
    name: str
    header: list[str]

    @property
    def filename(self):
        return f"{self.name}.csv"

    @property
    def path(self) -> Path:
        return Path(consts.TABLES_ROOT, self.group, self.filename)

    def open(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.io = open(self.path, "w", newline="", encoding="utf-8")
        self.writer = csv.writer(self.io)

    def close(self):
        self.io.close()

    def add_header(self):
        self.writer.writerow(self.header)
