from dataclasses import dataclass, field
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
        # Restituisce il valore della variabile d'ambiente
        return os.environ[var_name]
    # Se non esiste
    except KeyError as e:
        # Se è definito un valore di default lo restituisce
        if default is not None:
            return default
        raise EnvironmentError(
            f"La variabile {var_name} non è stata impostata correttamente."
        )


@dataclass(frozen=True, slots=True)
class DynamoCredentials:
    """Definisce il modello delle credenziali per la connessione a DynamoDB.

    Attributes:
        username (str): Username.
        password (str): Password.

    """

    awsAccessKeyId: str = field(default=get_env_variable("AK"))
    awsSecretAccessKey: str = field(default=get_env_variable("SK"))
    endpointUrl: str = field(
        default=get_env_variable("AWS_ENDPOINT_URL", default="http://localhost:8000")
    )
    regionName: str = field(
        default=get_env_variable("DYNAMODB_REGION", default="eu-west-1")
    )
    tableName: str = field(default=get_env_variable("UsersTable"))
    version: str = field(default=get_env_variable("TagVersion"))


if __name__ == "__main__":
    credentials = DynamoCredentials()
    print(credentials)
