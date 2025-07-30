from typing import List, Optional, Dict
from .common import Validateable, Devops, BuildType, MixinType
from .image import Image
from .c4k import C4k
from .provs_k3s import K3s
from .terraform import TerraformDomain
from .release import Release
from .version import Version


class DevopsFactory:
    def __init__(self):
        pass

    def build_devops(self, inp: dict, version: Optional[Version] = None) -> Devops:
        build_types = self.parse_build_types(inp["build_types"])
        mixin_types = self.parse_mixin_types(inp["mixin_types"])

        specialized_builds: Dict[BuildType, Validateable] = {}
        if BuildType.IMAGE in build_types:
            specialized_builds[BuildType.IMAGE] = Image(inp)
        if BuildType.C4K in build_types:
            specialized_builds[BuildType.C4K] = C4k(inp)
        if BuildType.K3S in build_types:
            specialized_builds[BuildType.K3S] = K3s(inp)
        if BuildType.TERRAFORM in build_types:
            specialized_builds[BuildType.TERRAFORM] = TerraformDomain(inp)

        mixins: Dict[MixinType, Validateable] = {}
        if MixinType.RELEASE in mixin_types:
            mixins[MixinType.RELEASE] = Release(inp, version)

        devops = Devops(inp, specialized_builds=specialized_builds, mixins=mixins)

        devops.throw_if_invalid()

        return devops

    def merge(self, inp: dict, context: dict, authorization: dict) -> dict:
        return {} | context | authorization | inp

    def parse_build_types(self, build_types: List[str]) -> List[BuildType]:
        result = []
        for build_type in build_types:
            result += [BuildType[build_type]]
        return result

    def parse_mixin_types(self, mixin_types: List[str]) -> List[MixinType]:
        result = []
        for mixin_type in mixin_types:
            result += [MixinType[mixin_type]]
        return result
