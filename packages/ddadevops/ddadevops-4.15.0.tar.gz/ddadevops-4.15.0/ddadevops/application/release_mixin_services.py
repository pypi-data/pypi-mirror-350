import json
from typing import List
from pathlib import Path
from ..infrastructure import GitApi, ArtifactDeploymentApi, BuildFileRepository
from ..domain import Version, Release, ReleaseType, Artifact


class ReleaseService:
    def __init__(
        self,
        git_api: GitApi,
        artifact_deployment_api: ArtifactDeploymentApi,
        build_file_repository: BuildFileRepository,
    ):
        self.git_api = git_api
        self.artifact_deployment_api = artifact_deployment_api
        self.build_file_repository = build_file_repository

    @classmethod
    def prod(cls, base_dir: str):
        return cls(
            GitApi(),
            ArtifactDeploymentApi(),
            BuildFileRepository(base_dir),
        )

    def update_release_type(self, release: Release, release_type_str: str):
        release.update_release_type(ReleaseType[release_type_str])

    def prepare_release(self, release: Release):
        match release.release_type:
            case ReleaseType.MAJOR:
                version = release.version.create_major()
            case ReleaseType.MINOR:
                version = release.version.create_minor()
            case ReleaseType.PATCH:
                version = release.version.create_patch()
            case _:
                return
        message = f"release: {version.to_string()}"
        self.__set_version_and_commit__(version, release.build_files(), message)

    def tag_bump_and_push_release(self, release: Release):
        match release.release_type:
            case ReleaseType.MAJOR:
                release_version = release.version.create_major()
            case ReleaseType.MINOR:
                release_version = release.version.create_minor()
            case ReleaseType.PATCH:
                release_version = release.version.create_patch()
            case _:
                return
        bump_version = release_version.create_bump()
        release_message = f"release: {release_version.to_string()}"
        bump_message = f"bump version to: {bump_version.to_string()}"
        release_tag = f"{release.release_tag_prefix}{release_version.to_string()}"
        self.git_api.tag_annotated(release_tag, release_message, 0)
        self.__set_version_and_commit__(
            bump_version,
            release.build_files(),
            bump_message,
        )
        self.git_api.push_follow_tags()

    def publish_artifacts(self, release: Release):
        token = str(release.release_artifact_token)
        release_id = self.__parse_forgejo_release_id__(
            self.artifact_deployment_api.create_forgejo_release(
                release.forgejo_release_api_endpoint(),
                release.version.to_string(),
                token,
            )
        )

        artifacts_sums = []
        for artifact in release.release_artifacts:
            sha256 = self.artifact_deployment_api.calculate_sha256(artifact.path())
            sha512 = self.artifact_deployment_api.calculate_sha512(artifact.path())
            artifacts_sums += [Artifact(sha256), Artifact(sha512)]

        artifacts = release.release_artifacts + artifacts_sums
        print(artifacts)
        for artifact in artifacts:
            print(str)
            self.artifact_deployment_api.add_asset_to_release(
                release.forgejo_release_asset_api_endpoint(release_id),
                artifact.path(),
                artifact.type(),
                token,
            )

    def __parse_forgejo_release_id__(self, release_response: str) -> int:
        parsed = json.loads(release_response)
        try:
            result = parsed["id"]
        except:
            raise RuntimeError(str(parsed))
        return result

    def __set_version_and_commit__(
        self, version: Version, build_file_ids: List[str], message: str
    ):
        for build_file_id in build_file_ids:
            build_file = self.build_file_repository.get(Path(build_file_id))
            build_file.set_version(version)
            self.build_file_repository.write(build_file)
            self.git_api.add_file(build_file.file_path)
        self.git_api.commit(message)
