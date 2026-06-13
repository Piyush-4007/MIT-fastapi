from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Temporary storage
todos = []

# Todo Model
class Todo(BaseModel):
    id: int
    title: str
    description: str
    completed: bool


# Create Todo
@app.post("/todos")
def create_todo(todo: Todo):

    # Check if ID already exists
    for existing_todo in todos:
        if existing_todo.id == todo.id:
            raise HTTPException(
                status_code=400,
                detail="Todo ID already exists"
            )

    todos.append(todo)

    return {
        "message": "Todo created successfully",
        "data": todo
    }


# Get All Todos
@app.get("/todos")
def get_all_todos():
    return todos


# Get Todo By ID
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):

    for todo in todos:
        if todo.id == todo_id:
            return todo

    raise HTTPException(
        status_code=404,
        detail="Todo not found"
    )


# Update Todo
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: Todo):

    for index, todo in enumerate(todos):
        if todo.id == todo_id:

            todos[index] = updated_todo

            return {
                "message": "Todo updated successfully",
                "data": updated_todo
            }

    raise HTTPException(
        status_code=404,
        detail="Todo not found"
    )


# Delete Todo
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):

    for index, todo in enumerate(todos):
        if todo.id == todo_id:

            deleted_todo = todos.pop(index)

            return {
                "message": "Todo deleted successfully",
                "data": deleted_todo
            }

    raise HTTPException(
        status_code=404,
        detail="Todo not found"
    )