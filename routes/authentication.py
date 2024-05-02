from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from services import authentication as authentication_svc
from schemas.authentication import LoginData, VerifyEmail
from schemas.user import UserCreate
from dependencies.db import get_db

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register")
async def register(
    user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    try:
        await authentication_svc.register(db, user, background_tasks)
        return {"message": "User registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(login: LoginData, db: Session = Depends(get_db)):

    try:
        token = authentication_svc.login(db, login)

        if token == 404:
            raise HTTPException(status_code=404, detail="User not found")
        elif token == 400:
            raise HTTPException(status_code=400, detail="Incorrect password")
        elif token == 401:
            raise HTTPException(status_code=401, detail="Email not verified")

        return token
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/verify-email")
def verify_email(user_email: VerifyEmail, db: Session = Depends(get_db)):

    try:
        authentication_svc.verify_email(db, user_email)
        return {"message": "Email verified successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
