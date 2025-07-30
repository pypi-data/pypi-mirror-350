from utils_local.stats import Table


MODELS = Table(
    "models",
    "models",
    [
        "path",
        "filename",
        "filesize",
        "version",
        "meshes_count",
        "total_vertices",
        "total_polygons",
        "flag.skeleton",
        "flag.texture",
        "flag.normals",
        "scale.position",
        "scale.texture",
        "scale.normals",
    ],
)

MESHES = Table(
    "models",
    "meshes",
    [
        "path",
        "filename",
        "model_version",
        "mesh_name",
        "material",
        "vertices",
        "polygons",
    ],
)

SKELETONS = Table(
    "models",
    "skeletons",
    [
        "path",
        "filename",
        "model_version",
        "bones_count",
        "bones_names",
    ],
)

ERRORS = Table(
    "models",
    "errors",
    [
        "path",
        "filename",
        "error",
    ],
)
