from typing import Optional, List, Dict
from pathlib import Path
from .common import (
    Validateable,
    ReleaseType,
)
from .version import (
    Version,
)
from .artifact import (
    Artifact,
)


class Release(Validateable):
    def __init__(self, inp: dict, version: Optional[Version]):
        self.release_type = ReleaseType[inp.get("release_type", "NONE")]
        self.release_main_branch = inp.get("release_main_branch", "main")
        self.release_current_branch = inp.get("release_current_branch")
        self.release_primary_build_file = inp.get(
            "release_primary_build_file", "./project.clj"
        )
        self.release_secondary_build_files = inp.get(
            "release_secondary_build_files", []
        )
        self.version = version
        self.release_tag_prefix = inp.get("release_tag_prefix", "")
        self.release_artifact_server_url = inp.get("release_artifact_server_url")
        self.release_organisation = inp.get("release_organisation")
        self.release_repository_name = inp.get("release_repository_name")
        self.release_artifact_token = inp.get("release_artifact_token")
        self.release_artifacts = []
        for a in inp.get("release_artifacts", []):
            self.release_artifacts.append(Artifact(a))

    def update_release_type(self, release_type: ReleaseType):
        self.release_type = release_type

    def validate(self):
        result = []
        result += self.__validate_is_not_empty__("release_type")
        result += self.__validate_is_not_empty__("release_main_branch")
        result += self.__validate_is_not_empty__("release_primary_build_file")
        result += self.__validate_is_not_empty__("version")
        try:
            Path(self.release_primary_build_file)
        except Exception as e:
            result.append(
                f"release_primary_build_file must be a valid path but was {e}"
            )
        for path in self.release_secondary_build_files:
            try:
                Path(path)
            except Exception as e:
                result.append(
                    f"release_secondary_build_file must be contain valid paths but was {e}"
                )
        if self.version:
            result += self.version.validate()
        if self.release_type is not None and self.release_type != ReleaseType.NONE:
            result += self.__validate_is_not_empty__("release_current_branch")
            if (
                self.release_current_branch is not None
                and self.release_type != ReleaseType.NONE
                and self.release_main_branch != self.release_current_branch
            ):
                result.append(
                    f"Releases are allowed only on {self.release_main_branch}"
                )
        return result

    def validate_for_artifact(self):
        result = []
        result += self.__validate_is_not_empty__("release_artifact_server_url")
        result += self.__validate_is_not_empty__("release_organisation")
        result += self.__validate_is_not_empty__("release_repository_name")
        result += self.__validate_is_not_empty__("release_artifact_token")
        return result

    def build_files(self) -> List[str]:
        result = [self.release_primary_build_file]
        result += self.release_secondary_build_files
        return result

    def forgejo_release_api_endpoint(self) -> str:
        validation = self.validate_for_artifact()
        if validation != []:
            raise RuntimeError(f"not valid for creating artifacts: {validation}")

        server_url = self.release_artifact_server_url.removeprefix("/").removesuffix(
            "/"
        )
        organisation = self.release_organisation.removeprefix("/").removesuffix("/")
        repository = self.release_repository_name.removeprefix("/").removesuffix("/")
        return f"{server_url}/api/v1/repos/{organisation}/{repository}/releases"

    def forgejo_release_asset_api_endpoint(self, release_id: int) -> str:
        return f"{self.forgejo_release_api_endpoint()}/{release_id}/assets"

    @classmethod
    def get_mapping_default(cls) -> List[Dict[str, str]]:
        return [
            {
                "gopass_path": "server/meissa/repo/buero-rw",
                "name": "release_artifact_token",
            }
        ]
