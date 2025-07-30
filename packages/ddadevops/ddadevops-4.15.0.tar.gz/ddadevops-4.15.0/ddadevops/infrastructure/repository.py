from pathlib import Path
from ..domain.common import Devops
from ..domain.build_file import BuildFile


class DevopsRepository:
    def get_devops(self, project) -> Devops:
        devops = project.get_property("devops")
        devops.throw_if_invalid()
        return devops

    def set_devops(self, project, devops: Devops):
        devops.throw_if_invalid()
        project.set_property("devops", devops)


class BuildFileRepository:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)

    def get(self, path: Path) -> BuildFile:
        with open(self.base_dir.joinpath(path), "r", encoding="utf-8") as file:
            content = file.read()
        result = BuildFile(path, content)
        result.throw_if_invalid()
        return result

    def write(self, build_file: BuildFile):
        build_file.throw_if_invalid()
        with open(
            self.base_dir.joinpath(build_file.file_path),
            "r+",
            encoding="utf-8",
        ) as file:
            file.seek(0)
            file.write(build_file.content)
            file.truncate()
