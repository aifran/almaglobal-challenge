import decouple
from enum import Enum

# Create a Config object and specify the path to your .env file


class CredentialsNotFoundError(Exception):
    pass

class ServiceEnum(Enum):
    ROFEX = "rofex"


SERVICE_CREDENTIALS = {
    ServiceEnum.ROFEX: [
        "rofex_user",
        "rofex_password",
        "rofex_account"
    ]
}


def load_credentials_from_env(service: ServiceEnum) -> dict:
    """
    Load credentials from environment for a given service
    :param service: any of the supported services in ServiceEnum
    :return: dict
    """
    # Load credentials from environment
    creds = {}
    try:
        for k in SERVICE_CREDENTIALS[service]:
            creds[k.replace(f"{service.value}_", "")] = decouple.config(k)
    except decouple.UndefinedValueError:
        raise CredentialsNotFoundError(f"{service.name} credentials not found in environment")
    return creds

