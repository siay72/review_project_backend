from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.auth import SECRET_KEY, ALGORITHM
from app.database import get_db
from app import models

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        user_id = int(payload.get("sub"))

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    return user


def get_current_admin(
    current_user=Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Admin access required",
        )

    return current_user