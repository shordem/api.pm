from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from schemas.todo import TodoCreate, TodoUpdate
from schemas.user import UserSchema
from services import todo as todo_svc
from dependencies.db import get_db
from dependencies.user import get_current_verified_user
from dependencies.permission import check_permission

router = APIRouter(
    prefix="/todos",
    tags=["Todo"],
    dependencies=[Depends(get_current_verified_user)],
)


@router.get("/{organization_id}/{todo_id}/view")
def get_todo(
    organization_id: str,
    todo_id: str,
    user: Annotated[UserSchema, Depends(get_current_verified_user)],
    db=Depends(get_db),
):
    try:
        return todo_svc.get_todo(db, todo_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{organization_id}/{folder_id}")
def get_todos(
    organization_id: str,
    folder_id: str,
    user: Annotated[UserSchema, Depends(get_current_verified_user)],
    db=Depends(get_db),
):
    try:
        check_permission(db, user, organization_id, "list_task")
        return todo_svc.get_todos(db, folder_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{organization_id}/{folder_id}")
def create_todo(
    organization_id: str,
    folder_id: str,
    todo: TodoCreate,
    user: Annotated[UserSchema, Depends(get_current_verified_user)],
    db=Depends(get_db),
):
    try:
        check_permission(db, user, organization_id, "create_task")
        todo_svc.create_todo(db, folder_id, user.id, todo)
        return {"detail": "Todo created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{organization_id}/{todo_id}")
def update_todo(
    organization_id: str,
    todo_id: str,
    todo: TodoUpdate,
    user: Annotated[UserSchema, Depends(get_current_verified_user)],
    db=Depends(get_db),
):
    try:
        check_permission(db, user, organization_id, "update_task")
        todo_svc.get_todo(db, todo_id)
        todo_svc.update_todo(db, todo_id, todo)
        return {"detail": "Todo updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{organization_id}/{todo_id}")
def delete_todo(
    organization_id: str,
    todo_id: str,
    user: Annotated[UserSchema, Depends(get_current_verified_user)],
    db=Depends(get_db),
):
    try:
        check_permission(db, user, organization_id, "delete_task")
        todo_svc.delete_todo(db, todo_id)
        return {"detail": "Todo deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
