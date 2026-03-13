from fastapi.testclient import TestClient
from app.main import app
from fastapi import status

client = TestClient(app)


def test_healthcheck():
    resp = client.get("/")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == {"status_code": status.HTTP_200_OK, "detail": "ok", "result": "working"}
