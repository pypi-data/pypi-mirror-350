from .domain import BuildType
from .application import ImageBuildService
from .devops_build import DevopsBuild


class DevopsImageBuild(DevopsBuild):
    def __init__(self, project, inp: dict):
        super().__init__(project, inp)
        self.image_build_service = ImageBuildService.prod()
        devops = self.devops_repo.get_devops(self.project)
        if BuildType.IMAGE not in devops.specialized_builds:
            raise ValueError("ImageBuild requires BuildType.IMAGE")

    def initialize_build_dir(self):
        super().initialize_build_dir()
        devops = self.devops_repo.get_devops(self.project)
        self.image_build_service.initialize_build_dir(devops)

    def image(self):
        devops = self.devops_repo.get_devops(self.project)
        self.image_build_service.image(devops)

    def drun(self):
        devops = self.devops_repo.get_devops(self.project)
        self.image_build_service.drun(devops)

    def dockerhub_login(self):
        devops = self.devops_repo.get_devops(self.project)
        self.image_build_service.dockerhub_login(devops)

    def dockerhub_publish(self):
        devops = self.devops_repo.get_devops(self.project)
        self.image_build_service.dockerhub_publish(devops)

    def test(self):
        devops = self.devops_repo.get_devops(self.project)
        self.image_build_service.test(devops)
