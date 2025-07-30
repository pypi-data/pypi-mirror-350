from pybuilder.core import Project
from .devops_build import DevopsBuild
from .application import ReleaseService
from .domain import MixinType


class ReleaseMixin(DevopsBuild):
    def __init__(self, project: Project, inp: dict):
        super().__init__(project, inp)
        self.release_service = ReleaseService.prod(project.basedir)
        devops = self.devops_repo.get_devops(self.project)
        if MixinType.RELEASE not in devops.mixins:
            raise ValueError("ReleaseMixin requires MixinType.RELEASE")

    def update_release_type(self, release_type_str: str):
        devops = self.devops_repo.get_devops(self.project)
        release = devops.mixins[MixinType.RELEASE]
        self.release_service.update_release_type(release, release_type_str)

    def prepare_release(self):
        devops = self.devops_repo.get_devops(self.project)
        release = devops.mixins[MixinType.RELEASE]
        self.release_service.prepare_release(release)

    def tag_bump_and_push_release(self):
        devops = self.devops_repo.get_devops(self.project)
        release = devops.mixins[MixinType.RELEASE]
        self.release_service.tag_bump_and_push_release(release)

    def publish_artifacts(self):
        devops = self.devops_repo.get_devops(self.project)
        release = devops.mixins[MixinType.RELEASE]
        self.release_service.publish_artifacts(release)
