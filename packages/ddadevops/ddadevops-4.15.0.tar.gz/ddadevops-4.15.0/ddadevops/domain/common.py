from enum import Enum
from typing import List, Dict


def filter_none(list_to_filter):
    return [x for x in list_to_filter if x is not None]


class BuildType(Enum):
    IMAGE = 0
    C4K = 1
    K3S = 2
    TERRAFORM = 3


class ProviderType(Enum):
    DIGITALOCEAN = 0
    HETZNER = 1
    AWS = 2


class MixinType(Enum):
    RELEASE = 0


class ReleaseType(Enum):
    MAJOR = 3
    MINOR = 2
    PATCH = 1
    NONE = None


class Validateable:
    def __validate_is_not_none__(self, field_name: str) -> List[str]:
        value = self.__dict__[field_name]
        if value is None:
            return [f"Field '{field_name}' must not be None."]
        return []

    def __validate_is_not_empty__(self, field_name: str) -> List[str]:
        result = self.__validate_is_not_none__(field_name)
        if len(result) == 0:
            value = self.__dict__[field_name]
            if type(value) is str and value == "":
                result += [f"Field '{field_name}' must not be empty."]
            elif type(value) is list and len(value) == 0:
                result += [f"Field '{field_name}' must not be empty."]
        return result

    def validate(self) -> List[str]:
        return []

    def is_valid(self) -> bool:
        return len(self.validate()) < 1

    def throw_if_invalid(self):
        if not self.is_valid():
            issues = "\n".join(self.validate())
            raise ValueError(f"Invalid Validateable: {issues}")


class CredentialMappingDefault:
    @classmethod
    def get_mapping_default(cls) -> List[Dict[str, str]]:
        return []


class DnsRecord(Validateable):
    def __init__(self, fqdn, ipv4=None, ipv6=None):
        self.fqdn = fqdn
        self.ipv4 = ipv4
        self.ipv6 = ipv6

    def validate(self) -> List[str]:
        result = []
        result += self.__validate_is_not_empty__("fqdn")
        if (not self.ipv4) and (not self.ipv6):
            result.append("ipv4 & ipv6 may not both be empty.")
        return result

    def ip(self) -> str:
        if (self.ipv4):
            return self.ipv4
        else:
            return self.ipv6


class Devops(Validateable):
    def __init__(
        self,
        inp: dict,
        specialized_builds: dict[BuildType, Validateable],
        mixins: dict[MixinType, Validateable],
    ):
        self.stage = inp.get("stage")
        self.project_root_path = inp.get("project_root_path")
        self.module = inp.get("module")
        self.name = inp.get("name", self.module)
        self.build_dir_name = inp.get("build_dir_name", "target")
        self.specialized_builds = specialized_builds
        self.mixins = mixins

    def build_path(self):
        path = [self.project_root_path, self.build_dir_name, self.name, self.module]
        return "/".join(filter_none(path))

    def validate(self) -> List[str]:
        result = []
        result += self.__validate_is_not_empty__("stage")
        result += self.__validate_is_not_empty__("project_root_path")
        result += self.__validate_is_not_empty__("module")
        result += self.__validate_is_not_none__("specialized_builds")
        if self.specialized_builds:
            for build in self.specialized_builds:
                result += self.specialized_builds[build].validate()
        if self.mixins:
            for mixin in self.mixins:
                result += self.mixins[mixin].validate()
        return result
