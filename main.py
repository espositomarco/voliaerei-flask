from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def initial_message():
    return jsonify({"response":'Questo è il messaggio di benvenuto'})

if __name__ == "__main__":
    app.run(debug=True)