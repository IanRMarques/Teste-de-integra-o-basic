from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from pathlib import Path

# Configuração da API
app = FastAPI(
    title="API de Tarefas Pessoais",
    description="Uma API simples para gerenciar suas tarefas do dia a dia",
    version="1.0.0"
)

# Banco de dados em memória
todos = []

# Modelos Pydantic
class Todo(BaseModel):
    id: int
    task: str
    completed: bool = False

class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    suggestion: str | None = None

# Carrega o template HTML
def load_html_template():
    template_path = Path(__file__).parent / "templates" / "home.html"
    with open(template_path, "r", encoding="utf-8") as file:
        return file.read()

# Rotas da API
@app.get("/", response_class=HTMLResponse)
def welcome_message():
    """Retorna a página inicial com documentação interativa"""
    return load_html_template()

@app.get("/todos", response_model=List[Todo])
def list_todos():
    """Retorna todas as tarefas cadastradas"""
    return todos

@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(todo: Todo):
    """Cria uma nova tarefa"""
    if any(t.id == todo.id for t in todos):
        raise HTTPException(
            status_code=400,
            detail={
                "message": f"Já existe uma tarefa com o ID {todo.id}",
                "suggestion": "Use um ID diferente ou atualize a tarefa existente"
            }
        )
    todos.append(todo)
    return todo

@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    """Busca uma tarefa específica por ID"""
    for todo in todos:
        if todo.id == todo_id:
            return todo
    
    raise HTTPException(
        status_code=404,
        detail={
            "message": f"Tarefa com ID {todo_id} não encontrada",
            "suggestion": "Verifique a lista completa em /todos ou crie uma nova tarefa"
        }
    )

# Tratamento de erros
@app.exception_handler(HTTPException)
async def custom_error_handler(request, exc):
    """Transforma erros em respostas amigáveis"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail.get("message", "Algo deu errado"),
            "suggestion": exc.detail.get("suggestion", "Tente novamente mais tarde")
        }
    )
