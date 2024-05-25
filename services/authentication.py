from datetime import timedelta

from fastapi import BackgroundTasks
from sqlalchemy.orm import Session

from config.email import send_email
from models.user import User
from schemas.authentication import LoginData, Token, VerifyEmail
from schemas.email import EmailSchema
from schemas.organization import OrganizationCreate
from schemas.user import UserCreate
from services.code import create_code, get_code_by_user_id_and_code
from services.organization import create_organization
from services.user import get_user_by_email
from utilities.authentication import hash_password, verify_password
from utilities.generate_code import generate_code
from utilities.jwt import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token


async def register(db: Session, user: UserCreate, background_tasks: BackgroundTasks):
    try:
        if db.query(User).filter(User.email == user.email).first():
            raise Exception("Email already exists")
        if db.query(User).filter(User.username == user.username).first():
            raise Exception("Username already exists")

        user = User(**user.model_dump())
        user.email = user.email.lower()
        user.password = hash_password(user.password)
        db.add(user)
        db.commit()

        org = OrganizationCreate(name="Personal", owner_id=str(user.id))

        create_organization(db, org)

        code = generate_code()
        create_code(db, code, str(user.id))

        email = EmailSchema(
            to=user.email,
            subject="Verify Your Email",
            template="verify-email.html",
            variables={"fullname": f"{user.first_name} {user.last_name}", "code": code},
        )

        background_tasks.add_task(send_email, email)

        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise e


def verify_email(db: Session, verify_email: VerifyEmail):
    user = get_user_by_email(db, verify_email.email)
    code = get_code_by_user_id_and_code(
        db=db, user_id=str(user.id), code=verify_email.code
    )

    user.is_email_verified = True

    db.delete(code)
    db.commit()


def login(db: Session, login: LoginData):

    try:
        user = db.query(User).filter(User.email == login.email.lower()).first()

        if user is None:
            return 404
        if not verify_password(login.password, user.password):
            return 400
        if not user.is_email_verified:
            return 401

        access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token)
    except Exception as e:
        # print(e)
        raise e
