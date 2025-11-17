from flask import Flask, jsonify

from db.utils import load_data_from_db

app = Flask(__name__)

@app.route('/')
def initial_message():
    return jsonify({"response":'Questo è il messaggio di benvenuto'})

@app.route('/nazioni', methods=['GET'])
def get_nazioni():
    dati = load_data_from_db() # Carica TUTTI i dati dal finto database nel file json
    nazioni: dict[str, dict[str, str]] = dati['Nazione']
    return jsonify(nazioni), 200

if __name__ == "__main__":
    app.run(debug=True)