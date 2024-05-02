from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import JWTError

from services.user import get_user
from utilities.jwt import verify_token
from schemas.user import UserSchema
from schemas.authentication import TokenData
from dependencies.db import get_db

bearer_scheme = HTTPBearer()


async def get_current_user(
    token: Annotated[str, Depends(bearer_scheme)], db=Depends(get_db)
):

    try:
        payload = verify_token(token.credentials)

        if not isinstance(payload, dict):
            raise HTTPException(status_code=400, detail="Invalid token")

        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=400, detail="Invalid token")
        token_data = TokenData(user_id=user_id)
    except JWTError as e:
        raise HTTPException(status_code=400, detail="Invalid token")

    user = get_user(db=db, user_id=token_data.user_id)

    return user


async def get_current_verified_user(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
):
    if current_user.is_email_verified is False:
        raise HTTPException(status_code=400, detail="Email not verified")
    return UserSchema.model_validate(current_user)
