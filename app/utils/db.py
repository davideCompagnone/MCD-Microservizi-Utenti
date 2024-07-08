import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key


# Configurazione del client DynamoDB

dynamodb = boto3.resource('dynamodb', \
                        endpoint_url='http://localhost:8000', \
                        region_name='us-west-2', \
                        aws_access_key_id='DUMMYIDEXAMPLE', \
                        aws_secret_access_key='DUMMYEXAMPLEKEY' \
                            )
table_name = 'Users'
index_name = 'user_id-index'  # Nome dell'indice su cui eseguire la query

# Funzione per verificare se la tabella esiste
def table_exists(table_name):
    existing_tables = dynamodb.meta.client.list_tables()['TableNames']
    return table_name in existing_tables

# Funzione per creare la tabella utenti su DynamoDB
def create_users_table():
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            AttributeDefinitions=[
                {
                    'AttributeName': 'user_id',
                    'AttributeType': 'N'  # S per stringa, N per numero, etc.
                },
                # Aggiungi altri attributi se necessario
            ],
            KeySchema=[
                {
                    'AttributeName': 'user_id',
                    'KeyType': 'HASH'  # HASH per chiave primaria
                },
                # Aggiungi altre chiavi se necessario (es. RANGE per chiave di ordinamento)
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': index_name,
                    'KeySchema': [
                        {
                            'AttributeName': 'user_id',
                            'KeyType': 'HASH'  # HASH per chiave primaria
                        },
                        # Aggiungi altre chiavi se necessario
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'  # Tipo di proiezione, può essere 'KEYS_ONLY', 'INCLUDE' o 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 10,
                        'WriteCapacityUnits': 10
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
        print(f"Tabella '{table_name}' creata con successo!")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"La tabella '{table_name}' esiste già.")
        else:
            print(f"Errore durante la creazione della tabella '{table_name}':", e.response['Error']['Message'])

#Funzione per ottenere il massimo user_id dalla tabella DynamoDB
def get_max_user_id():
    
    try:
        table = dynamodb.Table(table_name)

        response = table.scan(
            Select='ALL_ATTRIBUTES',  # Indica di restituire tutti gli attributi degli item trovati
        )

        items = response['Items']
        if not items:
            return 0

        max_user_id = max(items, key=lambda x: int(x['user_id']))['user_id']
        return max_user_id


    except ClientError as e:
        print(f"Errore durante il recupero del massimo user_id: {e}")
        return -1  # Se c'è un errore, ritorna '0'



# Funzione per inserire un nuovo utente nella tabella
def insert_user(nome, cognome, cf, p_iva, email,n_telefono,indirizzo_residenza,indirizzo_fatturazione):
    if not table_exists(table_name):
        create_users_table()

    try:
        max_user_id = get_max_user_id()
        if max_user_id ==-1:
            print("Errore nel recupero dello user id, riprovare")
            return -1
        else:
            new_user_id = max_user_id + 1

        table = dynamodb.Table(table_name)
        table.put_item(
            Item={
                'user_id': new_user_id,
                'nome': nome,
                'cognome':cognome,
                'cf': cf,
                'p_iva': p_iva,
                'email': email,
                'n_telefono':n_telefono,
                'indirizzo_residenza' : indirizzo_residenza,
                'indirizzo_fatturazione' : indirizzo_fatturazione
            }
        )
        print(f"Utente con ID {new_user_id} inserito con successo.")
        return new_user_id

    except ClientError as e:
        print("Errore durante l'inserimento dell'utente:", e.response['Error']['Message'])
        return -2


# Funzione per cancellare un utente dalla tabella
def delete_user(user_id):
    table = dynamodb.Table(table_name)
    try:
        table.delete_item(
            Key={
                'user_id': user_id
            }
        )
        print(f"Utente con ID {user_id} eliminato con successo.")
        return 0
    except ClientError as e:
        print("Errore durante l'eliminazione dell'utente:", e.response['Error']['Message'])
        return -1

# Funzione per ottenere tutti gli utenti o uno specifico per ID
def get_users(user_id=None):
    table = dynamodb.Table(table_name)
    if user_id:
        response = table.get_item(Key={'user_id': user_id})
        item = response.get('Item')
        print("Dettagli utente:")
        print(item)
        return item
    else:
        response = table.scan()
        items = response.get('Items', [])
        if items:
            print("Lista degli utenti:")
            for item in items:
                print(item)
            return items
        else:
            print("Nessun utente trovato.")
            return None

def delete_table(table_name):
    if not table_exists(table_name):
        print(f"La tabella '{table_name}' non esiste.")
        return

    table = dynamodb.Table(table_name)
    try:
        table.delete()
        table.meta.client.get_waiter('table_not_exists').wait(TableName=table_name)
        print(f"Tabella '{table_name}' eliminata con successo.")
    except ClientError as e:
        print(f"Errore durante l'eliminazione della tabella '{table_name}':", e.response['Error']['Message'])



if __name__=="__main__":

    # Esempio di utilizzo delle funzioni definite

    # Creazione della tabella se non esiste
    create_users_table()

    # Inserimento di un nuovo utente
    user_id=insert_user( 'alice', 'al','738219837213',None,'alice@example.com','32243242342','via kennedy',None)
    user_id=insert_user( 'bob', 'blob','738219837213',None,'bob@example.com','32243242342','via kennedy',None)
    user_id=insert_user( 'carl', 'marx',None,'sa.kjda88','carle@example.com','32243242342','via lenin','via mosca')


    # Ottenere tutti gli utenti
    get_users()

    # Ottenere un utente specifico per ID
    get_users(user_id)

    # Eliminazione di un utente
    delete_user(user_id)

    delete_table(table_name)


