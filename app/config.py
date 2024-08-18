# app/config.py

class Config:
    RABBITMQ_HOST = 'localhost'
    REQUEST_QUEUE_NAME = 'temperatureRequestQueue'
    RESPONSE_QUEUE_NAME = 'temperatureResponseQueue'
    MICROCONTROLLER_MANAGER_URL = 'http://localhost:4000'  # URL для обращения к Microservice MicrocontrollerManager