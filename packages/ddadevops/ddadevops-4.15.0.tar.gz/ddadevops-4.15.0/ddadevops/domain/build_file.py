import json
import re
from enum import Enum
from typing import Optional
from pathlib import Path
from .common import Validateable
from .version import Version


class BuildFileType(Enum):
    JS = ".json"
    JAVA_GRADLE = ".gradle"
    JAVA_CLOJURE = ".clj"
    JAVA_CLOJURE_EDN = ".edn"
    PYTHON = ".py"


class BuildFile(Validateable):
    def __init__(self, file_path: Path, content: str):
        self.file_path = file_path
        self.content = content

    def validate(self):
        result = []
        result += self.__validate_is_not_empty__("file_path")
        result += self.__validate_is_not_empty__("content")
        if not self.build_file_type():
            result += [f"Suffix {self.file_path} is unknown."]
        return result

    def build_file_type(self) -> Optional[BuildFileType]:
        result: Optional[BuildFileType] = None
        if not self.file_path:
            return result
        config_file_type = self.file_path.suffix
        match config_file_type:
            case ".json":
                result = BuildFileType.JS
            case ".gradle":
                result = BuildFileType.JAVA_GRADLE
            case ".clj":
                result = BuildFileType.JAVA_CLOJURE
            case ".py":
                result = BuildFileType.PYTHON
            case ".edn":
                result = BuildFileType.JAVA_CLOJURE_EDN
            case _:
                result = None
        return result

    def __get_file_type_regex_str(self, file_type: BuildFileType):
        match file_type:
            case BuildFileType.JAVA_GRADLE:
                return r"(?P<pre_version>\bversion\s?=\s?)\"(?P<version>\d*\.\d*\.\d*(-SNAPSHOT)?)\""
            case BuildFileType.PYTHON:
                return r"(?P<pre_version>\bversion\s?=\s?)\"(?P<version>\d*\.\d*\.\d*(-SNAPSHOT|-dev\d*)?)\""
            case BuildFileType.JAVA_CLOJURE:
                return r"(?P<pre_version>\(defproject\s(\S)*\s)\"(?P<version>\d*\.\d*\.\d*(-SNAPSHOT)?)\""
            case BuildFileType.JAVA_CLOJURE_EDN:
                return r"(?P<pre_version>\:version\s+)\"(?P<version>\d*\.\d*\.\d*(-SNAPSHOT)?)\""
            case _:
                return ""

    def get_version(self) -> Version:
        try:
            build_file_type = self.build_file_type()
            match build_file_type:
                case BuildFileType.JS:
                    version_str = json.loads(self.content)["version"]
                case (
                    BuildFileType.JAVA_GRADLE
                    | BuildFileType.PYTHON
                    | BuildFileType.JAVA_CLOJURE
                    | BuildFileType.JAVA_CLOJURE_EDN
                ):
                    version_str = re.search(
                        self.__get_file_type_regex_str(build_file_type), self.content
                    ).group("version")
        except:
            raise RuntimeError(f"Version not found in file {self.file_path}")

        result = Version.from_str(version_str, self.get_default_suffix())
        result.throw_if_invalid()

        return result

    def set_version(self, new_version: Version):

        if new_version.is_snapshot():
            new_version.snapshot_suffix = self.get_default_suffix()

        try:
            build_file_type = self.build_file_type()
            match build_file_type:
                case BuildFileType.JS:
                    json_data = json.loads(self.content)
                    json_data["version"] = new_version.to_string()
                    self.content = json.dumps(json_data, indent=4)
                case (
                    BuildFileType.JAVA_GRADLE
                    | BuildFileType.PYTHON
                    | BuildFileType.JAVA_CLOJURE
                    | BuildFileType.JAVA_CLOJURE_EDN
                ):
                    substitute = re.sub(
                        self.__get_file_type_regex_str(build_file_type),
                        rf'\g<pre_version>"{new_version.to_string()}"',
                        self.content,
                        1,
                    )
                    self.content = substitute
        except:
            raise RuntimeError(f"Version not found in file {self.file_path}")

    def get_default_suffix(self) -> str:
        result = "SNAPSHOT"
        match self.build_file_type():
            case BuildFileType.PYTHON:
                result = "dev"
        return result

    def __eq__(self, other):
        return other and self.file_path == other.file_path

    def __hash__(self) -> int:
        return self.file_path.__hash__()
