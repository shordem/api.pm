from sqlalchemy.orm import Session

from models.folder import Folder
from models.todo import Todo
from models.note import Note
from schemas.folder import FolderCreate, FolderUpdate


def get_folder(db: Session, folder_id: str):
    return db.query(Folder).filter(Folder.id == folder_id).first()


def get_folders(db: Session, org_id: str):
    return db.query(Folder).filter(Folder.organization_id == org_id).all()


def create_folder(db: Session, folder_create: FolderCreate, org_id: str):
    folder = Folder(name=folder_create.name, organization_id=org_id)
    db.add(folder)
    db.commit()
    db.refresh(folder)
    return folder


def update_folder(db: Session, folder: FolderUpdate):
    db.add(folder)
    db.commit()
    db.refresh(folder)
    return folder


def delete_folder(db: Session, folder_id: str):
    folder = db.query(Folder).filter(Folder.id == folder_id).first()
    if folder.is_default:
        raise Exception("Default folder cannot be deleted")

    # move all todos and notes to default folder
    default_org_folder = (
        db.query(Folder)
        .filter(
            Folder.organization_id == folder.organization_id, Folder.is_default == True
        )
        .first()
    )

    db.query(Todo).filter(Todo.folder_id == folder_id).update(
        {Todo.folder_id: default_org_folder.id}
    )
    db.query(Note).filter(Note.folder_id == folder_id).update(
        {Note.folder_id: default_org_folder.id}
    )

    db.delete(folder)
    db.commit()
