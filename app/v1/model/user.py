from pydantic import EmailStr, BaseModel


class User(BaseModel):
    nome: str
    cognome: str
    codice_fiscale: str
    email: EmailStr
    numero_telefono: str
    indirizzo_residenza: str
    indirizzo_fatturazione: str


if __name__ == "__main__":
    user = User(
        nome="Mario",
        cognome="Rossi",
        codice_fiscale="RSSMRA80A01",
        email="federico.cantarelli@mail.polimi.it",
        numero_telefono="1234567890",
        indirizzo_residenza="Via Garibaldi 1, 20100 Milano (MI)",
        indirizzo_fatturazione="Via Garibaldi 1, 20100 Milano (MI)",
    )
    print(user)
