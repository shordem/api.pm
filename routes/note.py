from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated

from schemas.note import NoteCreate, NoteUpdate
from services import note as note_svc
from dependencies.db import get_db
from dependencies.user import get_current_verified_user
from dependencies.permission import check_permission

router = APIRouter(
    prefix="/notes",
    tags=["Note"],
    dependencies=[Depends(get_current_verified_user)],
)


@router.get("/{note_id}")
def get_note(note_id: str, db=Depends(get_db)):
    try:
        return note_svc.get_note(db, note_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{folder_id}")
def get_notes(folder_id: str, db=Depends(get_db)):
    try:
        return note_svc.get_notes(db, folder_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{folder_id}")
def create_note(folder_id: str, note: NoteCreate, db=Depends(get_db)):
    try:
        return note_svc.create_note(db, folder_id, note)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{note_id}")
def update_note(note_id: str, note: NoteUpdate, db=Depends(get_db)):
    try:
        note_svc.get_note(db, note_id)
        return note_svc.update_note(db, note)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{note_id}")
def delete_note(note_id: str, db=Depends(get_db)):
    try:
        return note_svc.delete_note(db, note_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
