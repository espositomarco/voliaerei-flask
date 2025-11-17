import requests
# va installato con 'pip install requests'

import json
if __name__ == "__main__":
    headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }

    response = requests.get(url="http://localhost:5000/",
                            headers=headers)

    print(response.json())

    # TEST 1 - GET /nazioni
    print(f"\n\n{"="*10} TEST 1 - GET /nazioni {"="*10}")

    nazioni_response = requests.get(url="http://localhost:5000/nazioni",
                                    headers=headers)

    print(json.dumps(nazioni_response.json(), indent=4))