from pydantic import BaseModel

class WizytaCreate(BaseModel):
    klient: str
    data: str
    godzina: str
    opis: str = "Brak opisu"

class Wizyta(WizytaCreate):
    id: int

    class Config:
        from_attributes = True