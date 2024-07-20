import requests
from flask import current_app

def fetch_webservice_data():
    webservice_url = 'http://first-webservice-url/api/data'
    response = requests.get(webservice_url)
    response.raise_for_status()
    return response.json()

def process_microcontroller_data(data):
    response = requests.post(
        current_app.config['MICROCONTROLLER_MANAGER_URL'],
        json={'data': data}
    )
    response.raise_for_status()
    return response.json()
