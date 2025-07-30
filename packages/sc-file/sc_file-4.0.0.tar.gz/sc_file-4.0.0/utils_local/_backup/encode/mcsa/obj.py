from scfile.file.base.decoder import FileDecoder
from scfile.file.data.model import ModelData
from scfile.io.streams import BinaryFileIO
from scfile.utils.model.datatypes import Polygon, Vector
from scfile.utils.model.mesh import Mesh, Vertex
from scfile.utils.model.model import Model


class ObjDecoder(FileDecoder[BinaryFileIO, ModelData]):
    @property
    def opener(self) -> type[BinaryFileIO]:
        return BinaryFileIO

    def create_data(self) -> ModelData:
        return ModelData(model=self._parse_model())

    def _parse_model(self) -> Model:
        meshes = []
        current_mesh = Mesh(name="default")

        id_map = {}
        current_id = 0

        while not self.f.seekable():
            line = self.f.readline().strip()
            if line.startswith(b"v "):
                current_mesh.vertices.append(self._parse_vertex(line))

            elif line.startswith(b"f "):
                polygons = self._parse_face(line, id_map, current_id)
                current_mesh.polygons.extend(polygons)
                current_id = max(current_id, max(p.a for p in polygons) + 1)

        meshes.append(current_mesh)
        return Model(meshes=meshes)

    def _parse_vertex(self, line: bytes) -> Vertex:
        x, y, z = line.split()
        position = Vector(float(x), float(y), float(z))
        return Vertex(position=position)

    def _parse_face(self, line: bytes, id_map: dict, current_id: int) -> list[Polygon]:
        parts = line.split()[1:]
        polygons = []

        for part in parts:
            vertex, texture, normal = (int(x) if x else 0 for x in part.split(b"/"))
            triple_key = (vertex, texture, normal)

            if triple_key in id_map:
                polygon_id = id_map[triple_key]
            else:
                polygon_id = current_id
                id_map[triple_key] = polygon_id
                current_id += 1

            polygons.append(Polygon(polygon_id, polygon_id, polygon_id))

        return polygons

    def parse(self) -> None:
        self._data = self.create_data()
