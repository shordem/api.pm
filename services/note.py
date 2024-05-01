from sqlalchemy.orm import Session

from models.note import Note
from schemas.note import NoteCreate, NoteUpdate, NoteSchema
from services.folder import get_folder


def get_note(db: Session, note_id: str):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise Exception("Note not found")

    note_schema = NoteSchema.model_validate(note)
    return note_schema


def get_notes(db: Session, folder_id: str):
    notes = db.query(Note).filter(Note.folder_id == folder_id).all()
    notes_schema = []
    for note in notes:
        notes_schema.append(NoteSchema.model_validate(note))
    return notes_schema


def create_note(db: Session, note: NoteCreate):
    get_folder(db, note.folder_id)

    note = Note(**note.model_dump())
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def update_note(db: Session, note: NoteUpdate):
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def delete_note(db: Session, note_id: str):
    note = db.query(Note).filter(Note.id == note_id).first()
    db.delete(note)
    db.commit()
    return note
