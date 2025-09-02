from flask import Blueprint, Response, current_app, jsonify, request

bp = Blueprint("collaboration", __name__, url_prefix="/api/collaboration")


@bp.get("/chat")
def get_chat() -> Response:
    limit = request.args.get("limit", default=50, type=int)
    messages = current_app.chat_service.latest(limit)
    return jsonify(messages)
