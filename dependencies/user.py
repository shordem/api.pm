from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import JWTError

from services.user import get_user
from utilities.jwt import verify_token
from schemas.user import User
from schemas.authentication import TokenData
from dependencies.db import get_db

bearer_scheme = HTTPBearer()


async def get_current_user(
    token: Annotated[str, Depends(bearer_scheme)], db=Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        payload = verify_token(token.credentials)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    except Exception as e:
        print(e)
        raise credentials_exception

    user = get_user(db=db, user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_verified_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.is_email_verified is False:
        raise HTTPException(status_code=400, detail="Email not verified")
    return current_user
