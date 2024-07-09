from app.config.db_credentials import DynamoCredentials
from app.routers.v1.exceptions.dynamo import (
    DynamoTableDoesNotExist,
    DynamoTableAlreadyExists,
    UserNotFound,
    EmptyTable,
)
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from typing import List, Dict, Tuple
from app.routers.v1.model.user import User
from dataclasses import dataclass, field
from app.utils.custom_logger import LogSetupper

logger = LogSetupper(__name__).setup()


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
    credentials: DynamoCredentials = DynamoCredentials()
    table_name: str = field(default="User")
    index_name: str = field(default="user_id-index")
    dynamo_db: boto3.resource | None = None

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


# # Funzione per inserire un nuovo utente nella tabella
# def insert_user(nome, cognome, cf, p_iva, email,n_telefono,indirizzo_residenza,indirizzo_fatturazione):
#     if not table_exists(table_name):
#         create_users_table()

#     try:
#         max_user_id = get_max_user_id()
#         if max_user_id ==-1:
#             print("Errore nel recupero dello user id, riprovare")
#             return -1
#         else:
#             new_user_id = max_user_id + 1

#         table = dynamodb.Table(table_name)
#         table.put_item(
#             Item={
#                 'user_id': new_user_id,
#                 'nome': nome,
#                 'cognome':cognome,
#                 'cf': cf,
#                 'p_iva': p_iva,
#                 'email': email,
#                 'n_telefono':n_telefono,
#                 'indirizzo_residenza' : indirizzo_residenza,
#                 'indirizzo_fatturazione' : indirizzo_fatturazione
#             }
#         )
#         print(f"Utente con ID {new_user_id} inserito con successo.")
#         return new_user_id

#     except ClientError as e:
#         print("Errore durante l'inserimento dell'utente:", e.response['Error']['Message'])
#         return -2


# if __name__=="__main__":

#     # Esempio di utilizzo delle funzioni definite

#     # Creazione della tabella se non esiste
#     create_users_table()

#     # Inserimento di un nuovo utente
#     user_id=insert_user( 'alice', 'al','738219837213',None,'alice@example.com','32243242342','via kennedy',None)
#     user_id=insert_user( 'bob', 'blob','738219837213',None,'bob@example.com','32243242342','via kennedy',None)
#     user_id=insert_user( 'carl', 'marx',None,'sa.kjda88','carle@example.com','32243242342','via lenin','via mosca')


#     # Ottenere tutti gli utenti
#     get_users()

#     # Ottenere un utente specifico per ID
#     get_users(user_id)

#     # Eliminazione di un utente
#     delete_user(user_id)

#     delete_table(table_name)
