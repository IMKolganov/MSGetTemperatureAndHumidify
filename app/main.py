# app/main.py

from flask import Flask
from app.routes import bp as routes_bp
import threading
import os

def create_app():
    app = Flask(__name__)

    env = os.getenv('FLASK_ENV', 'development')
    if env == 'development':
        app.config.from_object('app.config.DevelopmentConfig')
    elif env == 'docker':
        app.config.from_object('app.config.DockerConfig')
    else:
        app.config.from_object('app.config.Config')
    
    app.register_blueprint(routes_bp)
    return app

def start_message_processing():
    """Запускает обработку сообщений в отдельном потоке."""
    import app.routes.requests as requests
    processing_thread = threading.Thread(target=requests.start_processing)
    processing_thread.daemon = True
    processing_thread.start()

app = create_app()
