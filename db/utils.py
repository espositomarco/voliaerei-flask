import json
import os

from data_model.citta import Citta
from data_model.nazione import Nazione

current_dir = os.path.curdir
MOCKUP_DB_INIT_JSON_FILENAME = os.path.join(current_dir, "db", "mockup_db_init.json")
MOCKUP_DB_JSON_FILENAME = os.path.join(current_dir, "db", "mockup_db.json")

def load_data_from_db() -> dict:
    with open(MOCKUP_DB_JSON_FILENAME) as f:
        return json.load(f)

def store_data_on_db(data) -> None:
    with open(MOCKUP_DB_JSON_FILENAME, "w+") as f:
        json.dump(data, f, indent=4)


def load_nazioni() -> dict[str, Nazione]:
    with open(MOCKUP_DB_INIT_JSON_FILENAME) as f:
        data = json.load(f)
    nazioni_dict = data["Nazione"]

    result: dict[str, Nazione] = dict()

    for nazione_nome, nazione_dict in nazioni_dict.items():
        nazione: Nazione = Nazione(nazione_dict["nome"])
        result[nazione_nome] = nazione

    return result

def load_citta(nazioni: dict[str, Nazione]) -> dict[str, Citta]:
    dati = load_data_from_db()

    all_citta_dict: dict[str, dict[str, int | str]] = dati["Citta"]

    result: dict[str, Citta] = dict()
    for citta_dict in all_citta_dict.values():
        nazione: Nazione = nazioni[citta_dict["nazione"]]
        citta: Citta = Citta(nome=citta_dict["nome"],
                             abitanti=citta_dict["n_abitanti"],
                             nazione=nazione)
        result[citta.nome()] = citta

    return result