# Documentazione API REST - Sistema Voli

## Base URL

```
http://localhost:5000/
```

---

## Endpoints Generali

### GET /

**Descrizione:** Messaggio di benvenuto.

**Response 200:**
```json
{
  "response": "Questo è il messaggio di benvenuto"
}
```

---

### GET /all

**Descrizione:** Restituisce tutti i dati presenti nel database mock.

**Response 200:**
```json
{
  "Nazione": { ... },
  "Citta": { ... },
  "Compagnia": { ... },
  "Aeroporto": { ... },
  "Volo": { ... }
}
```

---

## Nazioni

### GET /nazioni

**Descrizione:** Restituisce la lista di tutte le nazioni.

**Response 200:**
```json
[
  {
    "nome": "Italia",
    "fondazione": 1861
  }
]
```

---

### GET /nazioni/{nome}

**Descrizione:** Restituisce i dettagli di una nazione specifica.

| Parametro | Tipo   | Descrizione        | Obbligatorio |
|-----------|--------|-------------------|--------------|
| nome      | string | Nome della nazione | Sì           |

**Response 200:**
```json
{
  "nome": "Italia",
  "fondazione": 1861
}
```

**Response 404:**
```json
{
  "error": "La nazione con nome Italia non esiste!"
}
```

---

### POST /nazioni

**Descrizione:** Crea una nuova nazione.

**Body JSON:**
```json
{
  "nome": "Italia",
  "fondazione": 1861
}
```

| Campo      | Tipo | Descrizione        | Obbligatorio |
|------------|------|-------------------|--------------|
| nome       | str  | Nome della nazione | Sì           |
| fondazione | int  | Anno di fondazione | Sì           |

**Response 201:**
```json
{
  "nome": "Italia",
  "fondazione": 1861
}
```

**Response 400:**
```json
{
  "errore": "Per creare una nazione, fornire il nome, una stringa!"
}
```

---

### PATCH /nazioni/{nome}

**Descrizione:** Aggiorna l'anno di fondazione di una nazione.

| Parametro | Tipo   | Descrizione        | Obbligatorio |
|-----------|--------|-------------------|--------------|
| nome      | string | Nome della nazione | Sì           |

**Body JSON:**
```json
{
  "fondazione": 1861
}
```

**Response 200:**
```json
{
  "nome": "Italia",
  "fondazione": 1861
}
```

**Response 400:**
```json
{
  "errore": "Il nome della nazione non è modificabile!"
}
```

**Response 404:**
```json
{
  "errore": "Non esiste una nazione con nome Italia!"
}
```

---

## Città

### GET /citta

**Descrizione:** Restituisce la lista di tutte le città.

**Response 200:**
```json
[
  {
    "nome": "Roma",
    "abitanti": 2873000,
    "nazione": "Italia"
  }
]
```

---

### GET /citta/{nome_citta}

**Descrizione:** Restituisce i dettagli di una città specifica.

| Parametro   | Tipo   | Descrizione      | Obbligatorio |
|-------------|--------|-----------------|--------------|
| nome_citta  | string | Nome della città | Sì           |

**Response 200:**
```json
{
  "nome": "Roma",
  "abitanti": 2873000,
  "nazione": "Italia"
}
```

**Response 404:**
```json
{
  "errore": "La citta con nome Roma non esiste!"
}
```

---

### POST /citta

**Descrizione:** Crea una nuova città.

**Body JSON:**
```json
{
  "nome": "Roma",
  "abitanti": 2873000,
  "nazione": "Italia"
}
```

| Campo    | Tipo   | Descrizione           | Obbligatorio |
|----------|--------|----------------------|--------------|
| nome     | string | Nome della città      | Sì           |
| abitanti | int    | Numero di abitanti    | Sì           |
| nazione  | string | Nome della nazione    | Sì           |

**Response 201:**
```json
{
  "nome": "Roma",
  "abitanti": 2873000,
  "nazione": "Italia"
}
```

**Response 400:**
```json
{
  "errore": "Per creare una citta, fornire il nome!"
}
```

**Response 404:**
```json
{
  "errore": "Non esiste una nazione con nome Italia!"
}
```

---

### PATCH /citta/{nome}

**Descrizione:** Aggiorna una città.

| Parametro | Tipo   | Descrizione      | Obbligatorio |
|-----------|--------|-----------------|--------------|
| nome      | string | Nome della città | Sì           |

**Body JSON:**
```json
{
  "abitanti": 3000000,
  "nazione": "Francia"
}
```

**Response 200:**
```json
{
  "nome": "Roma",
  "abitanti": 3000000,
  "nazione": "Francia"
}
```

**Response 400:**
```json
{
  "errore": "Il nome della citta' non è modificabile!"
}
```

**Response 404:**
```json
{
  "errore": "Non esiste una citta' con nome Roma!"
}
```

---

## Compagnie

### GET /compagnie

**Descrizione:** Restituisce la lista di tutte le compagnie.

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

---

### GET /compagnie/{nome}

**Descrizione:** Restituisce i dettagli di una compagnia specifica.

| Parametro | Tipo   | Descrizione          | Obbligatorio |
|-----------|--------|----------------------|--------------|
| nome      | string | Nome della compagnia | Sì           |

**Response 200:**
```json
{
  "nome": "Alitalia",
  "fondazione": 1946,
  "citta": "Roma"
}
```

**Response 404:**
```json
{
  "error": "La compagnia con nome Alitalia non esiste!"
}
```

---

### POST /compagnie

**Descrizione:** Crea una nuova compagnia.

**Body JSON:**
```json
{
  "nome": "Alitalia",
  "fondazione": 1946,
  "citta": "Roma"
}
```

| Campo      | Tipo   | Descrizione           | Obbligatorio |
|------------|--------|----------------------|--------------|
| nome       | string | Nome della compagnia  | Sì           |
| fondazione | int    | Anno di fondazione    | Sì           |
| citta      | string | Nome della città      | Sì           |

**Response 201:**
```json
{
  "nome": "Alitalia",
  "fondazione": 1946,
  "citta": "Roma"
}
```

**Response 400:**
```json
{
  "errore": "Per creare una compagnia, fornire il nome!"
}
```

**Response 404:**
```json
{
  "errore": "Non esiste una citta' con nome Roma!"
}
```

---

### PATCH /compagnie/{nome}

**Descrizione:** Aggiorna la città di sede di una compagnia.

| Parametro | Tipo   | Descrizione          | Obbligatorio |
|-----------|--------|----------------------|--------------|
| nome      | string | Nome della compagnia | Sì           |

**Body JSON:**
```json
{
  "citta": "Milano"
}
```

**Response 200:**
```json
{
  "nome": "Alitalia",
  "fondazione": 1946,
  "citta": "Milano"
}
```

**Response 400:**
```json
{
  "errore": "Il nome della compagnia e il suo anno di fondazione non sono modificabili!"
}
```

**Response 404:**
```json
{
  "errore": "Non esiste una compagnia con nome Alitalia!"
}
```

---

## Aeroporti

### GET /aeroporti

**Descrizione:** Restituisce la lista di tutti gli aeroporti.

**Response 200:**
```json
[
  {
    "nome": "Fiumicino",
    "codice": "FCO",
    "citta": "Roma"
  }
]
```

---

### GET /aeroporti/{codice}

**Descrizione:** Restituisce i dettagli di un aeroporto specifico.

| Parametro | Tipo   | Descrizione           | Obbligatorio |
|-----------|--------|----------------------|--------------|
| codice    | string | Codice IATA aeroporto | Sì           |

**Response 200:**
```json
{
  "nome": "Fiumicino",
  "codice": "FCO",
  "citta": "Roma"
}
```

**Response 404:**
```json
{
  "error": "L'aeroporto con codice IATA FCO non esiste!"
}
```

---

### POST /aeroporti

**Descrizione:** Crea un nuovo aeroporto.

**Body JSON:**
```json
{
  "nome": "Fiumicino",
  "codice": "FCO",
  "citta": "Roma"
}
```

| Campo | Tipo   | Descrizione           | Obbligatorio |
|-------|--------|----------------------|--------------|
| nome  | string | Nome aeroporto        | Sì           |
| codice| string | Codice IATA           | Sì           |
| citta | string | Nome della città      | Sì           |

**Response 201:**
```json
{
  "nome": "Fiumicino",
  "codice": "FCO",
  "citta": "Roma"
}
```

**Response 400:**
```json
{
  "errore": "Per creare un aeroporto, fornire il nome!"
}
```

**Response 404:**
```json
{
  "errore": "Non esiste una citta' con nome Roma!"
}
```

---

### PATCH /aeroporti/{codice}

**Descrizione:** Aggiorna il nome di un aeroporto.

| Parametro | Tipo   | Descrizione           | Obbligatorio |
|-----------|--------|----------------------|--------------|
| codice    | string | Codice IATA aeroporto | Sì           |

**Body JSON:**
```json
{
  "nome": "Fiumicino Nuovo"
}
```

**Response 200:**
```json
{
  "nome": "Fiumicino Nuovo",
  "codice": "FCO",
  "citta": "Roma"
}
```

**Response 400:**
```json
{
  "errore": "Il codice dell'aeroporto e la sua citta' non sono modificabili!"
}
```

**Response 404:**
```json
{
  "errore": "Non esiste un aeroporto con codice FCO!"
}
```

---

## Voli

### GET /voli

**Descrizione:** Restituisce la lista di tutti i voli.

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

### GET /voli/{codice}

**Descrizione:** Restituisce i dettagli di un volo specifico.

| Parametro | Tipo   | Descrizione | Obbligatorio |
|-----------|--------|------------|--------------|
| codice    | string | Codice volo | Sì           |

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

**Response 404:**
```json
{
  "error": "Il volo con codice AZ123 non esiste!"
}
```

---

### POST /voli

**Descrizione:** Crea un nuovo volo.

**Body JSON:**
```json
{
  "codice": "AZ123",
  "compagnia": "Alitalia",
  "partenza": "FCO",
  "arrivo": "MXP",
  "durata_minuti": 60
}
```

| Campo         | Tipo   | Descrizione                      | Obbligatorio |
|---------------|--------|----------------------------------|--------------|
| codice        | string | Codice volo                      | Sì           |
| compagnia     | string | Nome compagnia                   | Sì           |
| partenza      | string | Codice IATA aeroporto partenza  | Sì           |
| arrivo        | string | Codice IATA aeroporto arrivo    | Sì           |
| durata_minuti | int    | Durata in minuti                 | Sì           |

**Response 201:**
```json
{
  "codice": "AZ123",
  "compagnia": "Alitalia",
  "partenza": "FCO",
  "arrivo": "MXP",
  "durata_minuti": 60
}
```

**Response 400:**
```json
{
  "errore": "Per creare un volo, fornire il codice!"
}
```

**Response 404:**
```json
{
  "errore": "Non esiste una compagnia con nome Alitalia!"
}
```

---

## Calcolo Voli

### GET /calcola_voli_tra_nazioni

**Descrizione:** Restituisce i voli disponibili tra due nazioni.

**Query Parameters:**

| Parametro | Tipo   | Descrizione               | Obbligatorio |
|-----------|--------|---------------------------|--------------|
| partenza  | string | Nome nazione di partenza  | Sì           |
| arrivo    | string | Nome nazione di arrivo    | Sì           |

**Response 200:**
```json
[
  {
    "codice": "AZ123",
    "compagnia": "Alitalia",
    "partenza": "FCO",
    "arrivo": "CDG",
    "durata_minuti": 120
  }
]
```

**Response 404:**
```json
{
  "errore": "Assicurarsi che le nazioni specificate esistano!"
}
```

---

### GET /calcola_voli_tra_citta

**Descrizione:** Restituisce i voli disponibili tra due città.

**Query Parameters:**

| Parametro | Tipo   | Descrizione           | Obbligatorio |
|-----------|--------|------------------------|--------------|
| partenza  | string | Nome città di partenza | Sì           |
| arrivo    | string | Nome città di arrivo   | Sì           |

**Response 200:**
```json
[
  {
    "codice": "AZ123",
    "compagnia": "Alitalia",
    "partenza": "FCO",
    "arrivo": "CDG",
    "durata_minuti": 120
  }
]
```

**Response 404:**
```json
{
  "errore": "Assicurarsi che le citta' specificate esistano!"
}
```

---

### GET /aeroporti/{codice}/voli_verso

**Descrizione:** Restituisce i voli da un aeroporto ad un altro, con filtro opzionale sulla durata.

| Parametro | Tipo   | Descrizione                    | Obbligatorio |
|-----------|--------|--------------------------------|--------------|
| codice    | string | Codice IATA aeroporto partenza | Sì           |

**Query Parameters:**

| Parametro | Tipo | Descrizione                 | Obbligatorio |
|-----------|------|-----------------------------| --------------|
| arrivo    | str  | Codice IATA aeroporto arrivo| Sì           |
| durata_max| int  | Durata massima in minuti    | No           |

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

**Response 404:**
```json
{
  "errore": "Assicurarsi che l'aeroporto di partenza specificato esista!"
}
```

---

## Codici di Stato HTTP

| Codice | Descrizione                              |
|--------|------------------------------------------|
| 200    | OK - Richiesta completata con successo   |
| 201    | Created - Risorsa creata con successo    |
| 400    | Bad Request - Errore nei dati inviati    |
| 404    | Not Found - Risorsa non trovata          |

---

## Note Importanti

- Tutti i parametri nei path devono corrispondere esattamente (case-sensitive, salvo dove specificato).
- I query parameters per calcolo voli tra nazioni/città vengono automaticamente capitalizzati.
- Per il calcolo voli tra aeroporti, il parametro `arrivo` viene convertito a maiuscolo.
- Le città e nazioni sono identificate dal nome (univoco).
- Gli aeroporti sono identificati dal codice IATA (univoco).
- I voli sono identificati dal codice volo (univoco).
