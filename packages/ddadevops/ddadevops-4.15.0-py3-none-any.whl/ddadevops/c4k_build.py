from .domain import BuildType, DnsRecord
from .devops_build import DevopsBuild
from .infrastructure import ExecutionApi


class C4kBuild(DevopsBuild):
    def __init__(self, project, config):
        super().__init__(project, config)
        self.execution_api = ExecutionApi()
        devops = self.devops_repo.get_devops(self.project)
        if BuildType.C4K not in devops.specialized_builds:
            raise ValueError("C4kBuild requires BuildType.C4K")

    def update_runtime_config(self, dns_record: DnsRecord):
        super().update_runtime_config(dns_record)
        devops = self.devops_repo.get_devops(self.project)
        devops.specialized_builds[BuildType.C4K].update_runtime_config(dns_record)
        self.devops_repo.set_devops(self.project, devops)

    def write_c4k_config(self):
        devops = self.devops_repo.get_devops(self.project)
        path = devops.build_path() + "/out_c4k_config.yaml"
        self.file_api.write_yaml_to_file(
            path, devops.specialized_builds[BuildType.C4K].config()
        )

    def write_c4k_auth(self):
        devops = self.devops_repo.get_devops(self.project)
        path = devops.build_path() + "/out_c4k_auth.yaml"
        self.file_api.write_yaml_to_file(
            path, devops.specialized_builds[BuildType.C4K].auth()
        )

    def c4k_apply(self, dry_run=False):
        devops = self.devops_repo.get_devops(self.project)
        return self.execution_api.execute(
            devops.specialized_builds[BuildType.C4K].command(devops), dry_run
        )
