from pydantic import EmailStr, BaseModel


class User(BaseModel):
    nome: str
    cognome: str
    cf: str
    p_iva: str
    email: EmailStr
    n_telefono: str
    indirizzo_residenza: str
    indirizzo_fatturazione: str


class UserResponse(User):
    user_id: int
