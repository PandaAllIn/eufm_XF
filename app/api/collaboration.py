from flask import Blueprint

collaboration_bp = Blueprint("collaboration", __name__, url_prefix="/api/collaboration")

@collaboration_bp.get("/health")
def health() -> dict:
    """Health check endpoint for collaboration service."""
    return {"status": "ok"}


def register_socketio(socketio):
    """Register Socket.IO event handlers for collaboration namespace."""

    @socketio.on("connect", namespace="/ws")
    def handle_connect():  # pragma: no cover - simple event handler
        pass

    @socketio.on("disconnect", namespace="/ws")
    def handle_disconnect():  # pragma: no cover - simple event handler
        pass

    @socketio.on("message", namespace="/ws")
    def handle_message(data):
        socketio.emit("message", data, namespace="/ws")
