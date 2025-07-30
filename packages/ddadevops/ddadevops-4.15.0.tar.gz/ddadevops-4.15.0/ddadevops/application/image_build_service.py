from pathlib import Path
from ..domain import Devops, BuildType
from ..infrastructure import FileApi, ResourceApi, ImageApi


class ImageBuildService:
    def __init__(
        self, file_api: FileApi, resource_api: ResourceApi, image_api: ImageApi
    ):
        self.file_api = file_api
        self.resource_api = resource_api
        self.image_api = image_api

    @classmethod
    def prod(cls):
        return cls(
            FileApi(),
            ResourceApi(),
            ImageApi(),
        )

    def __copy_build_resource_file_from_package__(self, resource_name, devops: Devops):
        data = self.resource_api.read_resource(
            f"src/main/resources/docker/{resource_name}"
        )
        self.file_api.write_data_to_file(
            Path(f"{devops.build_path()}/{resource_name}"), data
        )

    def __copy_build_resources_from_package__(self, devops: Devops):
        self.__copy_build_resource_file_from_package__(
            "image/resources/install_functions.sh", devops
        )
        self.__copy_build_resource_file_from_package__(
            "image/resources/install_functions_debian.sh", devops
        )
        self.__copy_build_resource_file_from_package__(
            "image/resources/install_functions_alpine.sh", devops
        )

    def __copy_build_resources_from_dir__(self, devops: Devops):
        image = devops.specialized_builds[BuildType.IMAGE]
        self.file_api.cp_force(image.build_commons_path(), devops.build_path())

    def initialize_build_dir(self, devops: Devops):
        image = devops.specialized_builds[BuildType.IMAGE]
        build_path = devops.build_path()
        self.file_api.clean_dir(f"{build_path}/image/resources")
        if image.image_use_package_common_files:
            self.__copy_build_resources_from_package__(devops)
        else:
            self.__copy_build_resources_from_dir__(devops)
        self.file_api.cp_recursive("image", build_path)
        try:
            self.file_api.cp_recursive("test", build_path)
        except:
            print("Folder 'test' not found")

    def image(self, devops: Devops):
        image = devops.specialized_builds[BuildType.IMAGE]
        self.image_api.image(image.image_name(), devops.build_path())

    def drun(self, devops: Devops):
        image = devops.specialized_builds[BuildType.IMAGE]
        self.image_api.drun(image.image_name())

    def dockerhub_login(self, devops: Devops):
        image = devops.specialized_builds[BuildType.IMAGE]
        self.image_api.dockerhub_login(
            image.image_dockerhub_user, image.image_dockerhub_password
        )

    def dockerhub_publish(self, devops: Devops):
        image = devops.specialized_builds[BuildType.IMAGE]
        if image.image_tag is not None:
            self.image_api.dockerhub_publish(
                image.image_name(), image.image_dockerhub_user, image.image_tag
            )
        self.image_api.dockerhub_publish(
            image.image_name(), image.image_dockerhub_user, 'latest'
        )

    def test(self, devops: Devops):
        image = devops.specialized_builds[BuildType.IMAGE]
        self.image_api.test(image.image_name(), devops.build_path())
