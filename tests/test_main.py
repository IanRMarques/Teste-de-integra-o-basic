from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_todos():
    response = client.get("/todos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_todo():
    new_todo = {"id": 1, "task": "Estudar FastAPI", "completed": False}
    response = client.post("/todos", json=new_todo)
    assert response.status_code == 200
    assert response.json()["task"] == "Estudar FastAPI"

def test_get_todo_not_found():
    response = client.get("/todos/999")
    assert response.status_code == 404