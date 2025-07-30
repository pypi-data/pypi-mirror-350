from enum import Enum
from pathlib import Path
from .common import (
    Validateable,
)


class ArtifactType(Enum):
    TEXT = 0
    JAR = 1


class Artifact(Validateable):
    def __init__(self, path: str):
        self.path_str = path

    def path(self) -> Path:
        return Path(self.path_str)

    def type(self) -> str:
        suffix = self.path().suffix
        match suffix:
            case ".jar":
                return "application/x-java-archive"
            case ".js":
                return "application/x-javascript"
            case _:
                return "text/plain"

    def validate(self):
        result = []
        result += self.__validate_is_not_empty__("path_str")
        try:
            Path(self.path_str)
        except Exception as e:
            result += [f"path was not a valid: {e}"]
        return result

    def __str__(self):
        return str(self.path())

    def __eq__(self, other):
        return other and self.__str__() == other.__str__()

    def __hash__(self) -> int:
        return self.__str__().__hash__()
