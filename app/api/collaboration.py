from flask import Blueprint, jsonify, request

from app.services.status_buffer import get_status_updates

bp = Blueprint("collaboration", __name__, url_prefix="/api/collaboration")


@bp.get("/agent_status")
def agent_status() -> tuple:
    """Return the most recent agent status updates.

    Query Parameters
    ----------------
    limit: int, optional
        Number of records to return. Defaults to 10.
    """
    try:
        limit = int(request.args.get("limit", 10))
    except ValueError:
        limit = 10
    updates = get_status_updates(limit)
    return jsonify({"updates": updates}), 200
