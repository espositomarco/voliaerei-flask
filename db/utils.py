import json
import os

from data_model.classes import Nazione

current_dir = os.path.curdir
MOCKUP_DB_INIT_JSON_FILENAME = os.path.join(current_dir, "db", "mockup_db_init.json")
MOCKUP_DB_JSON_FILENAME = os.path.join(current_dir, "db", "mockup_db.json")

def load_data_from_db() -> dict:
    with open(MOCKUP_DB_JSON_FILENAME) as f:
        return json.load(f)

def store_data_on_db(data) -> None:
    with open(MOCKUP_DB_JSON_FILENAME, "w+") as f:
        json.dump(data, f, indent=4)


def get_nazioni_from_db() -> dict[str, Nazione]:
    all_data = load_data_from_db()
    nazioni_dict: dict[str, dict[str, str]] = all_data['Nazione']

    result: dict[str, Nazione] = dict()
    for nazione_dict in nazioni_dict.values():
        nazione = Nazione(nome=nazione_dict['nome'])

        result[nazione.nome()] = nazione
    return result

def inser_nazione_on_db(nazione: Nazione) -> None:
    dati = load_data_from_db()
    dati["Nazione"][nazione.nome()] = nazione.info()
    store_data_on_db(dati)
