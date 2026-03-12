from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_healthcheck():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"status_code": 200, "detail": "ok", "result": "working"}
