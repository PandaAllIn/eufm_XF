from flask import Flask, jsonify
from flask_socketio import SocketIO
from config.settings import get_settings
from config.logging import setup_logging
from app.utils.ai_services import AIServices
from app.exceptions import EUFMAssistantException

socketio = None

def create_app():
    """Application factory for creating Flask app instances."""
    
    # Initialize logging
    setup_logging()
    
    app = Flask(__name__)

    global socketio
    socketio = SocketIO(app, cors_allowed_origins="*")
    
    # Load configuration
    settings = get_settings()
    app.config['APP_SETTINGS'] = settings
    
    # Initialize AI services
    ai_services = AIServices(settings.ai.dict())
    app.ai_services = ai_services
    
    # Register a simple root route for health checks
    @app.route("/")
    def index():
        return "EUFM Assistant is running."

    # Register collaboration API blueprint and Socket.IO handlers
    from app.api.collaboration import collaboration_bp, register_socketio

    app.register_blueprint(collaboration_bp)
    register_socketio(socketio)

    # Register global error handler
    @app.errorhandler(EUFMAssistantException)
    def handle_app_exception(error):
        app.logger.error(f"{error.__class__.__name__}: {error}")
        response = jsonify(error.to_dict())
        response.status_code = 400  # Or a more specific code
        return response

    print("Flask App Created and Configured with Logging and Error Handling.")
    
    return app
