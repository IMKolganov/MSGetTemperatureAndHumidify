import pika
import json
import random
from flask import Blueprint, request, jsonify
from app.config import Config

bp = Blueprint('requests', __name__)

def get_rabbitmq_connection():
    """Создает соединение с RabbitMQ и возвращает канал и соединение."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=Config.RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=Config.REQUEST_QUEUE_NAME, durable=False, exclusive=False, auto_delete=False)
    channel.queue_declare(queue=Config.RESPONSE_QUEUE_NAME, durable=False, exclusive=False, auto_delete=False)
    return connection, channel

@bp.route('/send_request', methods=['POST'])
def send_request():
    """Отправляет запрос в очередь RabbitMQ."""
    data = request.json
    correlation_id = data.get('correlationId')
    if not correlation_id:
        return jsonify({'error': 'CorrelationId is required'}), 400

    connection, channel = get_rabbitmq_connection()
    message = json.dumps({'methodName': 'get-temperature-and-humidify', 'isRandom': True})
    channel.basic_publish(
        exchange='',
        routing_key=Config.REQUEST_QUEUE_NAME,
        body=message,
        properties=pika.BasicProperties(
            correlation_id=correlation_id
        )
    )
    connection.close()
    return jsonify({'message': 'Request sent'}), 200

def process_message(ch, method, properties, body):
    """Функция обратного вызова для обработки сообщений из очереди RabbitMQ."""
    request_data = json.loads(body)
    method_name = request_data.get('MethodName')
    correlation_id = properties.correlation_id

    print(f"Received message: {request_data} with CorrelationId: {correlation_id}")

    if method_name == 'get-temperature-and-humidify':
        temperature = round(random.uniform(0, 100), 2)
        humidity = round(random.uniform(0, 100), 2)

        response_message = {
            'temperature': temperature,
            'humidity': humidity
        }
        response_json = json.dumps(response_message)

        ch.basic_publish(
            exchange='',
            routing_key=Config.RESPONSE_QUEUE_NAME,
            body=response_json,
            properties=pika.BasicProperties(
                correlation_id=correlation_id
            )
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        error_message = {
            'error': f"Unknown methodName: {method_name}"
        }
        error_json = json.dumps(error_message)

        print(f"Unknown methodName received: {method_name}. Sending error response.")

        ch.basic_publish(
            exchange='',
            routing_key=Config.RESPONSE_QUEUE_NAME,
            body=error_json,
            properties=pika.BasicProperties(
                correlation_id=correlation_id
            )
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)

def start_processing():
    """Запускает прослушиватель очереди для обработки сообщений."""
    connection, channel = get_rabbitmq_connection()
    channel.basic_consume(
        queue=Config.REQUEST_QUEUE_NAME,
        on_message_callback=process_message,
        auto_ack=False
    )

    print("Processing messages...")
    channel.start_consuming()
