import deprecation
from .infrastructure import CredentialsApi


@deprecation.deprecated(
    deprecated_in="3.2", details="use infrastructure.CredentialsApi instead"
)
def gopass_field_from_path(path, field):
    api = CredentialsApi()
    return api.gopass_field_from_path(path, field)


@deprecation.deprecated(
    deprecated_in="3.2", details="use infrastructure.CredentialsApi instead"
)
def gopass_password_from_path(path):
    api = CredentialsApi()
    return api.gopass_password_from_path(path)
