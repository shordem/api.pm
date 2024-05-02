from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated

from dependencies.user import get_current_verified_user
from schemas.user import UserSchema

router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.get("")
def get_user(user: Annotated[UserSchema, Depends(get_current_verified_user)]):
    try:
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
