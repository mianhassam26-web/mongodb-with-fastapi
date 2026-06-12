# python -m uvicorn main:app --reload
from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# MongoDB Connection
client = MongoClient(os.getenv("MONGO_URL"))
db = client["todo_db"]
collection = db["todos"]

# ---------------- MODELS ---------------- #

class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False


class TodoUpdate(BaseModel):
    title: str = None
    completed: bool = None


# ---------------- CREATE TODO ---------------- #

@app.post("/todos")
def create_todo(todo: Todo):
    collection.insert_one(todo.model_dump())
    return {"message": "Todo created successfully", "data": todo}


# ---------------- GET ALL TODOS ---------------- #

@app.get("/todos")
def get_all_todos():
    return list(collection.find({}, {"_id": 0}))


# ---------------- GET BY ID ---------------- #

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    todo = collection.find_one({"id": todo_id}, {"_id": 0})

    if not todo:
        return {"message": "Todo not found"}

    return todo
# ---------------- GET BY ID ---------------- #
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):

    todo = collection.find_one(
        {"id": todo_id},
        {"_id": 0}
    )

    if not todo:
        return {"message": "Todo not found"}

    return {
        "message": "Todo found successfully",
        "data": todo
    }

# ---------------- UPDATE TODO ---------------- #

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: TodoUpdate):

    update_data = todo.model_dump()

    # None values remove kar do
    update_data = {k: v for k, v in update_data.items() if v is not None}

    if not update_data:
        return {"message": "No data to update"}

    result = collection.update_one(
        {"id": todo_id},
        {"$set": update_data}
    )

    if result.modified_count > 0:
        return {"message": "Todo updated successfully"}

    return {"message": "Todo not found"}


# ---------------- DELETE TODO ---------------- #

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):

    result = collection.delete_one({"id": todo_id})

    if result.deleted_count > 0:
        return {"message": "Todo deleted successfully"}

    return {"message": "Todo not found"}