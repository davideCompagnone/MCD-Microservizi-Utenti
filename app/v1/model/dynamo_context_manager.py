from ..config.db_credentials import DynamoCredentials
from ..exceptions.dynamo import (
    DynamoTableDoesNotExist,
    DynamoTableAlreadyExists,
    UserNotFound,
    EmptyTable,
)
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from typing import List, Dict, Tuple
from ..model.user import User
from dataclasses import dataclass, field
from ..utils.custom_logger import LogSetupper

logger = LogSetupper(__name__).setup()


def parse_credentials() -> DynamoCredentials:
    return DynamoCredentials()


class DynamoContext:
    def __init__(self, table_name: str, index_name: str):
        self.tableName = table_name
        self.indexName = index_name
        self.connection = DynamoConnection(table_name=table_name, index_name=index_name)

    def __enter__(self):
        return self.connection

    def __exit__(self, error: Exception, value: object, traceback: object):
        self.close()


@dataclass(frozen=True, slots=True)
class DynamoConnection:
    credentials: DynamoCredentials
    table_name: str = field(default="User")
    index_name: str = field(default="user_id-index")
    dynamo_db: boto3.resource = field(default_factory=boto3.resource, init=False)

    # Apri la connessione
    def __post_init__(self):
        if self.dynamo_db is None:
            self.dynamo_db = boto3.resource(
                "dynamodb",
                endpoint_url=self.credentials.endpointUrl,
                region_name=self.credentials.regionName,
                aws_access_key_id=self.credentials.awsAccessKeyId,
                aws_secret_access_key=self.credentials.awsSecretAccessKey,
            )
        if self.credentials is None:
            self.credentials = parse_credentials()

    def close(self) -> None:
        """Funzione per chiudere la connessione a Dynamo DB"""
        self.dynamo_db.meta.client.close()

    def list_tables(self) -> List[str]:
        """Funzione per ottenere la lista delle tabelle presenti in DynamoDB

        Returns:
            List[str]: Ritorna la lista delle tabelle presenti in DynamoDB. Ritorna [] se non sono state trovate tabelle.
        """
        return self.dynamo_db.meta.client.list_tables()["TableNames"]

    # Proprietà per verificare se la tabella esiste
    @property
    def table_exists(self) -> bool:
        """Funzione per verificare se la tabella esiste. La tabella è la stessa passata al costruttore della classe.

        Returns:
            bool: Ritorna True se la tabella esiste, False altrimenti
        """
        existing_tables = self.list_tables()
        return self.table_name in existing_tables

    # Funzione per ritornare il massimo ID presente nella tabella
    def get_max_table_id(self) -> int:
        """Funzione per ottenere l'ID massimo presente nella tabella.

        Raises:
            DynamoTableDoesNotExist: Eccezione sollevata se la tabella non esiste.

        Returns:
            int: Ritorna l'ID massimo presente nella tabella
        """

        if not self.table_exists:
            raise DynamoTableDoesNotExist(self.table_name)

        table = self.dynamo_db.Table(self.table_name)
        response = table.scan(
            Select="ALL_ATTRIBUTES",  # Indica di restituire tutti gli attributi degli item trovati
        )
        items = response["Items"]
        if not items:
            return 0

        max_user_id = max(items, key=lambda x: int(x["user_id"]))["user_id"]
        return max_user_id

    # Funzione per cancellare un utente
    def delete_user(self, user_id: str):
        if not self.table_exists:
            raise DynamoTableDoesNotExist(self.table_name)

        table = self.dynamo_db.Table(self.table_name)

        table.delete_item(Key={"user_id": user_id})

    # Funzione per cancellare la tabella
    def delete_table(self):
        """Funzione per eliminare la tabella. La tabella è la stessa passata al costruttore della classe.

        Raises:
            DynamoTableDoesNotExist: Eccezione sollevata se la tabella non esiste.
        """
        if not self.table_exists:
            raise DynamoTableDoesNotExist(self.table_name)
        table = self.dynamo_db.Table(self.table_name)
        table.delete()
        table.meta.client.get_waiter("table_not_exists").wait(TableName=self.table_name)

    def get_users(self) -> List[Dict]:
        """Funzione per ritornare tutti gli utenti all'interno della tabella.

        Raises:
            DynamoTableDoesNotExist: Eccezione sollevata se la tabella non esiste.
            EmptyTable: Eccezione sollevata se la tabella è vuota.

        Returns:
            List[Dict]: Ritorna la lista degli utenti presenti nella tabella
        """
        if not self.table_exists:
            raise DynamoTableDoesNotExist(self.table_name)

        table = self.dynamo_db.Table(self.table_name)
        response = table.scan()
        items = response.get("Items", [])
        if not items:
            raise EmptyTable(self.table_name)
        return items

    def get_user(self, user_id: str) -> Dict:
        """Funzione per estrarre un utente dalla tabella.

        Args:
            user_id (str): Id dell'utente da estrarre.

        Raises:
            DynamoTableDoesNotExist: Eccezione sollevata se la tabella non esiste.
            UserNotFound: Eccezione sollevata se l'utente non è presente nella tabella.

        Returns:
            Dict: Ritorna l'utente estratto dalla tabella
        """
        if not self.table_exists:
            raise DynamoTableDoesNotExist(self.table_name)

        table = self.dynamo_db.Table(self.table_name)

        response = table.get_item(Key={"user_id": user_id})
        item = response.get("Item")
        if not item:
            raise UserNotFound(user_id)
        return item

    # Funzione per creare la tabella utenti su DynamoDB
    def create_users_table(self):
        """Funzione per creare la tabella utenti su DynamoDB.

        Raises:
            DynamoTableAlreadyExists: Eccezione sollevata se la tabella esiste già.
        """
        if self.table_exists:
            raise DynamoTableAlreadyExists(self.table_name)

        table = self.dynamo_db.create_table(
            TableName=self.table_name,
            AttributeDefinitions=[
                {
                    "AttributeName": "user_id",
                    "AttributeType": "N",  # S per stringa, N per numero, etc.
                },
                # Aggiungi altri attributi se necessario
            ],
            KeySchema=[
                {
                    "AttributeName": "user_id",
                    "KeyType": "HASH",  # HASH per chiave primaria
                },
                # Aggiungi altre chiavi se necessario (es. RANGE per chiave di ordinamento)
            ],
            GlobalSecondaryIndexes=[
                {
                    "IndexName": self.index_name,
                    "KeySchema": [
                        {
                            "AttributeName": "user_id",
                            "KeyType": "HASH",  # HASH per chiave primaria
                        },
                        # Aggiungi altre chiavi se necessario
                    ],
                    "Projection": {
                        "ProjectionType": "ALL"  # Tipo di proiezione, può essere 'KEYS_ONLY', 'INCLUDE' o 'ALL'
                    },
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 10,
                        "WriteCapacityUnits": 10,
                    },
                }
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
        )
        table.meta.client.get_waiter("table_exists").wait(TableName=self.table_name)
        logger.info(f"Tabella '{self.table_name}' creata con successo!")

    @property
    def is_alive(self) -> Tuple[bool, int]:
        response = self.list_tables()
        return (
            response["ResponseMetadata"]["HTTPStatusCode"] == 200,
            response["ResponseMetadata"]["HTTPStatusCode"],
        )
