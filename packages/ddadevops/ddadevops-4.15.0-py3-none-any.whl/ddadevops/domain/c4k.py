from typing import List, Dict, Optional
from .common import (
    Validateable,
    CredentialMappingDefault,
    DnsRecord,
    Devops,
)


class C4k(Validateable, CredentialMappingDefault):
    def __init__(self, inp: dict):
        self.module = inp.get("module")
        self.stage = inp.get("stage")
        self.c4k_executable_name = inp.get("c4k_executable_name", inp.get("module"))
        self.c4k_config = inp.get("c4k_config", {})
        self.c4k_grafana_cloud_url = inp.get(
            "c4k_grafana_cloud_url",
            "https://prometheus-prod-01-eu-west-0.grafana.net/api/prom/push",
        )
        self.c4k_auth = inp.get("c4k_auth", {})
        self.c4k_grafana_cloud_user = inp.get("c4k_grafana_cloud_user")
        self.c4k_grafana_cloud_password = inp.get("c4k_grafana_cloud_password")
        self.dns_record: Optional[DnsRecord] = None

    def update_runtime_config(self, dns_record: DnsRecord):
        self.dns_record = dns_record
        self.throw_if_invalid()

    def validate(self) -> List[str]:
        result = []
        result += self.__validate_is_not_empty__("module")
        result += self.__validate_is_not_empty__("stage")
        result += self.__validate_is_not_empty__("c4k_executable_name")
        result += self.__validate_is_not_empty__("c4k_grafana_cloud_user")
        result += self.__validate_is_not_empty__("c4k_grafana_cloud_password")
        if self.dns_record:
            result += self.dns_record.validate()
        return result

    def config(self):
        if not self.dns_record:
            raise ValueError("dns_reqord was not set.")
        result = self.c4k_config.copy()
        result["fqdn"] = self.dns_record.fqdn
        result["mon-cfg"] = {
            "cluster-name": self.module,
            "cluster-stage": self.stage,
            "grafana-cloud-url": self.c4k_grafana_cloud_url,
        }
        return result

    def auth(self):
        result = self.c4k_auth.copy()
        result["mon-auth"] = {
            "grafana-cloud-user": self.c4k_grafana_cloud_user,
            "grafana-cloud-password": self.c4k_grafana_cloud_password,
        }
        return result

    def command(self, devops: Devops):
        module = devops.module
        build_path = devops.build_path()
        config_path = f"{build_path}/out_c4k_config.yaml"
        auth_path = f"{build_path}/out_c4k_auth.yaml"
        output_path = f"{build_path}/out_{module}.yaml"
        return f"c4k-{self.c4k_executable_name}-standalone.jar {config_path} {auth_path} > {output_path}"

    @classmethod
    def get_mapping_default(cls) -> List[Dict[str, str]]:
        return [
            {
                "gopass_path": "server/meissa/grafana-cloud",
                "gopass_field": "grafana-cloud-user",
                "name": "c4k_grafana_cloud_user",
            },
            {
                "gopass_path": "server/meissa/grafana-cloud",
                "name": "c4k_grafana_cloud_password",
            },
        ]
