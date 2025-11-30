# Voli Aerei in Flask 🛫

Questa repository ospita il codice del progetto _Voli Aerei_ 
implementato in `flask`.


## Contesto

Questo progetto è stato sviluppato per gli studenti dell'**ITS ICT Academy** ([sito web](https://www.its-ictacademy.com/)) 
come esercitazione pratica su:

- **Backend**: Python con Flask, creazione di API REST, gestione di dati
- **Frontend**: React, consumo di API, gestione dello stato
- **Database**: Gestione mockup di dati (da estendere a vero database)
- **Integrazione**: Comunicazione client-server tramite HTTP

---

## 🏗️ Architettura

```
VoliAerei/
├── data_model/           # Modelli dati (OOP) secondo la metodologia di Design in Python vista in Progettazione.1
│   ├── nazione.py
│   ├── citta.py
│   ├── compagnia.py
│   ├── aeroporto.py
│   ├── volo.py
│   └── custom_types.py
├── db/
    ├── mockup_db.json   # Database "finto", su un singolo file JSON
│   └── utils.py         # Utilità di caricamento dati
├── main.py              # App Flask principale
├── test.py              # (alcuni) test dell'API con il modulo `requests` di Python
└── README.md
```

---

## 🚀 Quick Start

### Requisiti

- Python 3.8+
- Flask
- Node.js / npm (per il frontend React)

### Backend Setup

```bash
# Clona il repository
git clone https://github.com/tuoutente/VoliAerei.git
cd VoliAerei

# Crea un ambiente virtuale
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oppure
venv\Scripts\activate     # Windows

# Installa le dipendenze
pip install flask requests

# Avvia il server
python main.py
```

Il backend sarà disponibile su `http://localhost:5000/`

### Frontend Setup


> [!NOTE]  
> Questa parte non è stata ancora implementata.


```bash
# In una nuova cartella
npx create-react-app client
cd client

# Installa axios per le richieste HTTP
npm install axios

# Avvia il frontend
npm start
```

Il frontend sarà disponibile su `http://localhost:3000/`

---

## 📖 API REST

### Base URL

```
http://localhost:5000/
```

### Endpoint Principali

#### 1. Nazioni

**GET /nazioni** - Lista di tutte le nazioni
```bash
curl http://localhost:5000/nazioni
```

**Response 200:**
```json
[
  {
    "nome": "Italia",
    "fondazione": 1861
  },
  {
    "nome": "Francia",
    "fondazione": 1789
  }
]
```

**POST /nazioni** - Crea una nuova nazione
```bash
curl -X POST http://localhost:5000/nazioni \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Germania",
    "fondazione": 1871
  }'
```

**Response 201:**
```json
{
  "nome": "Germania",
  "fondazione": 1871
}
```

**GET /nazioni/{nome}** - Dettagli di una nazione
```bash
curl http://localhost:5000/nazioni/Italia
```

**Response 200:**
```json
{
  "nome": "Italia",
  "fondazione": 1861
}
```

**PATCH /nazioni/{nome}** - Aggiorna una nazione
```bash
curl -X PATCH http://localhost:5000/nazioni/Italia \
  -H "Content-Type: application/json" \
  -d '{
    "fondazione": 1861
  }'
```

---

#### 2. Città

**GET /citta** - Lista di tutte le città
```bash
curl http://localhost:5000/citta
```

**Response 200:**
```json
[
  {
    "nome": "Roma",
    "abitanti": 2873000,
    "nazione": "Italia"
  },
  {
    "nome": "Milano",
    "abitanti": 1352000,
    "nazione": "Italia"
  }
]
```

**POST /citta** - Crea una nuova città
```bash
curl -X POST http://localhost:5000/citta \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Firenze",
    "abitanti": 380000,
    "nazione": "Italia"
  }'
```

**Response 201:**
```json
{
  "nome": "Firenze",
  "abitanti": 380000,
  "nazione": "Italia"
}
```

**PATCH /citta/{nome}** - Aggiorna una città
```bash
curl -X PATCH http://localhost:5000/citta/Roma \
  -H "Content-Type: application/json" \
  -d '{
    "abitanti": 2900000,
    "nazione": "Italia"
  }'
```

---

#### 3. Compagnie

**GET /compagnie** - Lista di tutte le compagnie
```bash
curl http://localhost:5000/compagnie
```

**Response 200:**
```json
[
  {
    "nome": "Alitalia",
    "fondazione": 1946,
    "citta": "Roma"
  }
]
```

**POST /compagnie** - Crea una nuova compagnia
```bash
curl -X POST http://localhost:5000/compagnie \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Ryanair",
    "fondazione": 1985,
    "citta": "Milano"
  }'
```

**Response 201:**
```json
{
  "nome": "Ryanair",
  "fondazione": 1985,
  "citta": "Milano"
}
```

---

#### 4. Aeroporti

**GET /aeroporti** - Lista di tutti gli aeroporti
```bash
curl http://localhost:5000/aeroporti
```

**Response 200:**
```json
[
  {
    "nome": "Fiumicino",
    "codice": "FCO",
    "citta": "Roma"
  },
  {
    "nome": "Malpensa",
    "codice": "MXP",
    "citta": "Milano"
  }
]
```

**POST /aeroporti** - Crea un nuovo aeroporto
```bash
curl -X POST http://localhost:5000/aeroporti \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Peretola",
    "codice": "FLR",
    "citta": "Firenze"
  }'
```

**Response 201:**
```json
{
  "nome": "Peretola",
  "codice": "FLR",
  "citta": "Firenze"
}
```

---

#### 5. Voli

**GET /voli** - Lista di tutti i voli
```bash
curl http://localhost:5000/voli
```

**Response 200:**
```json
[
  {
    "codice": "AZ123",
    "compagnia": "Alitalia",
    "partenza": "FCO",
    "arrivo": "MXP",
    "durata_minuti": 60
  },
  {
    "codice": "AZ456",
    "compagnia": "Alitalia",
    "partenza": "FCO",
    "arrivo": "CDG",
    "durata_minuti": 120
  }
]
```

**POST /voli** - Crea un nuovo volo
```bash
curl -X POST http://localhost:5000/voli \
  -H "Content-Type: application/json" \
  -d '{
    "codice": "FR789",
    "compagnia": "Ryanair",
    "partenza": "MXP",
    "arrivo": "FCO",
    "durata_minuti": 70
  }'
```

**Response 201:**
```json
{
  "codice": "FR789",
  "compagnia": "Ryanair",
  "partenza": "MXP",
  "arrivo": "FCO",
  "durata_minuti": 70
}
```

**GET /voli/{codice}** - Dettagli di un volo
```bash
curl http://localhost:5000/voli/AZ123
```

**Response 200:**
```json
{
  "codice": "AZ123",
  "compagnia": "Alitalia",
  "partenza": "FCO",
  "arrivo": "MXP",
  "durata_minuti": 60
}
```

---

#### 6. Calcolo Voli

**GET /calcola_voli_tra_nazioni** - Voli tra due nazioni
```bash
curl "http://localhost:5000/calcola_voli_tra_nazioni?partenza=Italia&arrivo=Francia"
```

**Response 200:**
```json
[
  {
    "codice": "AZ456",
    "compagnia": "Alitalia",
    "partenza": "FCO",
    "arrivo": "CDG",
    "durata_minuti": 120
  }
]
```

**GET /calcola_voli_tra_citta** - Voli tra due città
```bash
curl "http://localhost:5000/calcola_voli_tra_citta?partenza=Roma&arrivo=Milano"
```

**Response 200:**
```json
[
  {
    "codice": "AZ123",
    "compagnia": "Alitalia",
    "partenza": "FCO",
    "arrivo": "MXP",
    "durata_minuti": 60
  }
]
```

**GET /aeroporti/{codice}/voli_verso** - Voli da un aeroporto a un altro
```bash
curl "http://localhost:5000/aeroporti/FCO/voli_verso?arrivo=MXP&durata_max=90"
```

**Response 200:**
```json
[
  {
    "codice": "AZ123",
    "compagnia": "Alitalia",
    "partenza": "FCO",
    "arrivo": "MXP",
    "durata_minuti": 60
  }
]
```


---

## 📝 Struttura Dati

### Nazione
```python
{
  "nome": str,        # Univoco
  "fondazione": int   # Anno
}
```

### Città
```python
{
  "nome": str,          # Univoco
  "abitanti": int,
  "nazione": str        # Riferimento a Nazione
}
```

### Compagnia
```python
{
  "nome": str,          # Univoco
  "fondazione": int,
  "citta": str          # Riferimento a Città
}
```

### Aeroporto
```python
{
  "codice": str,        # Codice IATA, univoco
  "nome": str,
  "citta": str          # Riferimento a Città
}
```

### Volo
```python
{
  "codice": str,        # Univoco
  "compagnia": str,     # Riferimento a Compagnia
  "partenza": str,      # Codice IATA Aeroporto
  "arrivo": str,        # Codice IATA Aeroporto
  "durata_minuti": int
}
```

---

## 🔧 Sviluppo Futuro

- [ ] Implementare database reale (SQLite, PostgreSQL)
- [ ] Autenticazione utenti
- [ ] Frontend completo con React
- [ ] Deploy su cloud

---

## 📚 Risorse Utili

- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [HTTP Methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)
- [REST API Best Practices](https://restfulapi.net/)

---

## 👨‍🏫 Per i Docenti

Questo progetto può essere usato come:
- Esercitazione pratica durante le lezioni
- Progetto finale del corso
- Base per estensioni (aggiungere database, autenticazione, etc.)

### Suggerimenti didattici:
1. Iniziare con i modelli dati
2. Creare gli endpoint API uno per uno
3. Testare con cURL, Postman, o requests
4. Sviluppare il frontend React in parallelo
5. Aggiungere database quando gli studenti comprendono i concetti base

---

## 📄 Licenza

Questo progetto è fornito a scopo didattico. Libero da usare, modificare e distribuire.

---

## ✉️ Contatti

Per domande o suggerimenti, contatta Marco Esposito (`esposito@di.uniroma1.it`).

---

**Buon lavoro! 🚀**

