from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import uvicorn

from database import engine, SessionLocal
import models
import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="System rezerwacji")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/wizyty", response_model=schemas.Wizyta)
def dodaj_wizyte(wizyta: schemas.WizytaCreate, db: Session = Depends(get_db)):
    db_wizyta = models.WizytaDB(
        klient = wizyta.klient,
        data = wizyta.data,
        godzina = wizyta.godzina,
        opis = wizyta.opis
    )

    db.add(db_wizyta)
    db.commit()
    db.refresh(db_wizyta)

    return db_wizyta

@app.get("/api/wizyty", response_model=list[schemas.Wizyta])
def pobierz_wizyty(db: Session = Depends(get_db)):
    return db.query(models.WizytaDB).all()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
