from collections import namedtuple

from flask import Flask, jsonify, request

from data_model.aeroporto import Aeroporto
from data_model.citta import Citta
from data_model.compagnia import Compagnia
from data_model.custom_types import CodiceVolo
from data_model.nazione import Nazione
import db.utils as db_utils
from data_model.volo import Volo

app = Flask(__name__)

db = namedtuple("mockup_db", "nazioni citta compagnie aeroporti voli")


db.nazioni = db_utils.load_nazioni()
db.citta = db_utils.load_citta(db.nazioni)
db.compagnie = db_utils.load_compagnie(db.citta)

db.aeroporti = db_utils.load_aeroporti(db.citta)
db.voli = db_utils.load_voli(db.aeroporti, db.compagnie)


app.mockup_db = db

@app.route('/')
def initial_message():
    return jsonify({"response":'Questo è il messaggio di benvenuto'})

@app.route('/all', methods=['GET'])
def get_all():
    dati = db_utils.load_data_from_db() # Carica TUTTI i dati dal finto database nel file json
    return jsonify(dati), 200

@app.route('/nazioni', methods=['GET'])
def get_nazioni():
    # dati = load_data_from_db()
    # nazioni: dict[str, dict[str, str]] = dati['Nazione']

    nazioni: dict[str, Nazione] =  app.mockup_db.nazioni
    all_nazioni_info = db_utils.nazioni_info(nazioni)
    return jsonify(all_nazioni_info), 200

@app.route('/nazioni/<string:nome>', methods=['GET'])
def get_nazione(nome:str):
    try:
        nazione: Nazione = app.mockup_db.nazioni[nome]
        return jsonify(nazione.as_dict()), 200

    except KeyError:
        return jsonify({"error": f"La nazione con nome {nome} non esiste!"}), 404

@app.route('/nazioni', methods=['POST'])
def add_nazione():

    new_nazione_dict: dict = request.get_json() #prendo il body della richiesta come json
    # inizio validazione dell'input
    if "nome" not in new_nazione_dict or not isinstance(new_nazione_dict["nome"], str) :
        return jsonify({"errore": "Per creare una nazione, fornire il nome, una stringa!"}), 400
    elif "fondazione" not in new_nazione_dict:
        return jsonify({"errore": "Per creare una nazione, fornire l'anno di fondazione!"}), 400


    if new_nazione_dict["nome"] in app.mockup_db.nazioni:
        return jsonify({"errore": f"Esiste gia' una nazione con nome {new_nazione_dict['nome']}!"}), 400

    # fine validazione dell'input

    new_nazione_obj: Nazione = Nazione(nome=new_nazione_dict["nome"],
                                       fondazione=new_nazione_dict["fondazione"])

    app.mockup_db.nazioni[new_nazione_obj.nome()] = new_nazione_obj

    return jsonify(new_nazione_obj.info()), 201

@app.route('/nazioni/<string:nome>', methods=['PATCH'])
def update_nazione(nome: str):
    # inizio validazione dell'input
    new_nazione_dict: dict = request.get_json() #prendo il body della richiesta come json
    if "nome" in new_nazione_dict:
        return jsonify({"errore": "Il nome della nazione non è modificabile!"}), 400
    elif "fondazione" not in new_nazione_dict:
        return jsonify({"errore": "Per modificare una nazione, fornire il nuovo anno di fondazione!"}), 400

    elif nome not in app.mockup_db.nazioni:
        return jsonify({"errore": f"Non esiste una nazione con nome {nome}!"}), 404

    # fine validazione dell'input

    naz: Nazione = app.mockup_db.nazioni[nome]
    naz.set_fondazione(new_nazione_dict["fondazione"])

    return jsonify(naz.info()), 200


@app.route('/nazioni/piuvecchia', methods=['GET'])
def nazione_piuvecchia():
    pass

@app.route('/citta', methods=['GET'])
def get_all_citta():

    all_citta: dict[str, Citta] = app.mockup_db.citta
    citta_info = db_utils.all_citta_info(all_citta)
    return jsonify(citta_info), 200

@app.route('/citta/<string:nome_citta>', methods=['GET'])
def get_citta(nome_citta: str):

    try:
        citta: Citta = app.mockup_db.citta[nome_citta]
        return jsonify(citta.as_dict()), 200
    except KeyError as e:
        return (jsonify({"errore": f"La citta con nome {nome_citta} non esiste! "
                                  f"Errore da python: KeyError: {str(e)}"})
                    , 404)

@app.route('/citta', methods=['POST'])
def add_citta():
    # inizio validazione dell'input
    new_citta_dict: dict = request.get_json() #prendo il body della richiesta come json
    if "nome" not in new_citta_dict:
        return jsonify({"errore": "Per creare una citta, fornire il nome!"}), 400
    elif "abitanti" not in new_citta_dict:
        return jsonify({"errore": "Per creare una citta, fornire il numero di abitanti!"}), 400
    elif "nazione" not in new_citta_dict:
        return jsonify({"errore": "Per creare una citta, fornire la nazione!"}), 400

    elif new_citta_dict["nome"] in app.mockup_db.citta:
        return jsonify({"errore": f"Esiste gia' una citta con nome {new_citta_dict['nome']}!"}), 400

    elif new_citta_dict["nazione"] not in app.mockup_db.nazioni:
        return jsonify({"errore": f"Non esiste una nazione con nome {new_citta_dict['nazione']}!"}), 404
    # fine validazione dell'input

    nazione: Nazione = app.mockup_db.nazioni[new_citta_dict['nazione']]


    new_citta_obj: Citta = Citta(nome=new_citta_dict["nome"],
                                abitanti=new_citta_dict["abitanti"],
                                 nazione=nazione)

    app.mockup_db.citta[new_citta_obj.nome()] = new_citta_obj

    return jsonify(new_citta_obj.info()), 201


@app.route('/citta/<string:nome>', methods=['PATCH'])
def update_citta(nome: str):
    # inizio validazione dell'input
    new_citta_dict: dict = request.get_json() #prendo il body della richiesta come json
    if "nome" in new_citta_dict:
        return jsonify({"errore": "Il nome della citta' non è modificabile!"}), 400
    elif "abitanti" not in new_citta_dict and "nazione" not in new_citta_dict:
        return jsonify({"errore": "Per modificare una citta, fornire il nuovo numero "
                                  "di abitanti e/o la nuova nazione!"}), 400

    elif nome not in app.mockup_db.citta:
        return jsonify({"errore": f"Non esiste una citta' con nome {nome}!"}), 404
    # fine validazione input

    citta: Citta = app.mockup_db.citta[nome]

    # fine validazione dell'input
    if "abitanti" in new_citta_dict:
        citta.set_abitanti(new_citta_dict["abitanti"])
    if "nazione" in new_citta_dict:
        new_nazione: Nazione = app.mockup_db.nazioni[new_citta_dict['nazione']]
        citta.set_nazione(new_nazione)

    return jsonify(citta.info()), 200

@app.route('/compagnie', methods=['GET'])
def get_compagnie():
    compagnie: dict[str, Compagnia] = app.mockup_db.compagnie
    return jsonify(db_utils.compagnie_info(compagnie)), 200


@app.route('/compagnie/<string:nome>', methods=['GET'])
def get_compagnia(nome:str):
    try:
        compagnia: Compagnia = app.mockup_db.compagnie[nome]
        return jsonify(compagnia.as_dict()), 200

    except KeyError:
        return jsonify({"error": f"La compagnia con nome {nome} non esiste!"}), 404


@app.route('/compagnie', methods=['POST'])
def add_compagnia():
    # inizio validazione dell'input
    new_compagnia_dict: dict = request.get_json() #prendo il body della richiesta come json
    if "nome" not in new_compagnia_dict:
        return jsonify({"errore": "Per creare una compagnia, fornire il nome!"}), 400
    elif "fondazione" not in new_compagnia_dict:
        return jsonify({"errore": "Per creare una compagnia, fornire l'anno di fondazione!"}), 400
    elif "citta" not in new_compagnia_dict:
        return jsonify({"errore": "Per creare una compagnia, fornire la citta' dove ha sede!"}), 400

    elif new_compagnia_dict["nome"] in app.mockup_db.compagnie:
        return jsonify({"errore": f"Esiste gia' una compagnia con nome {new_compagnia_dict['nome']}!"}), 400

    elif new_compagnia_dict["citta"] not in app.mockup_db.citta:
        return jsonify({"errore": f"Non esiste una citta' con nome {new_compagnia_dict['nazione']}!"}), 404
    # fine validazione dell'input

    citta: Citta = app.mockup_db.citta[new_compagnia_dict['citta']]


    new_compagnia_obj: Compagnia = Compagnia(nome=new_compagnia_dict["nome"],
                                fondazione=new_compagnia_dict["fondazione"],
                                 citta=citta)

    app.mockup_db.compagnie[new_compagnia_obj.nome()] = new_compagnia_obj

    return jsonify(new_compagnia_obj.info()), 201


@app.route('/compagnie/<string:nome>', methods=['PATCH'])
def update_compagnia(nome: str):
    # inizio validazione dell'input
    new_compagnia_dict: dict = request.get_json() #prendo il body della richiesta come json
    if "nome" in new_compagnia_dict or "fondazione" in new_compagnia_dict:
        return jsonify({"errore": "Il nome della compagnia e il suo anno di fondazione non sono modificabili!"}), 400
    elif "citta" not in new_compagnia_dict:
        return jsonify({"errore": "Per modificare una compagnia fornire la nuova citta'!"}), 400
    elif nome not in app.mockup_db.compagnie:
        return jsonify({"errore": f"Non esiste una compagnia con nome {nome}!"}), 404
    elif new_compagnia_dict["citta"] not in app.mockup_db.citta:
        return jsonify({"errore": f"Non esiste una citta' con nome {nome}!"}), 404
    # fine validazione input

    compagnia: Compagnia = app.mockup_db.compagnie[nome]

    # fine validazione dell'input
    citta: Citta = app.mockup_db.citta[new_compagnia_dict['citta']]
    compagnia.set_citta(citta)

    return jsonify(compagnia.info()), 200

















@app.route('/aeroporti', methods=['GET'])
def get_aeroporti():
    aeroporti: dict[str, Aeroporto] = app.mockup_db.aeroporti
    return jsonify(db_utils.aeroporti_info(aeroporti)), 200


@app.route('/aeroporti/<string:codice>', methods=['GET'])
def get_aeroporto(codice:str):
    try:
        aeroporto: Aeroporto = app.mockup_db.aeroporti[codice]
        return jsonify(aeroporto.as_dict()), 200

    except KeyError:
        return jsonify({"error": f"L'aeroporto con codice IATA {codice} non esiste!"}), 404


@app.route('/aeroporti', methods=['POST'])
def add_aeroporto():
    # inizio validazione dell'input
    new_aeroporto_dict: dict = request.get_json() #prendo il body della richiesta come json
    if "nome" not in new_aeroporto_dict:
        return jsonify({"errore": "Per creare un aeroporto, fornire il nome!"}), 400
    elif "codice" not in new_aeroporto_dict:
        return jsonify({"errore": "Per creare un aeroporto, fornire il codice IATA!"}), 400
    elif "citta" not in new_aeroporto_dict:
        return jsonify({"errore": "Per creare un aeroporto, fornire la citta'!"}), 400

    elif new_aeroporto_dict["codice"] in app.mockup_db.aeroporti:
        return jsonify({"errore": f"Esiste gia' un aeroporto con codice {new_aeroporto_dict['codice']}!"}), 400

    elif new_aeroporto_dict["citta"] not in app.mockup_db.citta:
        return jsonify({"errore": f"Non esiste una citta' con nome {new_aeroporto_dict['citta']}!"}), 404
    # fine validazione dell'input

    citta: Citta = app.mockup_db.citta[new_aeroporto_dict['citta']]


    new_aeroporto_obj: Aeroporto = Aeroporto(codice=new_aeroporto_dict['codice'],
                                             nome=new_aeroporto_dict["nome"],
                                             citta=citta)

    app.mockup_db.aeroporti[new_aeroporto_obj.codice()] = new_aeroporto_obj

    return jsonify(new_aeroporto_obj.as_dict()), 201


@app.route('/aeroporti/<string:codice>', methods=['PATCH'])
def update_aeroporto(codice: str):
    # inizio validazione dell'input
    new_aeroporto_dict: dict = request.get_json() #prendo il body della richiesta come json
    if "codice" in new_aeroporto_dict or "citta" in new_aeroporto_dict:
        return jsonify({"errore": "Il codice dell'aeroporto e la sua citta' non sono modificabili!"}), 400
    elif "nome" not in new_aeroporto_dict:
        return jsonify({"errore": "Per modificare un aeroporto fornire il nuovo nome!"}), 400
    elif codice not in app.mockup_db.aeroporti:
        return jsonify({"errore": f"Non esiste un aeroporto con codice {codice}!"}), 404

    # fine validazione input

    aeroporto: Aeroporto = app.mockup_db.aeroporti[codice]

    # fine validazione dell'input
    aeroporto.set_nome(new_aeroporto_dict["nome"])

    return jsonify(aeroporto.as_dict()), 200

























@app.route('/voli', methods=['GET'])
def get_voli():
    voli: dict[str, Volo] = app.mockup_db.voli
    return jsonify(db_utils.voli_info(voli)), 200


@app.route('/voli/<string:codice>', methods=['GET'])
def get_volo(codice:str | CodiceVolo):
    try:
        volo: Volo = app.mockup_db.voli[codice]
        return jsonify(volo.as_dict()), 200

    except KeyError:
        return jsonify({"error": f"Il volo con codice {codice} non esiste!"}), 404


@app.route('/voli', methods=['POST'])
def add_volo():
    # inizio validazione dell'input
    new_volo_dict: dict = request.get_json() #prendo il body della richiesta come json

    if "codice" not in new_volo_dict:
        return jsonify({"errore": "Per creare un volo, fornire il codice!"}), 400
    elif "compagnia" not in new_volo_dict:
        return jsonify({"errore": "Per creare un volo, fornire il nome della compagnia'!"}), 400
    elif "partenza" not in new_volo_dict:
        return jsonify({"errore": "Per creare un volo, fornire il codice IATA dell'aeroporto di partenza'!"}), 400
    elif "arrivo" not in new_volo_dict:
        return jsonify({"errore": "Per creare un volo, fornire il codice IATA dell'aeroporto di arrivo'!"}), 400
    elif "durata_minuti" not in new_volo_dict:
        return jsonify({"errore": "Per creare un volo, fornire la durata in minuti'!"}), 400

    elif new_volo_dict["codice"] in app.mockup_db.voli:
        return jsonify({"errore": f"Esiste gia' un aeroporto con codice {new_volo_dict['codice']}!"}), 400


    elif new_volo_dict["compagnia"] not in app.mockup_db.compagnie:

        return jsonify({"errore": f"Non esiste una compagnia con nome {new_volo_dict['compagnia']}!"}), 404

    elif new_volo_dict["partenza"] not in app.mockup_db.aeroporti:
        return jsonify({"errore": f"Non esiste un aeroporto con codice IATA {new_volo_dict['partenza']}!"}), 404

    elif new_volo_dict["arrivo"] not in app.mockup_db.aeroporti:
        return jsonify({"errore": f"Non esiste un aeroporto con codice IATA {new_volo_dict['arrivo']}!"}), 404
    # fine validazione dell'input

    compagnia: Compagnia = app.mockup_db.compagnie[new_volo_dict['compagnia']]
    partenza: Aeroporto = app.mockup_db.aeroporti[new_volo_dict['partenza']]
    arrivo: Aeroporto = app.mockup_db.aeroporti[new_volo_dict['arrivo']]


    new_volo_obj: Volo = Volo(codice=new_volo_dict['codice'],
                              durata=new_volo_dict['durata_minuti'],
                              compagnia=compagnia,
                              partenza=partenza,
                              arrivo=arrivo)

    app.mockup_db.voli[new_volo_obj.codice()] = new_volo_obj

    return jsonify(new_volo_obj.as_dict()), 201


'''@app.route('/voli', methods=['GET'])
def get_voli():
    dati = db_utils.load_data_from_db()
    voli: dict[str, dict[str, str | int]] = dati['Volo']
    return jsonify(voli), 200
'''
if __name__ == "__main__":
    app.run(debug=True)