from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated

from schemas.folder import FolderCreate, FolderUpdate
from schemas.user import UserSchema
from services import folder as folder_svc
from dependencies.db import get_db
from dependencies.user import get_current_verified_user
from dependencies.permission import check_permission

router = APIRouter(
    prefix="/folders",
    tags=["Folder"],
    dependencies=[Depends(get_current_verified_user)],
)


@router.get("/{organization_id}")
def get_folders(
    organization_id: str,
    user: Annotated[UserSchema, Depends(get_current_verified_user)],
    db=Depends(get_db),
):
    try:
        check_permission(db, user, organization_id, "list_folder")
        return folder_svc.get_folders(db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{organization_id}")
def create_folder(
    organization_id: str,
    folder: FolderCreate,
    user: Annotated[UserSchema, Depends(get_current_verified_user)],
    db=Depends(get_db),
):
    try:
        check_permission(db, user, organization_id, "create_folder")
        return folder_svc.create_folder(db, folder)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{organization_id}/{folder_id}")
def update_folder(
    organization_id: str,
    folder_id: str,
    folder: FolderUpdate,
    user: Annotated[UserSchema, Depends(get_current_verified_user)],
    db=Depends(get_db),
):
    try:
        check_permission(db, user, organization_id, "update_folder")
        return folder_svc.update_folder(db, folder_id, folder)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{organization_id}/{folder_id}")
def delete_folder(
    organization_id: str,
    folder_id: str,
    user: Annotated[UserSchema, Depends(get_current_verified_user)],
    db=Depends(get_db),
):
    try:
        check_permission(db, user, organization_id, "delete_folder")
        return folder_svc.delete_folder(db, folder_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
