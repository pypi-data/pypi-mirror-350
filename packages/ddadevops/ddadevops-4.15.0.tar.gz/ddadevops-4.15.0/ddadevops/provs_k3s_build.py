from .domain import DnsRecord, BuildType
from .infrastructure import ExecutionApi
from .devops_build import DevopsBuild


class ProvsK3sBuild(DevopsBuild):
    def __init__(self, project, inp):
        super().__init__(project, inp)
        self.execution_api = ExecutionApi()
        devops = self.devops_repo.get_devops(self.project)
        if BuildType.K3S not in devops.specialized_builds:
            raise ValueError("K3SBuild requires BuildType.K3S")

    def update_runtime_config(self, dns_record: DnsRecord):
        super().update_runtime_config(dns_record)
        devops = self.devops_repo.get_devops(self.project)
        devops.specialized_builds[BuildType.K3S].update_runtime_config(dns_record)
        self.devops_repo.set_devops(self.project, devops)

    def write_provs_config(self):
        devops = self.devops_repo.get_devops(self.project)
        k3s = devops.specialized_builds[BuildType.K3S]
        with open(
            self.build_path() + "/out_k3sServerConfig.yaml", "w", encoding="utf-8"
        ) as output_file:
            output_file.write(k3s.provs_config())

    def provs_apply(self, dry_run=False):
        devops = self.devops_repo.get_devops(self.project)
        k3s = devops.specialized_builds[BuildType.K3S]
        self.execution_api.execute_live(k3s.command(devops), dry_run=dry_run)
