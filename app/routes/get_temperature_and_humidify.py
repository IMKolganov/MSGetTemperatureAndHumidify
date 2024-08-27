# app/routes/get_temperature_and_humidify.py

from flask import jsonify
from . import bp
import random

@bp.route('/get-temperature-and-humidify')
def get_temperature_and_humidify():
    temperature = round(random.uniform(0, 100), 2)
    humidity = round(random.uniform(0, 100), 2)
    
    response_message = {
        'temperature': temperature,
        'humidity': humidity
    }

    #todo: this method must use the service temperature_humidity_service
    
    return jsonify(response_message)