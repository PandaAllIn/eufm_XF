from flask import Flask, jsonify
from flask_socketio import SocketIO
from pathlib import Path

from config.settings import get_settings
from config.logging import setup_logging
from app.utils.ai_services import AIServices
from app.exceptions import EUFMAssistantException
from app.services.chat_service import ChatService

socketio = SocketIO()


def create_app():
    """Application factory for creating Flask app instances."""

    # Initialize logging
    setup_logging()

    app = Flask(__name__)

    # Load configuration
    settings = get_settings()
    app.config["APP_SETTINGS"] = settings

    # Initialize AI services
    ai_services = AIServices(settings.ai.dict())
    app.ai_services = ai_services

    # Initialize chat service
    chat_service = ChatService(Path(".state/chat.jsonl"))
    app.chat_service = chat_service

    # Register API blueprints
    from app.api import init_app as init_api

    init_api(app)

    # Register a simple root route for health checks
    @app.route("/")
    def index():
        return "EUFM Assistant is running."

    # Register global error handler
    @app.errorhandler(EUFMAssistantException)
    def handle_app_exception(error):
        app.logger.error(f"{error.__class__.__name__}: {error}")
        response = jsonify(error.to_dict())
        response.status_code = 400  # Or a more specific code
        return response

    socketio.init_app(app, cors_allowed_origins="*")

    print("Flask App Created and Configured with Logging and Error Handling.")

    return app


@socketio.on("message", namespace="/ws")
def handle_message(data):
    from flask import current_app

    if not isinstance(data, dict):
        return
    user = data.get("user")
    text = data.get("text")
    if not user or not text:
        return
    msg = {"user": user, "text": text}
    current_app.chat_service.append(msg)
    socketio.emit("message", msg, namespace="/ws")
