from sqlalchemy.orm import Session

from models.todo import Todo
from models.user import User
from schemas.todo import TodoCreate, TodoUpdate, TodoSchema
from schemas.user import UserSchema
from .folder import get_folder
from .user import get_user


def get_todo(db: Session, todo_id: str):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise Exception("Todo not found")

    todo_schema = TodoSchema(
        created_by=get_user(db, todo.created_by),
        title=todo.title,
        description=todo.description,
        due_date=todo.due_date,
        completed=todo.completed,
        id=todo.id,
    )

    return todo_schema


def get_todos(db: Session, folder_id: str):
    results = (
        db.query(Todo, User)
        .join(User, User.id == Todo.created_by)
        .filter(Todo.folder_id == folder_id)
        .all()
    )

    todos = []
    for todo, user in results:
        user_data = UserSchema.model_validate(user)
        todo_schema = TodoSchema(
            created_by=user_data,
            title=todo.title,
            description=todo.description,
            due_date=todo.due_date,
            completed=todo.completed,
            id=todo.id,
        )

        todos.append(todo_schema)

    return todos


def create_todo(db: Session, folder_id: str, user_id: str, todo: TodoCreate):
    get_folder(db, folder_id)

    todo = Todo(
        title=todo.title,
        description=todo.description,
        due_date=todo.due_date,
        folder_id=folder_id,
        created_by=user_id,
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def update_todo(db: Session, todo_id: str, todo_update: TodoUpdate):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise Exception("Todo not found")

    todo.title = todo_update.title
    todo.description = todo_update.description
    todo.due_date = todo_update.due_date
    todo.completed = todo_update.completed

    db.commit()
    return todo_update


def delete_todo(db: Session, todo_id: str):
    todo = get_todo(db, todo_id)
    todo_obj = db.query(Todo).filter(Todo.id == todo_id).first()

    db.delete(todo_obj)
    db.commit()
    return todo
