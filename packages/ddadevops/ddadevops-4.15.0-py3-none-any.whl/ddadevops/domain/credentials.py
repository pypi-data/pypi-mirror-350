from enum import Enum
from typing import List, Optional
from inflection import underscore
from .common import (
    Validateable,
)


class GopassType(Enum):
    FIELD = 0
    PASSWORD = 1


class CredentialMapping(Validateable):
    def __init__(self, mapping: dict):
        self.name = mapping.get("name", None)
        self.gopass_field = mapping.get("gopass_field", None)
        self.gopass_path = mapping.get("gopass_path", None)

    def validate(self) -> List[str]:
        result = []
        result += self.__validate_is_not_empty__("gopass_path")
        if not self.name and not self.gopass_field:
            result.append("Either name or gopass field has to be defined.")
        return result

    def gopass_type(self):
        if self.gopass_field:
            return GopassType.FIELD
        else:
            return GopassType.PASSWORD

    def name_for_input(self):
        if self.name:
            result = self.name
        elif self.gopass_field:
            result = underscore(self.gopass_field)
        else:
            result = ""
        return result

    def name_for_environment(self):
        return self.name_for_input().upper()


class Credentials(Validateable):
    def __init__(self, inp: dict, default_mappings: Optional[List] = None):
        if default_mappings is None:
            default_mappings = []
        inp_mappings = inp.get("credentials_mapping", [])
        self.mappings = {}
        for inp_mapping in default_mappings:
            mapping = CredentialMapping(inp_mapping)
            self.mappings[mapping.name_for_input()] = mapping
        for inp_mapping in inp_mappings:
            mapping = CredentialMapping(inp_mapping)
            self.mappings[mapping.name_for_input()] = mapping

    def validate(self) -> List[str]:
        result = []
        for mapping in self.mappings.values():
            result += mapping.validate()
        return result
