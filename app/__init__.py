from flask import Flask, jsonify
from config.settings import get_settings
from config.logging import setup_logging
from app.utils.ai_services import AIServices
from app.services.agent_factory import AgentFactory
from app.exceptions import EUFMAssistantException


def create_app():
    """Application factory for creating Flask app instances."""

    # Initialize logging
    setup_logging()

    app = Flask(__name__)

    # Load configuration
    settings = get_settings()
    app.config["APP_SETTINGS"] = settings

    # Initialize AI services and agent factory
    ai_services = AIServices(settings.ai.dict())
    agent_factory = AgentFactory(ai_services, settings.ai.dict())
    app.ai_services = ai_services
    app.agent_factory = agent_factory
    app.config["AGENT_FACTORY"] = agent_factory

    # Register a simple root route for health checks
    @app.route("/")
    def index():
        return "EUFM Assistant is running."

    # Register global error handler
    @app.errorhandler(EUFMAssistantException)
    def handle_app_exception(error):
        response = jsonify(error.to_dict())
        response.status_code = 400  # Or a more specific code
        return response

    print("Flask App Created and Configured with Logging and Error Handling.")

    return app
