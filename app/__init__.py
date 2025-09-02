from flask import Flask, jsonify
from config.settings import get_settings
from config.logging import setup_logging
from app.utils.ai_services import AIServices
from app.exceptions import EUFMAssistantException
from app.api.collaboration import bp as collaboration_bp


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

    # Register API blueprints
    app.register_blueprint(collaboration_bp)

    print("Flask App Created and Configured with Logging and Error Handling.")

    return app
