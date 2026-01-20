# 🏥 System Rezerwacji Wizyt (FastAPI)

Kompletna aplikacja webowa typu **Full-Stack** do zarządzania rezerwacjami wizyt.
Projekt umożliwia umawianie, przeglądanie, edytowanie oraz usuwanie wizyt (CRUD) poprzez nowoczesny interfejs graficzny.

## 🚀 Technologie

Projekt został zbudowany przy użyciu nowoczesnego stosu technologicznego:

* **Backend:** Python 3.10+, FastAPI
* **Baza Danych:** SQLite + SQLAlchemy (ORM)
* **Frontend:** HTML5, CSS3 (Flexbox, Gradienty), JavaScript (Vanilla JS)
* **Templating:** Jinja2
* **Serwer:** Uvicorn

## ⚙️ Funkcjonalności

Aplikacja posiada zaawansowaną logikę biznesową i zabezpieczenia:

1.  **Pełny CRUD:** Możliwość dodawania, odczytu, edycji i usuwania wizyt.
2.  **Inteligentna Walidacja:**
    * 🗓️ Blokada umawiania wizyt z datą wsteczną.
    * ⏰ Ograniczenie godzin pracy (tylko 8:00 - 16:00).
    * 🚫 **Wykrywanie duplikatów:** System nie pozwoli umówić dwóch osób na tę samą datę i godzinę.
3.  **Sortowanie:** Wizyty są automatycznie układane chronologicznie (rosnąco).
4.  **Nowoczesny UI:**
    * Układ typu Dashboard (Formularz + Lista).
    * Responsywny design.
    * Interaktywne komunikaty błędów.

## 🛠️ Jak uruchomić projekt

1.  **Sklonuj repozytorium:**
    ```bash
    git clone https://github.com/Elenaa78/booking-system-api
    ```

2.  **Zainstaluj wymagane biblioteki:**
    ```bash
    pip install fastapi uvicorn sqlalchemy jinja2
    ```

3.  **Uruchom serwer:**
    ```bash
    python main.py
    ```

4.  **Otwórz w przeglądarce:**
    Wejdź na adres: `http://127.0.0.1:8000`

## 📚 Dokumentacja API

Automatyczna dokumentacja endpointów (Swagger UI) jest dostępna pod adresem:
`http://127.0.0.1:8000/docs`