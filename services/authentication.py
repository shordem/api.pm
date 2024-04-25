from datetime import timedelta
from sqlalchemy.orm import Session

from models.user import User
from schemas.authentication import LoginData, Token, VerifyEmail
from schemas.user import UserCreate
from utilities.authentication import hash_password, verify_password
from utilities.jwt import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token


def register(db: Session, user: UserCreate):
    if db.query(User).filter(User.email == user.email).first():
        raise Exception("Email already exists")
    if db.query(User).filter(User.username == user.username).first():
        raise Exception("Username already exists")

    user = User(**user.model_dump())
    user.password = hash_password(user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def verify_email(db: Session, user_email: VerifyEmail):
    user = db.query(User).filter(User.email == user_email.email).first()
    user.is_email_verified = True
    db.commit()
    db.refresh(user)
    return user


def login(db: Session, login: LoginData):

    try:
        user = db.query(User).filter(User.username == login.username).first()

        if user is None:
            return 404
        if not verify_password(login.password, user.password):
            return 400
        if not user.is_email_verified:
            return 401

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token)
    except Exception as e:
        # print(e)
        raise e
