from pydantic import EmailStr, BaseModel, Field


class Indirizzo(BaseModel):
    via: str = Field(min_length=5)
    civico: int
    cap: int
    citta: str = Field(min_length=5)
    provincia: str = Field(min_length=2, max_length=2)

    def __str__(self):
        return f"{self.via} {self.civico}, {self.cap} {self.citta} ({self.provincia})"


class User(BaseModel):
    nome: str
    cognome: str
    codice_fiscale: str
    email: EmailStr
    numero_telefono: str
    indirizzo_residenza: Indirizzo
    indirizzo_fatturazione: Indirizzo


if __name__ == "__main__":
    user = User(
        nome="Mario",
        cognome="Rossi",
        codice_fiscale="RSSMRA80A01",
        email="federico.cantarelli@mail.polimi.it",
        numero_telefono="1234567890",
        indirizzo_residenza=Indirizzo(
            via="Via Garibaldi",
            civico=1,
            cap=20100,
            citta="Milano",
            provincia="MI",
        ),
        indirizzo_fatturazione=Indirizzo(
            via="Via Garibaldi",
            civico=1,
            cap=20100,
            citta="Milano",
            provincia="MI",
        ),
    )
    print(user)
