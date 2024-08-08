# worker.py
from .rabbitmq import RabbitMQ

def process_message(message):
    print("Received message:", message)
    # Логика обработки сообщения

def main():
    rabbitmq = RabbitMQ()
    rabbitmq.declare_queue('default_queue')
    rabbitmq.receive_message('default_queue', process_message)

if __name__ == '__main__':
    main()
