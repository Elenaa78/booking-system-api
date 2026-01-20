from sqlalchemy import Column, Integer, String
from database import Base

class WizytaDB(Base):
    __tablename__ = "wizyty"

    id = Column(Integer, primary_key=True, index=True)
    klient = Column(String, index=True)
    data = Column(String)
    godzina = Column(String)
    opis = Column(String)