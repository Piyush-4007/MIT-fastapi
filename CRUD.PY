from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

todos = []

class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False  # default False so HTML doesn't need to send it


@app.post("/todos")
def create_todo(todo: Todo):
    for existing in todos:
        if existing.id == todo.id:
            raise HTTPException(status_code=400, detail="Todo ID already exists")
    todos.append(todo)
    return {"message": "Todo created successfully", "data": todo}


@app.get("/todos")
def get_all_todos():
    return todos


@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: Todo):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[index] = updated_todo
            return {"message": "Todo updated successfully", "data": updated_todo}
    raise HTTPException(status_code=404, detail="Todo not found")


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            deleted = todos.pop(index)
            return {"message": "Todo deleted successfully", "data": deleted}
    raise HTTPException(status_code=404, detail="Todo not found")