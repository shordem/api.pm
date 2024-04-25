from sqlalchemy.orm import Session

from models.folder import Folder
from schemas.folder import FolderCreate


def get_folder(db: Session, folder_id: str):
    return db.query(Folder).filter(Folder.id == folder_id).first()


def get_folders(db: Session, org_id: str):
    return db.query(Folder).filter(Folder.organization_id == org_id).all()


def create_folder(db: Session, folder: FolderCreate):
    db.add(folder)
    db.commit()
    db.refresh(folder)
    return folder


#
