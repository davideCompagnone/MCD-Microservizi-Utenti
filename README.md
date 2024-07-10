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
## Variabili ambientali
```bash
AWS_ACCESS_KEY_ID='<key_id>'
AWS_SECRET_ACCESS_KEY='<access_key>'
AWS_ENDPOINT_URL='<endpointurl>:<port>'
AWS_REGION_NAME='<region>' # default a ...
```