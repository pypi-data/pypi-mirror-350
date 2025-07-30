from typing import List, Dict, Set, Any
from .common import Validateable, CredentialMappingDefault


class Aws(Validateable, CredentialMappingDefault):
    def __init__(
        self,
        inp: dict,
    ):
        self.stage = inp.get("stage")
        self.module = inp.get("module")
        self.aws_access_key = inp.get("aws_access_key")
        self.aws_secret_key = inp.get("aws_secret_key")
        self.aws_bucket = inp.get("aws_bucket")
        self.aws_bucket_kms_key_id = inp.get("aws_bucket_kms_key_id")
        self.aws_account_name = inp.get("aws_account_name", self.stage)
        self.aws_bucket_key = inp.get("aws_bucket_key", self.module)
        self.aws_as_backend = inp.get("aws_as_backend", False)
        self.aws_region = inp.get("aws_region", "eu-central-1")

    def validate(self) -> List[str]:
        result = []
        result += self.__validate_is_not_empty__("stage")
        result += self.__validate_is_not_empty__("module")
        result += self.__validate_is_not_empty__("aws_access_key")
        result += self.__validate_is_not_empty__("aws_secret_key")
        result += self.__validate_is_not_empty__("aws_account_name")
        result += self.__validate_is_not_empty__("aws_as_backend")
        if self.aws_as_backend:
            result += self.__validate_is_not_empty__("aws_bucket")
            result += self.__validate_is_not_empty__("aws_bucket_key")
            result += self.__validate_is_not_empty__("aws_region")
        return result

    def backend_config(self) -> Dict[str, Any]:
        result = {}
        if self.aws_as_backend:
            result = {
                "access_key": self.aws_access_key,
                "secret_key": self.aws_secret_key,
                "bucket": self.aws_bucket,
                "key": self.__bucket_key__(),
                "region": self.aws_region,
            }
            if self.aws_bucket_kms_key_id:
                result["kms_key_id"] = self.aws_bucket_kms_key_id
        return result

    def resources_from_package(self) -> Set[str]:
        result = {"provider_registry.tf", "aws_provider.tf", "aws_provider_vars.tf"}
        if self.aws_as_backend:
            if self.aws_bucket_kms_key_id:
                result.update(
                    {
                        "aws_backend_wkms_vars.tf",
                        "aws_backend.tf",
                    }
                )
            else:
                result.update(
                    {
                        "aws_backend_wokms_vars.tf",
                        "aws_backend.tf",
                    }
                )
        return result

    def project_vars(self):
        result = {
            "aws_access_key": self.aws_access_key,
            "aws_secret_key": self.aws_secret_key,
            "aws_region": self.aws_region,
        }
        if self.aws_as_backend:
            result.update(
                {
                    "account_name": self.aws_account_name,
                    "bucket": self.aws_bucket,
                    "key": self.__bucket_key__(),
                }
            )
            if self.aws_bucket_kms_key_id:
                result.update(
                    {
                        "kms_key_id": self.aws_bucket_kms_key_id,
                    }
                )
        return result

    def is_local_state(self):
        return not self.aws_as_backend

    def __bucket_key__(self):
        result = ""
        if self.aws_as_backend:
            if self.aws_account_name and self.aws_bucket_key:
                result = f"{self.aws_account_name}/{self.aws_bucket_key}"
            else:
                result = f"{self.stage}/{self.module}"
        return result

    @classmethod
    def get_mapping_default(cls) -> List[Dict[str, str]]:
        return []
