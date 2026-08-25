from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db, TaskDB


app = FastAPI()


# Allow your frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# What the frontend sends when creating a task
class TaskCreate(BaseModel):
    name: str


# What the frontend can send when updating a task
class TaskUpdate(BaseModel):
    name: str | None = None
    completed: bool | None = None


@app.get("/")
def read_root():
    return {"message": "Welcome to our TO-DO web"}


# GET ALL TASKS
@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(TaskDB).all()

    return [
        {
            "id": task.idtasks,
            "name": task.name,
            "completed": task.completed
        }
        for task in tasks
    ]


# ADD TASK
@app.post("/tasks")
def add_task(task: TaskCreate, db: Session = Depends(get_db)):

    new_task = TaskDB(
        name=task.name,
        completed=False
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "message": "Task added",
        "task": {
            "id": new_task.idtasks,
            "name": new_task.name,
            "completed": new_task.completed
        }
    }


# UPDATE TASK
@app.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db)
):

    existing_task = db.query(TaskDB).filter(
        TaskDB.idtasks == task_id
    ).first()

    if existing_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task.name is not None:
        existing_task.name = task.name

    if task.completed is not None:
        existing_task.completed = task.completed

    db.commit()
    db.refresh(existing_task)

    return {
        "message": "Task updated",
        "task": {
            "id": existing_task.idtasks,
            "name": existing_task.name,
            "completed": existing_task.completed
        }
    }


# DELETE TASK
@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    existing_task = db.query(TaskDB).filter(
        TaskDB.idtasks == task_id
    ).first()

    if existing_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(existing_task)
    db.commit()

    return {
        "message": "Task deleted"
    }