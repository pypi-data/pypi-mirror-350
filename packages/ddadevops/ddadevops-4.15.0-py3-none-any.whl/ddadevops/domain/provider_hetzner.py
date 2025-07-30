from typing import List, Dict, Set, Any
from .common import Validateable, CredentialMappingDefault


class Hetzner(Validateable, CredentialMappingDefault):
    def __init__(
        self,
        inp: dict,
    ):
        self.hetzner_api_key = inp.get("hetzner_api_key")

    def validate(self) -> List[str]:
        result = []
        result += self.__validate_is_not_empty__("hetzner_api_key")
        return result

    def backend_config(self) -> Dict[str, Any]:
        return {}

    def resources_from_package(self) -> Set[str]:
        return {
            "provider_registry.tf",
            "hetzner_provider.tf",
            "hetzner_provider_vars.tf",
        }

    def project_vars(self):
        return {"hetzner_api_key": self.hetzner_api_key}

    def is_local_state(self):
        return True

    @classmethod
    def get_mapping_default(cls) -> List[Dict[str, str]]:
        return []
