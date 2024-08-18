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

def handle_signal(signum, frame):
    print('Received signal:', signum)
    # Perform cleanup if needed
    sys.exit(0)

def start_message_processing(app):
    """Starts message processing in a separate thread with application context."""
    import app.routes.requests as requests
    processing_thread = threading.Thread(target=requests.start_processing, args=(app,))
    processing_thread.daemon = True
    processing_thread.start()
    print("Message processing thread started")

app = create_app()