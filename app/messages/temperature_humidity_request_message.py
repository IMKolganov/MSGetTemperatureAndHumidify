# app/messages/temperature_humidity_request_message.py

import json
import uuid
from datetime import datetime

class TemperatureHumidityRequestMessage:
    def __init__(self, request_id = None, method_name="get-temperature-and-humidify", sensor_id = 0, 
                 create_date = None, additional_info = None):
        self.request_id = request_id or str(uuid.uuid4())
        self.method_name = method_name

        self.create_date = create_date or datetime.utcnow().isoformat()
        self.additional_info = additional_info or {}

    def to_dict(self):
        return {
            "RequestId": self.request_id,
            "MethodName": self.method_name,

            "CreateDate": self.create_date,
            "AdditionalInfo": self.additional_info
        }

    def to_json(self):
        return json.dumps(self.to_dict())
