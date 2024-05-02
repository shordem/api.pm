from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated

from schemas.note import NoteCreate, NoteUpdate
from schemas.user import UserSchema
from services import note as note_svc
from dependencies.db import get_db
from dependencies.user import get_current_verified_user
from dependencies.permission import check_permission

router = APIRouter(
    prefix="/notes",
    tags=["Note"],
    dependencies=[Depends(get_current_verified_user)],
)


@router.get("/{organization_id}/{note_id}/view")
def get_note(
    organization_id: str,
    note_id: str,
    user: Annotated[UserSchema, Depends(get_current_verified_user)],
    db=Depends(get_db),
):
    try:
        # check_permission(db, user, organization_id, "view_task")
        return note_svc.get_note(db, note_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{organization_id}/{folder_id}")
def get_notes(
    organization_id: str,
    folder_id: str,
    user: Annotated[UserSchema, Depends(get_current_verified_user)],
    db=Depends(get_db),
):
    try:
        check_permission(db, user, organization_id, "list_task")
        return note_svc.get_notes(db, folder_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{organization_id}/{folder_id}")
def create_note(
    organization_id: str,
    folder_id: str,
    note: NoteCreate,
    user: Annotated[UserSchema, Depends(get_current_verified_user)],
    db=Depends(get_db),
):
    try:
        check_permission(db, user, organization_id, "create_task")
        note_svc.create_note(db, folder_id, user.id, note)
        return {"detail": "Note created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{organization_id}/{note_id}")
def update_note(
    organization_id: str,
    note_id: str,
    note: NoteUpdate,
    user: Annotated[UserSchema, Depends(get_current_verified_user)],
    db=Depends(get_db),
):
    try:
        check_permission(db, user, organization_id, "update_task")
        note_svc.get_note(db, note_id)
        note_svc.update_note(db, note_id, note)
        return {"detail": "Note updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{organization_id}/{note_id}")
def delete_note(
    organization_id: str,
    note_id: str,
    user: Annotated[UserSchema, Depends(get_current_verified_user)],
    db=Depends(get_db),
):
    try:
        check_permission(db, user, organization_id, "delete_task")
        note_svc.delete_note(db, note_id)
        return {"detail": "Note deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
