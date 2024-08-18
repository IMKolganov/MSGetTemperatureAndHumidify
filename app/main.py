# app/main.py

from flask import Flask
from app.routes import bp as routes_bp
import threading

def create_app():
    app = Flask(__name__)
    app.register_blueprint(routes_bp)
    return app

def start_message_processing():
    """Запускает обработку сообщений в отдельном потоке."""
    import app.routes.requests as requests
    processing_thread = threading.Thread(target=requests.start_processing)
    processing_thread.daemon = True
    processing_thread.start()

app = create_app()

if __name__ == '__main__':
    start_message_processing()  # Запуск обработки сообщений
    app.run(debug=True, host='0.0.0.0', port=5000)
