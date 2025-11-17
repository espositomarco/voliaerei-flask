import requests
# va installato con 'pip install requests'

if __name__ == "__main__":
    headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }

    response = requests.get(url="http://localhost:5000/",
                            headers=headers)

    print(response.json())