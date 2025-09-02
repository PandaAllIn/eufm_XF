from app import create_app
from app.services.status_buffer import add_status_update, clear_status_updates


def test_agent_status_endpoint_returns_latest_updates():
    app = create_app()
    client = app.test_client()

    clear_status_updates()
    add_status_update({"agent": "alpha", "status": "Queued", "message": "ready"})
    add_status_update({"agent": "beta", "status": "Running", "message": "processing"})

    response = client.get("/api/collaboration/agent_status?limit=1")
    assert response.status_code == 200
    data = response.get_json()
    assert "updates" in data
    assert len(data["updates"]) == 1
    assert data["updates"][0]["agent"] == "beta"
