from collections import namedtuple

from flask import Flask, jsonify, request

from data_model.nazione import Nazione
from db.utils import load_data_from_db, store_data_on_db, load_nazioni, load_citta, nazioni_info

app = Flask(__name__)

db = namedtuple("mockup_db", "nazioni citta")


db.nazioni = load_nazioni()
db.citta = load_citta(db.nazioni)
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
    '''dati = load_data_from_db()
    print(dati['Nazione'])
    if nome not in dati['Nazione']:
        return jsonify({"error": f"La nazione con nome {nome} non esiste!"}), 404
    nazione: dict[str, str] = dati['Nazione'][nome]
    return jsonify(nazione), 200'''
    try:
        nazione: Nazione = app.mockup_db.nazioni[nome]
        return jsonify(nazione.info()), 200

    except KeyError:
        return jsonify({"error": f"La nazione con nome {nome} non esiste!"}), 404


@app.route('/citta', methods=['GET'])
def get_all_citta():
    dati = load_data_from_db()
    citta: dict[str, dict[str, str | int]] = dati['Citta']
    return jsonify(citta), 200

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
        return jsonify({"errore": "Per creare una nazione, fornire il nome!"}), 400

    if new_nazione_dict["nome"] in app.mockup_db.nazioni:
        return jsonify({"errore": f"Esiste gia' una nazione con nome {new_nazione_dict['nome']}!"}), 400

    # fine validazione dell'input


    new_nazione_obj: Nazione = Nazione(nome=new_nazione_dict["nome"],
                                       fondazione=new_nazione_dict["fondazione"])
    app.mockup_db.nazioni[new_nazione_obj.nome] = new_nazione_obj

    return jsonify(new_nazione_obj.info()), 201



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