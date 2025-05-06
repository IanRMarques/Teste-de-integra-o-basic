from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="API de Tarefas Pessoais",
    description="Uma API simples para gerenciar suas tarefas do dia a dia",
    version="1.0.0"
)


todos = []


class Todo(BaseModel):
    id: int          
    task: str        
    completed: bool  


class ErrorResponse(BaseModel):
    success: bool = False  
    message: str           
    suggestion: str        

@app.get("/", response_class=HTMLResponse)
def welcome_message():
  
    return """
    <html>
        <head>
            <title>API de Tarefas</title>
            <style>
                body {
                    font-family: 'Arial', sans-serif;
                    line-height: 1.6;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    color: #333;
                }
                h1 {
                    color: #2c3e50;
                    border-bottom: 2px solid #3498db;
                    padding-bottom: 10px;
                }
                .links {
                    margin-top: 30px;
                    background: #f9f9f9;
                    padding: 20px;
                    border-radius: 5px;
                }
                a {
                    color: #3498db;
                    text-decoration: none;
                    font-weight: bold;
                }
                a:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <h1>Página inicial para integração!!</h1>
            <p>Feito para verificar o que acontece por trás do FastApi.</p>
            
            <div class="links">
                <h2>Link:</h2>
                <ul>
                    <li><a href="/docs" target="_blank">/docs</a> - Teste a API diretamente no seu navegador (Swagger UI)</li>
                    <li><a href="/redoc" target="_blank">/redoc</a> - Documentação alternativa (Redoc)</li>
                </ul>
                
                <h2>Endpoints:</h2>
                <ul>
                    <li><strong>GET /todos</strong> - Lista todas as suas tarefas</li>
                    <li><strong>POST /todos</strong> - Adiciona uma nova tarefa</li>
                    <li><strong>GET /todos/{id}</strong> - Busca uma tarefa específica</li>
                </ul>
            </div>
            <p>Desenvolvido por Ian Marques</p>
        </body>
    </html>
    """

#Listar todas as tarefas
@app.get("/todos", response_model=List[Todo])
def list_todos():
    """
    Retorna a lista completa de todas as tarefas cadastradas.
    Se não houver tarefas, retorna uma lista vazia.
    """
    return todos

#Criar nova tarefa
@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(todo: Todo):
    """
    Adiciona uma nova tarefa à sua lista.
    
    Parâmetros:
    - id: Identificador único (não pode repetir)
    - task: Descrição da tarefa (ex: "Lavar o carro")
    - completed: Se já foi concluída (opcional, padrão False)
    
    Retorna a tarefa criada com confirmação.
    """
   
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

#Buscar tarefa por ID
@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    """
    Busca uma tarefa específica pelo seu ID.
    
    Se não encontrar, retorna um erro amigável com sugestões.
    """
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


@app.exception_handler(HTTPException)
async def custom_error_handler(request, exc):
    """
    Transforma erros técnicos em respostas mais amigáveis para os usuários.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail.get("message", "Algo deu errado"),
            "suggestion": exc.detail.get("suggestion", "Tente novamente mais tarde")
        }
    )