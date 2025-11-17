import requests
# va installato con 'pip install requests'

import json
headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }

def _show_response(response: requests.Response, n:int = 1):
    print(f"\n\n{"=" * 10} TEST {n} - GET {response.url} {"=" * 10}")
    print(f"\nRESPONSE:\n"
          f"- HTTP Status Code: {response.status_code}\n"
          f"- JSON CONTENT:")
    print(json.dumps(response.json(), indent=4))


def test_get_nazioni():
    # TEST 1 - GET /nazioni
    response = requests.get(url="http://localhost:5000/nazioni", headers=headers)
    _show_response(response, n=1)

def test_get_all_citta():
    # TEST 2 - GET /citta
    response = requests.get(url="http://localhost:5000/citta", headers=headers)
    _show_response(response, n=2)


def test_get_compagnie():
    # TEST 3 - GET /compagnie
    response = requests.get(url="http://localhost:5000/compagnie", headers=headers)
    _show_response(response, n=3)

def test_get_aeroporti():
    # TEST 4 - GET /aeroporti
    response = requests.get(url="http://localhost:5000/aeroporti", headers=headers)
    _show_response(response, n=4)

def test_get_voli():
    # TEST 5 - GET /aeroporti
    response = requests.get(url="http://localhost:5000/voli", headers=headers)
    _show_response(response, n=5)

def test_get_nazione(nome_nazione: str, n:int):
    response = requests.get(url=f"http://localhost:5000/nazioni/{nome_nazione}", headers=headers)
    _show_response(response, n)


def test_get_citta(id_citta: int, n:int):
    response = requests.get(url=f"http://localhost:5000/citta/{id_citta}", headers=headers)
    _show_response(response, n=n)

def test_create_nazione(nome_nazione: str, n:int):
    response = requests.post(url=f"http://localhost:5000/nazioni", headers=headers,
                             json={"nome": nome_nazione})
    _show_response(response, n)

if __name__ == "__main__":
    test_get_nazioni()
    test_get_all_citta()
    test_get_compagnie()
    test_get_aeroporti()
    test_get_voli()
    test_get_nazione("Jamaica", 6)
    test_get_nazione("Francia", 7)
    test_get_citta(165, 8)
    test_create_nazione(nome_nazione="Jamaica", n=9)



