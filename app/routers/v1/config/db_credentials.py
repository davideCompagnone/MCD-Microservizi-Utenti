from dataclasses import dataclass, Field
import os


def get_env_variable(var_name: str, default=None) -> str:
    """Esegui il parsing di una variabile d'ambiente.

    Args:
        var_name (str): Nome della variabile d'ambiente.
        default (str, optional): Valore di default.

    Raises:
        EnvironmentError: Se non trova la variabile d'ambiente e il default non è definito.

    Returns:
        str: Il valore della variabile d'ambiente.
    """
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        error_msg = f"Required environment variable {var_name} is not set."
        raise EnvironmentError(error_msg)


@dataclass(frozen=True, slots=True)
class DynamoCredentials:
    """Define credentials model.

    Attributes:
        username (str): Username.
        password (str): Password.

    Raises:
        pydantic.error_wrappers.ValidationError: If any of provided attribute
            doesn't pass type validation.

    """

    awsAccessKeyId: str = Field(default_factory=get_env_variable("AWS_ACCESS_KEY_ID"))
    awsSecretAccessKey: str = Field(
        default_factory=get_env_variable("AWS_SECRET_ACCESS_KEY")
    )
    endpointUrl: str = Field(
        default_factory=get_env_variable("AWS_ENDPOINT_URL", "http://localhost:8000")
    )
    regionName: str = Field(
        default_factory=get_env_variable("AWS_REGION_NAME", "us-west-2")
    )
