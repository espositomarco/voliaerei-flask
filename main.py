from collections import namedtuple

from flask import Flask, jsonify, request

from data_model.citta import Citta
from data_model.nazione import Nazione
from db.utils import load_data_from_db, store_data_on_db, load_nazioni, load_citta, nazioni_info, all_citta_info

app = Flask(__name__)

db = namedtuple("mockup_db", "nazioni citta")


db.nazioni = load_nazioni()
db.citta = load_citta(db.nazioni)
'''db.compagnie = load_compagnie(db.citta)
db.aeroporti = load_aeroporti(db.citta)
db.voli = load_voli(db.aeroporti, db.compagnie)'''
# TODO carica tutto il resto

app.mockup_db = db

@app.route('/')
def initial_message():
    return jsonify({"response":'Questo è il messaggio di benvenuto'})

@app.route('/all', methods=['GET'])
def get_all():
    dati = load_data_from_db() # Carica TUTTI i dati dal finto database nel file json
    return jsonify(dati), 200

@app.route('/nazioni', methods=['GET'])
def get_nazioni():
    # dati = load_data_from_db()
    # nazioni: dict[str, dict[str, str]] = dati['Nazione']

    nazioni: dict[str, Nazione] =  app.mockup_db.nazioni
    all_nazioni_info = nazioni_info(nazioni)
    return jsonify(all_nazioni_info), 200

@app.route('/nazioni/<string:nome>', methods=['GET'])
def get_nazione(nome:str):
    try:
        nazione: Nazione = app.mockup_db.nazioni[nome]
        return jsonify(nazione.as_dict()), 200

    except KeyError:
        return jsonify({"error": f"La nazione con nome {nome} non esiste!"}), 404


@app.route('/nazioni/piuvecchia', methods=['GET'])
def nazione_piuvecchia():
    pass

@app.route('/citta', methods=['GET'])
def get_all_citta():

    all_citta: dict[str, Citta] = app.mockup_db.citta
    citta_info = all_citta_info(all_citta)
    return jsonify(citta_info), 200

@app.route('/citta/<int:id_citta>', methods=['GET'])
def get_citta(id_citta:int):
    dati = load_data_from_db()
    all_citta: dict[str, dict[str, str]] = dati['Citta']
    try:
        citta = all_citta[str(id_citta)]
        return jsonify(citta), 200
    except KeyError as e:
        return (jsonify({"errore": f"La citta con id {id_citta} non esiste! "
                                  f"Errore da python: KeyError: {str(e)}"})
                    , 404)

@app.route('/nazioni', methods=['POST'])
def add_nazione():
    # inizio validazione dell'input
    new_nazione_dict: dict = request.get_json() #prendo il body della richiesta come json
    if "nome" not in new_nazione_dict:
        return jsonify({"errore": "Per creare una nazione, fornire il nome!"}), 400
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


@app.route('/citta/<string:nome>', methods=['PATCH', 'PUT'])
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



@app.route('/aeroporti', methods=['GET'])
def get_aeroporti():
    dati = load_data_from_db()
    aeroporti: dict[str, dict[str, str | int]] = dati['Aeroporto']
    return jsonify(aeroporti), 200

@app.route('/compagnie', methods=['GET'])
def get_compagnie():
    dati = load_data_from_db()
    compagnie: dict[str, dict[str, str | int]] = dati['Compagnia']
    return jsonify(compagnie), 200

@app.route('/voli', methods=['GET'])
def get_voli():
    dati = load_data_from_db()
    voli: dict[str, dict[str, str | int]] = dati['Volo']
    return jsonify(voli), 200

if __name__ == "__main__":
    app.run(debug=True)