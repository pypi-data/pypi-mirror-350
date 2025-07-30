from typing import List, Dict, Set, Any
from .common import Validateable, CredentialMappingDefault


class Digitalocean(Validateable, CredentialMappingDefault):
    def __init__(
        self,
        inp: dict,
    ):
        self.stage = inp.get("stage")
        self.module = inp.get("module")
        self.do_api_key = inp.get("do_api_key")
        self.do_spaces_access_id = inp.get("do_spaces_access_id")
        self.do_spaces_secret_key = inp.get("do_spaces_secret_key")
        self.do_as_backend = inp.get("do_as_backend", False)
        self.do_account_name = inp.get("do_account_name", self.stage)
        self.do_bucket = inp.get("do_bucket")
        self.do_bucket_key = inp.get("do_bucket_key", self.module)
        self.do_endpoint = inp.get("do_endpoint", "fra1.digitaloceanspaces.com")
        self.do_region = inp.get("do_region", "eu-central-1")

    def validate(self) -> List[str]:
        result = []
        result += self.__validate_is_not_empty__("stage")
        result += self.__validate_is_not_empty__("module")
        result += self.__validate_is_not_empty__("do_api_key")
        result += self.__validate_is_not_empty__("do_spaces_access_id")
        result += self.__validate_is_not_empty__("do_spaces_secret_key")
        result += self.__validate_is_not_empty__("do_spaces_secret_key")
        result += self.__validate_is_not_none__("do_as_backend")
        if self.do_as_backend:
            result += self.__validate_is_not_empty__("do_account_name")
            result += self.__validate_is_not_empty__("do_endpoint")
            result += self.__validate_is_not_empty__("do_bucket")
            result += self.__validate_is_not_empty__("do_region")
        return result

    def backend_config(self) -> Dict[str, Any]:
        result = {}
        if self.do_as_backend:
            result = {
                "access_key": self.do_spaces_access_id,
                "secret_key": self.do_spaces_secret_key,
                "endpoint": self.do_endpoint,
                "bucket": self.do_bucket,
                "key": self.__bucket_key__(),
                "region": self.do_region,
            }
        return result

    def resources_from_package(self) -> Set[str]:
        result = {"provider_registry.tf", "do_provider.tf", "do_provider_vars.tf"}
        if self.do_as_backend:
            result.update(
                {"do_backend_vars.tf", "do_backend.tf"}
            )
        return result

    def project_vars(self):
        result = {
            "do_api_key": self.do_api_key,
            "do_spaces_access_id": self.do_spaces_access_id,
            "do_spaces_secret_key": self.do_spaces_secret_key,
        }
        if self.do_as_backend:
            result.update(
                {
                    "account_name": self.do_account_name,
                    "endpoint": self.do_endpoint,
                    "bucket": self.do_bucket,
                    "key": self.__bucket_key__(),
                    "region": self.do_region,
                }
            )
        return result

    def is_local_state(self):
        return not self.do_as_backend

    def __bucket_key__(self):
        result = ""
        if self.do_as_backend:
            if self.do_account_name and self.do_bucket_key:
                result = f"{self.do_account_name}/{self.do_bucket_key}"
            else:
                result = f"{self.stage}/{self.module}"
        return result

    @classmethod
    def get_mapping_default(cls) -> List[Dict[str, str]]:
        return [
            {
                "gopass_path": "server/devops/digitalocean/s3",
                "gopass_field": "id",
                "name": "do_spaces_access_id",
            },
            {
                "gopass_path": "server/devops/digitalocean/s3",
                "gopass_field": "secret",
                "name": "do_spaces_secret_key",
            },
        ]
