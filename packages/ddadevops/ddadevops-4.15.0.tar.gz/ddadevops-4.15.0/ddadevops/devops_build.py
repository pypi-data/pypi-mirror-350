from .domain import InitService, DnsRecord
from .infrastructure import DevopsRepository, FileApi


def get_devops_build(project):
    return project.get_property("build")


class DevopsBuild:
    def __init__(self, project, inp: dict):
        self.project = project
        self.file_api = FileApi()
        self.init_service = InitService.prod(project.basedir)
        self.devops_repo = DevopsRepository()
        devops = self.init_service.initialize(inp)
        self.devops_repo.set_devops(self.project, devops)
        self.project.set_property("build", self)

    def name(self):
        devops = self.devops_repo.get_devops(self.project)
        return devops.name

    def build_path(self):
        devops = self.devops_repo.get_devops(self.project)
        return devops.build_path()

    def initialize_build_dir(self):
        devops = self.devops_repo.get_devops(self.project)
        self.file_api.clean_dir(devops.build_path())

    def update_runtime_config(self, dns_record: DnsRecord):
        pass
