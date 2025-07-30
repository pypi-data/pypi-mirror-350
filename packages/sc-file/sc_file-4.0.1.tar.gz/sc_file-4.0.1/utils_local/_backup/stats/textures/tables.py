from utils_local.stats import Table


TEXTUTES = Table(
    "textures",
    "textures",
    [
        "path",
        "filename",
        "filesize",
        "fourcc",
        "width",
        "height",
        "mipmap_count",
        "texture_id",
    ],
)

ERRORS = Table(
    "textures",
    "errors",
    [
        "path",
        "filename",
        "error",
    ],
)
