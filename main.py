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

@app.delete("/api/wizyty")
def usun_wizyte(id_wizyty: int, db: Session = Depends(get_db)):
    wizyta_do_usuniecia = db.query(models.WizytaDB).filter(models.WizytaDB.id == id_wizyty).first()

    if wizyta_do_usuniecia:
        db.delete(wizyta_do_usuniecia)
        db.commit()
        return {"message": f"Wizyta o id {id_wizyty} została usunięta"}
    
    return {"message": "Nie znaleziono takiej wizyty"}

@app.put("/api/wizyty", response_model=schemas.Wizyta)
def edytuj_wizyte(id_wizyty: int, nowe_dane: schemas.WizytaCreate, db: Session = Depends(get_db)):
    wizyta = db.query(models.WizytaDB).filter(models.WizytaDB.id == id_wizyty).first()

    if wizyta:
        wizyta.klient = nowe_dane.klient
        wizyta.data = nowe_dane.data
        wizyta.godzina = nowe_dane.godzina
        wizyta.opis = nowe_dane.opis

        db.commit()
        db.refresh(wizyta)

        return wizyta

    return None

@app.get("/api/wizyty/{wizyta_id}", response_model=schemas.Wizyta)
def pobierz_wizyte(id_wizyty: int, db: Session = Depends(get_db)):
    return db.query(models.WizytaDB).filter(models.WizytaDB.id == id_wizyty).first()

@app.get("/api/wizyty", response_model=list[schemas.Wizyta])
def pobierz_wizyty(db: Session = Depends(get_db)):
    return db.query(models.WizytaDB).all()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
