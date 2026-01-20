from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import uvicorn
from datetime import date

from database import engine, SessionLocal
import models
import schemas

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

app = FastAPI(title="System rezerwacji")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def strona_glowna(request: Request, db: Session = Depends(get_db)):
    wizyty_z_bazy = db.query(models.WizytaDB).all()

    return templates.TemplateResponse("index.html", {
        "request": request, 
        "wizyty": wizyty_z_bazy
    })

@app.post("/api/wizyty", response_model=schemas.Wizyta)
def dodaj_wizyte(wizyta: schemas.WizytaCreate, db: Session = Depends(get_db)):

    zajety_termin = db.query(models.WizytaDB).filter(
        models.WizytaDB.data == wizyta.data,
        models.WizytaDB.godzina == wizyta.godzina
    ).first()

    if zajety_termin:
        raise HTTPException(status_code=400, detail="Ten termin jest już zajęty")
    
    dzisiaj = date.today()
    if date.fromisoformat(wizyta.data) < dzisiaj:
        raise HTTPException(status_code=400, detail="Zła data")
    
    godzina_liczba = int(wizyta.godzina.split(":")[0])
    if godzina_liczba < 8 or godzina_liczba >= 16:
        raise HTTPException(status_code=400, detail="Pracujemy tylko między 8:00 a 16:00")

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

@app.delete("/api/wizyty/{id_wizyty}")
def usun_wizyte(id_wizyty: int, db: Session = Depends(get_db)):
    wizyta_do_usuniecia = db.query(models.WizytaDB).filter(models.WizytaDB.id == id_wizyty).first()

    if not wizyta_do_usuniecia:
        raise HTTPException(404, "Taka wizyta nie istnieje")
    
    db.delete(wizyta_do_usuniecia)
    db.commit()

    return {"message": f"Wizyta o id {id_wizyty} została usunięta"}


@app.put("/api/wizyty/{id_wizyty}", response_model=schemas.Wizyta)
def edytuj_wizyte(id_wizyty: int, nowe_dane: schemas.WizytaCreate, db: Session = Depends(get_db)):
    wizyta = db.query(models.WizytaDB).filter(models.WizytaDB.id == id_wizyty).first()

    if not wizyta:
        raise HTTPException(404, "Nie znaleziono wizyty")

    wizyta.klient = nowe_dane.klient
    wizyta.data = nowe_dane.data
    wizyta.godzina = nowe_dane.godzina
    wizyta.opis = nowe_dane.opis

    db.commit()
    db.refresh(wizyta)

    return wizyta

@app.get("/api/wizyty/{id_wizyty}", response_model=schemas.Wizyta)
def pobierz_wizyte(id_wizyty: int, db: Session = Depends(get_db)):
    wynik = db.query(models.WizytaDB).filter(models.WizytaDB.id == id_wizyty).first()

    if not wynik:
        raise HTTPException(404, "Wynik jest pusty")
    
    return wynik

@app.get("/api/wizyty", response_model=list[schemas.Wizyta])
def pobierz_wizyty(db: Session = Depends(get_db)):

    return db.query(models.WizytaDB).all()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
