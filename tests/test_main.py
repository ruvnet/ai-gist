from fastapi.testclient import TestClient
from app.app import app

client = TestClient(app)

def test_create_gist():
    response = client.post("/gists", json={
        "description": "Test Gist",
        "public": True,
        "files": [{"filename": "test.txt", "content": "Hello World"}]
    })
    assert response.status_code == 200
    assert response.json()["description"] == "Test Gist"

def test_update_gist():
    gist_id = "existing_gist_id"
    response = client.patch(f"/gists/{gist_id}", json={
        "description": "Updated Gist",
        "files": [{"filename": "test.txt", "content": "Updated Content"}]
    })
    assert response.status_code == 200
    assert response.json()["description"] == "Updated Gist"
