from sqlalchemy.orm import Session

from models.folder import Folder
from models.todo import Todo
from schemas.todo import TodoCreate, TodoUpdate, TodoSchema


def get_todo(db: Session, todo_id: str):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise Exception("Todo not found")

    todo_schema = TodoSchema.model_validate(todo)
    return todo_schema


def get_todos(db: Session, folder_id: str):
    todos = db.query(Todo).filter(Todo.folder_id == folder_id).all()
    todos_schema = []
    for todo in todos:
        todos_schema.append(TodoSchema.model_validate(todo))
    return todos_schema


def create_todo(db: Session, todo: TodoCreate):
    todo = Todo(**todo.model_dump())
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def update_todo(db: Session, todo: TodoUpdate):
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def delete_todo(db: Session, todo_id: str):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    db.delete(todo)
    db.commit()
    return todo
