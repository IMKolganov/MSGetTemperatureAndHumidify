# routes.py
from flask import Blueprint, request, jsonify
import random
from .utils import fetch_webservice_data
from .rabbitmq import RabbitMQ

main_bp = Blueprint('main', __name__)

# Инициализация RabbitMQ
rabbitmq = RabbitMQ()

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
            }
        }
        return jsonify(random_data), 200
    
    try:
        data = fetch_webservice_data()
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

    result = {
        'webservice_data': data,
    }
    return jsonify(result), 200

@main_bp.route('/send-request', methods=['POST'])
def send_request():
    request_data = request.json
    queue_name = request_data.get('queue_name', 'temperatureQueue')
    response_queue = request_data.get('response_queue', 'temperatureResponseQueue')
    message = request_data.get('message', {})

    try:
        rabbitmq.send_message(queue_name, message)
        response = rabbitmq.get_message(response_queue, message['requestId'], timeout=30)
        return jsonify(response), 200
    except TimeoutError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({'status': 'ok'}), 200
