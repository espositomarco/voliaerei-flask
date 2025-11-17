from flask import Flask, jsonify

from db.utils import load_data_from_db
app = Flask(__name__)

@app.route('/')
def initial_message():
    return jsonify({"response":'Questo è il messaggio di benvenuto'})

@app.route('/all', methods=['GET'])
def get_all():
    dati = load_data_from_db() # Carica TUTTI i dati dal finto database nel file json
    return jsonify(dati), 200

@app.route('/nazioni', methods=['GET'])
def get_nazioni():
    dati = load_data_from_db()
    nazioni: dict[str, dict[str, str]] = dati['Nazione']
    return jsonify(nazioni), 200

@app.route('/nazioni/<string:nome>', methods=['GET'])
def get_nazione(nome:str):
    dati = load_data_from_db()
    print(dati['Nazione'])
    if nome not in dati['Nazione']:
        return jsonify({"error": f"La nazione con nome {nome} non esiste!"}), 404
    nazione: dict[str, str] = dati['Nazione'][nome]
    return jsonify(nazione), 200

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


def add_nazione

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