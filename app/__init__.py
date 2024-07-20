from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        # Регистрация маршрутов
        from . import routes
        app.register_blueprint(routes.main_bp)
    
    return app
