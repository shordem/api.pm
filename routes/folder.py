from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated

from schemas.folder import FolderCreate, FolderUpdate
from services import folder as folder_svc
from dependencies.db import get_db
from dependencies.user import get_current_verified_user
from dependencies.permission import check_permission

router = APIRouter(
    prefix="/folders",
    tags=["Folder"],
    dependencies=[Depends(get_current_verified_user)],
)


@router.get("")
def get_folders(db=Depends(get_db)):
    try:
        return folder_svc.get_folders(db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("")
def create_folder(folder: FolderCreate, db=Depends(get_db)):
    try:
        return folder_svc.create_folder(db, folder)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{folder_id}")
def update_folder(folder_id: str, folder: FolderUpdate, db=Depends(get_db)):
    try:
        return folder_svc.update_folder(db, folder_id, folder)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{folder_id}")
def delete_folder(folder_id: str, db=Depends(get_db)):
    try:
        return folder_svc.delete_folder(db, folder_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
