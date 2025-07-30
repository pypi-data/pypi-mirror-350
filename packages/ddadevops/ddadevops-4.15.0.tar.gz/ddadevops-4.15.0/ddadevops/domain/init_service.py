from pathlib import Path
from typing import Dict
from .common import Devops, MixinType, BuildType, ProviderType
from .credentials import CredentialMapping, Credentials, GopassType
from .devops_factory import DevopsFactory
from .terraform import TerraformDomain
from .provider_digitalocean import Digitalocean
from .provider_hetzner import Hetzner
from .c4k import C4k
from .image import Image
from .release import ReleaseType, Release
from ..infrastructure import BuildFileRepository, CredentialsApi, EnvironmentApi, GitApi


class InitService:
    def __init__(
        self,
        devops_factory,
        build_file_repository,
        credentials_api,
        environment_api,
        git_api,
    ):
        self.devops_factory = devops_factory
        self.build_file_repository = build_file_repository
        self.credentials_api = credentials_api
        self.environment_api = environment_api
        self.git_api = git_api

    @classmethod
    def prod(cls, base_dir: str):
        return cls(
            DevopsFactory(),
            BuildFileRepository(base_dir),
            CredentialsApi(),
            EnvironmentApi(),
            GitApi(),
        )

    def initialize(self, inp: dict) -> Devops:
        build_types = self.devops_factory.parse_build_types(
            inp.get("build_types", [])
        )
        mixin_types = self.devops_factory.parse_mixin_types(
            inp.get("mixin_types", [])
        )
        provider_types = TerraformDomain.parse_provider_types(
            inp.get("tf_provider_types", [])
        )

        version = None
        default_mappings = []

        if BuildType.C4K in build_types:
            default_mappings += C4k.get_mapping_default()
        if BuildType.IMAGE in build_types:
            default_mappings += Image.get_mapping_default()
        if BuildType.TERRAFORM in build_types:
            if ProviderType.DIGITALOCEAN in provider_types:
                default_mappings += Digitalocean.get_mapping_default()
            if ProviderType.HETZNER in provider_types:
                default_mappings += Hetzner.get_mapping_default()

        if MixinType.RELEASE in mixin_types:
            primary_build_file_id = inp.get(
                "release_primary_build_file", "./project.clj"
            )
            primary_build_file = self.build_file_repository.get(
                Path(primary_build_file_id)
            )
            version = primary_build_file.get_version()
            default_mappings += Release.get_mapping_default()

        credentials = Credentials(inp, default_mappings)
        authorization = self.authorization(credentials)

        context = self.context(mixin_types, version)

        merged = self.devops_factory.merge(inp, context, authorization)

        return self.devops_factory.build_devops(merged, version=version)

    def context(self, mixin_types, version) -> dict:
        result = {}

        tag = self.environment_api.get("IMAGE_TAG")

        if MixinType.RELEASE in mixin_types:
            release_type = self.environment_api.get("RELEASE_TYPE")
            if not release_type:
                latest_commit = self.git_api.get_latest_commit()
                if latest_commit in [
                    ReleaseType.MAJOR.name,
                    ReleaseType.MINOR.name,
                    ReleaseType.PATCH.name,
                    ReleaseType.NONE.name,
                ]:
                    release_type = latest_commit
            if release_type:
                result["release_type"] = release_type
            result["release_current_branch"] = self.git_api.get_current_branch()

            if not tag:
                tag = version.to_string()

        if tag:
            result["image_tag"] = tag

        return result

    def authorization(self, credentials: Credentials) -> Dict[str, CredentialMapping]:
        result = {}
        for name in credentials.mappings.keys():
            mapping = credentials.mappings[name]
            if self.environment_api.is_defined(mapping.name_for_environment()):
                result[name] = self.environment_api.get(mapping.name_for_environment())
            else:
                if mapping.gopass_type() == GopassType.FIELD:
                    result[name] = self.credentials_api.gopass_field_from_path(
                        mapping.gopass_path, mapping.gopass_field
                    )
                if mapping.gopass_type() == GopassType.PASSWORD:
                    result[name] = self.credentials_api.gopass_password_from_path(
                        mapping.gopass_path
                    )
        return result
