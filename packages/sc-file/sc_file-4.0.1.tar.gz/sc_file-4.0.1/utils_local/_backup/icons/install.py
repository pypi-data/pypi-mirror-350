import shutil
import winreg
from pathlib import Path


ROOT = Path(__file__).parent.parent.parent.absolute()

SOURCE = ROOT / "assets" / "files"
TARGET = Path.home() / "scfile" / "icons"


ICONS = {
    "anm": "Animation",
    "aabb": "Collider",
    "xeon": "Config",
    "smm": "Config Mobs",
    "ol": "Texture",
    "mic": "Image",
    "mcsa": "Model",
    "mcxd": "Model Material",
    "mcvd": "Model Collider",
    "mcal": "Model Weapon",
    "mcws": "Model Safezone",
    "l": "Container",
    "t": "Container Item",
    "m": "Container Block",
}


def copy_icons():
    TARGET.mkdir(parents=True, exist_ok=True)

    for file in SOURCE.glob("*"):
        shutil.copy(file, TARGET)


def register_icon(extension: str, filename: str):
    try:
        ext_key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, f".{extension}")
        icon_key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, f".{extension}\\DefaultIcon")

    except Exception as err:
        print(f'CreateKey Error for ".{extension}" - {err}')
        return

    try:
        winreg.SetValue(icon_key, "", winreg.REG_SZ, str(TARGET / f"{filename}.ico"))

    except Exception as err:
        print(f'SetValue Error for ".{extension}" - {err}')

    finally:
        winreg.CloseKey(ext_key)
        winreg.CloseKey(icon_key)


def main():
    copy_icons()

    for extension, filename in ICONS.items():
        register_icon(extension, filename)


if __name__ == "__main__":
    main()
