# rabbitmq.py
import pika
import json
import time

class RabbitMQ:
    def __init__(self, host='localhost'):
        self.host = host
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()

    def declare_queue(self, queue_name):
        self.channel.queue_declare(queue=queue_name, durable=True)

    def send_message(self, queue_name, message):
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            ))

    def get_message(self, queue_name, request_id, timeout=30):
        def callback(ch, method, properties, body):
            nonlocal response
            message = json.loads(body)
            if message.get('requestId') == request_id:
                response = message
                ch.basic_ack(delivery_tag=method.delivery_tag)
        
        response = None
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback)

        start_time = time.time()
        while response is None and (time.time() - start_time) < timeout:
            self.connection.process_data_events(time_limit=1)

        if response is None:
            raise TimeoutError("Timeout waiting for response")

        return response

    def close_connection(self):
        self.connection.close()
