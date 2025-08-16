from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os

socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY","dev")
    from .api.views import bp as api_bp
    app.register_blueprint(api_bp, url_prefix="/api")
    socketio.init_app(app, async_mode="eventlet", message_queue=os.getenv("REDIS_URL"))
    return app
