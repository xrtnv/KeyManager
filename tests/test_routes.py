import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_generate_secret():
    response = client.post("/generate", json={"secret": "mysecret", "passphrase": "mypassword", "ttl": 60})
    assert response.status_code == 200
    assert "secret_key" in response.json()


def test_get_secret():
    generate_response = client.post("/generate", json={"secret": "mysecret", "passphrase": "mypassword", "ttl": 60})
    secret_key = generate_response.json()["secret_key"]
    get_response = client.get(f"/secrets/{secret_key}", params={"passphrase": "mypassword"})
    assert get_response.status_code == 200
    assert get_response.json()["secret"] == "mysecret"
