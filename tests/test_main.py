import pytest
from fastapi.testclient import TestClient
from app.main import app, todos

client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_todos():
    """Limpa a lista de todos antes de cada teste"""
    todos.clear()

def test_welcome_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "API de Tarefas Pessoais" in response.text

def test_list_empty_todos():
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []

def test_create_todo():
    response = client.post(
        "/todos",
        json={"id": 1, "task": "Estudar pytest", "completed": False}
    )
    assert response.status_code == 201
    assert response.json()["task"] == "Estudar pytest"

def test_create_duplicate_todo():
    # Primeira criação
    client.post("/todos", json={"id": 1, "task": "Tarefa 1", "completed": False})
    
    # Tentativa de duplicação
    response = client.post(
        "/todos",
        json={"id": 1, "task": "Tarefa duplicada", "completed": True}
    )
    assert response.status_code == 400
    assert "Já existe uma tarefa" in response.json()["message"]

def test_get_todo():
    # Cria tarefa de teste
    test_todo = {"id": 2, "task": "Tarefa para buscar", "completed": True}
    client.post("/todos", json=test_todo)
    
    # Busca
    response = client.get("/todos/2")
    assert response.status_code == 200
    assert response.json()["task"] == "Tarefa para buscar"
    assert response.json()["completed"] is True

def test_get_nonexistent_todo():
    response = client.get("/todos/999")
    assert response.status_code == 404
    assert "não encontrada" in response.json()["message"]

def test_delete_todo():
    # Cria tarefa para deletar
    client.post("/todos", json={"id": 3, "task": "Tarefa para deletar", "completed": False})
    
    # Deleta
    response = client.delete("/todos/3")
    assert response.status_code == 200
    assert "removida" in response.json()["message"]
    
    # Verifica se foi removida
    response = client.get("/todos/3")
    assert response.status_code == 404

def test_delete_nonexistent_todo():
    response = client.delete("/todos/999")
    assert response.status_code == 404
