# MCD-Microservizi-Utenti

Repository per il progetto del Master CDE - V edizione.

## Esecuzione in locale
Per eseguire in locale, seguire i seguenti passaggi:
```bash
# Clona la repository dell'esame
git clone https://github.com/davideCompagnone/MCD-Microservizi-Utenti.git

# Spostati nella repository appena creata
cd MCD-Microservizi-Utenti

# Esegui il docker-compose
docker-compose up --build # per eseguirelo in modalità detached aggiungere il flag -d

# Esegui una chiamata per verificare che sia correttamente in esecuzione
curl http://localhost:8080/v1/ready
```
Il file `esame_master.postman_collection.json` contiene delle chiamate postman d'esempio.

## Variabili ambientali
```bash
AWS_ACCESS_KEY_ID='DUMMYIDEXAMPLE'
AWS_SECRET_ACCESS_KEY='DUMMYEXAMPLEKEY'
AWS_ENDPOINT_URL='http://dynamodb-local:8000'
ENVIRONMENT='local' # variabile per configurazioni dipendenti dall'ambiente di esecuzione, come il livello dei log
DYNAMODB_REGION='eu-west-1'
DYNAMODB_TABLE='MCDE2023-users-cf'
```