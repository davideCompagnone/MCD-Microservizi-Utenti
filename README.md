# Users Microservices
![Static Badge](https://img.shields.io/badge/python--3.10-blue?style=flat&logo=python&labelColor=white) <br>

This repository contains the project work for the Cloud Data Engineer master's program held by Cefriel. The project involves implementing a simple API interface to perform basic CRUD operations on a DynamoDB database containing user data.

## Environment Variables
```bash
AWS_ACCESS_KEY_ID='DUMMYIDEXAMPLE' # Amazon AK
AWS_SECRET_ACCESS_KEY='DUMMYEXAMPLEKEY' #AMAZOn SK
AWS_ENDPOINT_URL='http://dynamodb-local:8000' # Local dynamo url for 
ENV='local' # Variable for environment-wide configuration
DYNAMODB_REGION='eu-west-1' # DynamoDb Region
DYNAMODB_TABLE='MCDE2023-users-cf' # Table Name of the dynamodb
```


## Local Development
To run locally, follow these steps:
```bash
# Clone the exam repository
git clone https://github.com/davideCompagnone/MCD-Microservizi-Utenti.git

# Navigate to the newly created repository
cd MCD-Microservizi-Utenti

# Execute the docker-compose
docker-compose up --build # to run in detached mode, add the -d flag

# Make a request to verify it is running correctly
curl http://localhost:8080/v1/ready
```
This [file](./esame_master.postman_collection.json) contains example Postman requests.

## API Documentation
The code utilizes the [OpenAPI Specification](https://github.com/OAI/OpenAPI-Specification) to define HTTP API interfaces via the [FastAPI](https://fastapi.tiangolo.com/) framework. The documentation is generated automatically by FastAPI framework. To display the documentatio of the API interface, once started the container, simply navigate to `localhost:8080/docs`.

## Contribution Guideline
The repository has two main branches. The first is dev, for development, and the second is main branch with the latest stable release of the code. Branches for new features always start from the main branch. The naming convention for creating new branches is as follows:
- `feature/<new-feature>` to implement a new feature
- `fix/<ticket nr or id>` to fix a bug
- `merge/<merge-cause>` to resolve merge conflict
Once the development on the individual branches is completed, a PR is opened in the dev branch to merge the code. After verifying that everything is working correctly, a PR is opened in the main branch, which will be reviewed and accepted.