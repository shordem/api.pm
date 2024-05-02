from sqlalchemy.orm import Session

from models.note import Note
from models.user import User
from schemas.note import NoteCreate, NoteUpdate, NoteSchema
from schemas.user import UserSchema
from .folder import get_folder
from .user import get_user


def get_note(db: Session, note_id: str):
    result = db.query(Note).filter(Note.id == note_id).first()
    if not result:
        raise Exception("Note not found")

    user_data = get_user(db, result.created_by)
    data = NoteSchema(
        created_by=user_data,
        title=result.title,
        content=result.content,
        id=result.id,
    )

    return data


def get_notes(db: Session, folder_id: str):
    notes = (
        db.query(Note, User)
        .join(User, User.id == Note.created_by)
        .filter(Note.folder_id == folder_id)
        .all()
    )

    result = []
    for note, user in notes:
        user_data = UserSchema.model_validate(user)
        data = NoteSchema(
            created_by=user_data, title=note.title, content=note.content, id=note.id
        )

        result.append(data)
    return result


def create_note(db: Session, folder_id: str, user_id: str, note: NoteCreate):
    get_folder(db, folder_id)

    note = Note(
        title=note.title,
        content=note.content,
        folder_id=folder_id,
        created_by=user_id,
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def update_note(db: Session, note_id: str, note: NoteUpdate):
    result = db.query(Note).filter(Note.id == note_id).first()
    if not result:
        raise Exception("Note not found")

    result.title = note.title
    result.content = note.content

    db.commit()
    return note


def delete_note(db: Session, note_id: str):
    note = db.query(Note).filter(Note.id == note_id).first()
    db.delete(note)
    db.commit()
    return note
