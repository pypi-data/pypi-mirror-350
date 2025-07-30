from pathlib import Path
from typing import Optional

from scfile.file import McsaDecoder
from scfile.utils.model import Model
from utils_local.stats import Parser, Table

from .tables import ERRORS, MESHES, MODELS, SKELETONS


class ModelsParser(Parser):
    @property
    def tables(self) -> list[Table]:
        return [MODELS, MESHES, SKELETONS, ERRORS]

    def decode(self, path: Path) -> Optional[McsaDecoder]:
        try:
            with McsaDecoder(path) as decoder:
                decoder.decode()

        except Exception as err:
            ERRORS.writer.writerow([self.get_directory(path), path.stem, err])
            pass

        else:
            return decoder

    def parse(self) -> None:
        for path in Path(self.target).rglob("*.mcsa"):
            decoder = self.decode(path)

            if not decoder:
                continue

            self.add_model(path, decoder)

    def add_model(self, path: Path, decoder: McsaDecoder) -> None:
        if not decoder.data:
            return

        directory = self.get_directory(path)

        model = decoder.data.model
        model.ensure_unique_names()

        MODELS.writer.writerow(
            [
                directory,
                path.stem,
                decoder.filesize,
                decoder.version,
                decoder.meshes_count,
                model.total_vertices,
                model.total_polygons,
                model.flags.skeleton,
                model.flags.texture,
                model.flags.normals,
                model.scale.position,
                model.scale.texture,
                model.scale.normals,
            ]
        )

        self.add_meshes(path, decoder, directory, model)

        if model.flags.skeleton:
            self.add_skeleton(path, decoder, directory, model)

    def add_meshes(self, path: Path, decoder: McsaDecoder, directory: str, model: Model) -> None:
        for mesh in model.meshes:
            MESHES.writer.writerow(
                [
                    directory,
                    path.stem,
                    decoder.version,
                    mesh.name,
                    mesh.material,
                    mesh.count.vertices,
                    mesh.count.polygons,
                ]
            )

    def add_skeleton(self, path: Path, decoder: McsaDecoder, directory: str, model: Model) -> None:
        names = ", ".join([bone.name for bone in model.skeleton.bones])

        SKELETONS.writer.writerow([directory, path.stem, decoder.version, len(model.skeleton.bones), names])
