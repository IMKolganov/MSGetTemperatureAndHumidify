from flask import Blueprint, request, jsonify
import requests
import random
from .utils import fetch_webservice_data, process_microcontroller_data

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    return jsonify({'service': 'Microservice GetTemperatureAndHumidify'}), 200

@main_bp.route('/get-temperature-and-humidify', methods=['GET'])
def get_temperature_and_humidify():
    is_dev = request.args.get('isDev') == '1'
    
    if is_dev:
        # Генерация случайных данных для режима разработки
        random_data = {
            'webservice_data': {
                'temperature': round(random.uniform(-20.0, 40.0), 2),
                'humidity': round(random.uniform(0.0, 100.0), 2)
            },
            'microcontroller_data': {
                'status': 'available',
                'connection_type': 'wifi',
                'version': '1.0'
            }
        }
        return jsonify(random_data), 200
    
    try:
        # Получение данных от первого веб-сервиса
        data = fetch_webservice_data()
        # Обработка данных и запрос к MicrocontrollerManager
        microcontroller_data = process_microcontroller_data(data)
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

    # Возвращаем объединённые данные
    result = {
        'webservice_data': data,
        'microcontroller_data': microcontroller_data
    }
    return jsonify(result), 200

@main_bp.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({'status': 'ok'}), 200


# docker stop ms-get-temp-and-humd-container || true && \
# docker rm ms-get-temp-and-humd-container || true && \
# docker build -t ms-get-temp-and-humd . && \
# docker run -d -p 5000:5000 --name ms-get-temp-and-humd-container ms-get-temp-and-humd
