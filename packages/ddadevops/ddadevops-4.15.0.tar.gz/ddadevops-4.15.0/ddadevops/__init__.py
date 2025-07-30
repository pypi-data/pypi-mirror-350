"""
ddadevops provide tools to support builds combining gopass,
terraform, dda-pallet, aws & hetzner-cloud.

"""

from .domain import DnsRecord, BuildType, MixinType, ReleaseType, ProviderType
from .provs_k3s_build import ProvsK3sBuild

# from .aws_mfa_mixin import AwsMfaMixin, add_aws_mfa_mixin_config
from .c4k_build import C4kBuild
from .devops_image_build import DevopsImageBuild
from .devops_terraform_build import DevopsTerraformBuild
from .devops_build import DevopsBuild, get_devops_build
from .credential import gopass_password_from_path, gopass_field_from_path
from .release_mixin import ReleaseMixin

__version__ = "${version}"
