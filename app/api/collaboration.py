from flask import Blueprint
from flask_socketio import emit

from app import socketio

collaboration_bp = Blueprint("collaboration", __name__)


@socketio.on("message")
def handle_message(data):
    """Broadcast received chat messages to all clients."""
    emit("message", data, broadcast=True)
