# app/routes/get_temperature_and_humidify.py

from flask import jsonify
from . import bp
import random

@bp.route('/get-temperature-and-humidify')
def get_temperature_and_humidify():
    # Генерация случайных данных
    temperature = round(random.uniform(0, 100), 2)
    humidity = round(random.uniform(0, 100), 2)
    
    response_message = {
        'temperature': temperature,
        'humidity': humidity
    }
    
    return jsonify(response_message)