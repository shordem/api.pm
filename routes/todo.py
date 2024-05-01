from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated

from schemas.todo import TodoCreate, TodoUpdate
from services import todo as todo_svc
from dependencies.db import get_db
from dependencies.user import get_current_verified_user
from dependencies.permission import check_permission

router = APIRouter(
    prefix="/todos",
    tags=["Todo"],
    dependencies=[Depends(get_current_verified_user)],
)


@router.get("/{todo_id}")
def get_todo(todo_id: str, db=Depends(get_db)):
    try:
        return todo_svc.get_todo(db, todo_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{folder_id}")
def get_todos(folder_id: str, db=Depends(get_db)):
    try:
        return todo_svc.get_todos(db, folder_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("")
def create_todo(todo: TodoCreate, db=Depends(get_db)):
    try:
        return todo_svc.create_todo(db, todo)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{todo_id}")
def update_todo(todo_id: str, todo: TodoUpdate, db=Depends(get_db)):
    try:
        todo_svc.get_todo(db, todo_id)
        return todo_svc.update_todo(db, todo)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{todo_id}")
def delete_todo(todo_id: str, db=Depends(get_db)):
    try:
        return todo_svc.delete_todo(db, todo_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
