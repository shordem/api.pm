from sqlalchemy.orm import Session

from models.user import User
from models.code import Code


def create_code(db: Session, code: str, user_id: str):
    new_code = Code(code=code, user_id=user_id)
    db.add(new_code)
    db.commit()
    db.refresh(new_code)
    return new_code


def get_code_by_user_id_and_code(db: Session, user_id: str, code: str):
    code = db.query(Code).filter(Code.user_id == user_id, Code.code == code).first()
    if not code:
        raise Exception("Code not found")
    return code
