from pydantic import EmailStr, BaseModel


class User(BaseModel):
    nome: str
    cognome: str
    codice_fiscale: str
    partita_iva: str
    email: EmailStr
    numero_telefono: str
    indirizzo_residenza: str
    indirizzo_fatturazione: str
