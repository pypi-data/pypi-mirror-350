from pathlib import Path


class PATH:
    EXBO = Path.home() / "AppData" / "Roaming" / "EXBO"
    STALCRAFT = EXBO / "runtime" / "stalcraft"
    ASSETS = STALCRAFT / "modassets" / "assets"


class DEFAULT:
    ASSETS = PATH.ASSETS
    OUTPUT = Path.home() / "scassets.unpacked"
    MULTITHREAD = True
