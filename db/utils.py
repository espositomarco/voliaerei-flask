import json
import os

from data_model.aeroporto import Aeroporto
from data_model.citta import Citta
from data_model.compagnia import Compagnia
from data_model.custom_types import CodiceIATA, CodiceVolo
from data_model.nazione import Nazione
from data_model.volo import Volo

current_dir = os.path.curdir
MOCKUP_DB_JSON_FILENAME = os.path.join(current_dir, "db", "mockup_db.json")

def load_data_from_db() -> dict:
    with open(MOCKUP_DB_JSON_FILENAME) as f:
        return json.load(f)

def store_data_on_db(data) -> None:
    with open(MOCKUP_DB_JSON_FILENAME, "w+") as f:
        json.dump(data, f, indent=4)


def load_nazioni() -> dict[str, 'Nazione']:
    with open(MOCKUP_DB_JSON_FILENAME) as f:
        data = json.load(f)
    nazioni_dict = data["Nazione"]

    result: dict[str, Nazione] = dict()

    for nazione_nome, nazione_dict in nazioni_dict.items():
        nazione: Nazione = Nazione(nome=nazione_dict["nome"],
                                   fondazione=nazione_dict["fondazione"])
        result[nazione_nome] = nazione

    return result

def store_nazione(nazione: Nazione) -> None:
    dati = load_data_from_db()
    # devo controllare se la nazione c'è già
    # se sì, la cancello
    nazioni_dict = dati["Nazione"]
    if nazione.nome() in nazioni_dict:
        nazioni_dict.pop(nazione.nome())

    nazione_info: dict[str, str] = nazione.info()

    nazioni_dict[nazione.nome()] = nazione_info
    store_data_on_db(dati)

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

def load_compagnie(all_citta: dict[str, Citta]) -> dict[str, Compagnia]:
    dati = load_data_from_db()

    compagnie_dict: dict[str, dict[str, int | str]] = dati["Compagnia"]

    result: dict[str, Compagnia] = dict()
    for compagnia_dict in compagnie_dict.values():

        citta: Citta = all_citta[compagnia_dict["citta"]]
        compagnia: Compagnia = Compagnia(nome=compagnia_dict["nome"],
                             fondazione=compagnia_dict["fondazione"],
                             citta=citta)
        result[compagnia.nome()] = compagnia

    return result

def load_aeroporti(all_citta: dict[str, Citta]) -> dict[str, Aeroporto]:
    dati = load_data_from_db()

    aeroporti_dict: dict[str, dict[str, int | str]] = dati["Aeroporto"]

    result: dict[str, Aeroporto] = dict()
    for aeroporto_dict in aeroporti_dict.values():

        citta: Citta = all_citta[aeroporto_dict["citta"]]
        aeroporto: Aeroporto = Aeroporto(
            codice=aeroporto_dict["codice"],
            nome=aeroporto_dict["nome"],
            citta=citta)
        result[aeroporto.codice()] = aeroporto

    return result


def load_voli(all_aeroporti: dict[str, Aeroporto], all_compagnie: dict[str, Compagnia]) -> dict[str, Volo]:
    dati = load_data_from_db()

    voli_dict: dict[str, dict[str, int | str]] = dati["Volo"]

    result: dict[str, Volo] = dict()
    for volo_dict in voli_dict.values():

        compagnia: Compagnia = all_compagnie[volo_dict["compagnia"]]
        partenza: Aeroporto = all_aeroporti[volo_dict["partenza"]]
        arrivo: Aeroporto = all_aeroporti[volo_dict["arrivo"]]
        volo: Volo = Volo(
            codice=volo_dict["codice"],
            durata=volo_dict["durata_minuti"],
            compagnia=compagnia,
            partenza=partenza,
            arrivo=arrivo)
        result[volo.codice()] = volo

    return result

def store_citta(citta: Citta) -> None:
    dati = load_data_from_db()
    # devo controllare se la citta c'è già
    # se sì, la cancello
    citta_dict = dati["Citta"]
    if citta.nome() in citta_dict:
        citta_dict.pop(citta.nome())

    citta_info: dict[str, str] = citta.info()

    citta_dict[citta.nome()] = citta_info
    store_data_on_db(dati)


def store_compagnia(compagnia: Compagnia) -> None:
    dati = load_data_from_db()
    # devo controllare se la compagnia c'è già
    # se sì, la cancello
    compagnie_dict = dati["Compagnia"]
    if compagnia.nome() in compagnie_dict:
        compagnie_dict.pop(compagnia.nome())

    compagnia_info: dict[str, str] = compagnia.info()

    compagnie_dict[compagnia.nome()] = compagnia_info
    store_data_on_db(dati)


def store_aeroporto(aeroporto: Aeroporto) -> None:
    dati = load_data_from_db()
    # devo controllare se l'aeroporto c'è già
    # se sì, la cancello
    aeroporti_dict = dati["Aeroporto"]
    if aeroporto.nome() in aeroporti_dict:
        aeroporti_dict.pop(aeroporto.codice())

    aeroporto_info: dict[str, str] = aeroporto.info()

    aeroporti_dict[aeroporto.codice()] = aeroporto_info
    store_data_on_db(dati)


def store_volo(volo: Volo) -> None:
    dati = load_data_from_db()
    voli_dict = dati["Volo"]
    if volo.codice() in voli_dict:
        voli_dict.pop(volo.codice())

    volo_info: dict[str, str] = volo.info()
    voli_dict[volo.codice()] = volo_info
    store_data_on_db(dati)

def nazioni_info(nazioni: dict[str, Nazione]) -> dict[str, dict[str, int | str]]:
    result: dict[str, dict[str, int | str]] = dict()
    for nazione in nazioni.values():
        result[nazione.nome()] = nazione.info()
    return result


def all_citta_info(citta: dict[str, Citta]) -> dict[str, dict[str, int | str]]:
    result: dict[str, dict[str, int | str]] = dict()
    for c in citta.values():
        result[c.nome()] = c.info()
    return result

def compagnie_info(compagnie: dict[str, Compagnia]) -> dict[str, dict[str, int | str]]:
    result: dict[str, dict[str, int | str]] = dict()
    for c in compagnie.values():
        result[c.nome()] = c.info()
    return result

def aeroporti_info(aeroporti: dict[str, Aeroporto]) -> dict[str, dict[str, CodiceIATA | str]]:
    result: dict[str, dict[str, CodiceIATA | str]] = dict()
    for a in aeroporti.values():
        result[a.codice()] = a.info()
    return result

def voli_info(voli: dict[str, Volo]) -> dict[str, dict[str, int | str | CodiceVolo]]:
    result: dict[str, dict[str, int| CodiceVolo | str]] = dict()
    for v in voli.values():
        result[v.codice()] = v.info()
    return result

