from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_current_user

from app.database import get_db
from app import models, schemas
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
)

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=schemas.UserResponse,
)
def register(
    user: schemas.RegisterUser,
    db: Session = Depends(get_db),
):
    existing = (
        db.query(models.User)
        .filter(models.User.email == user.email)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),
        is_admin=False,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.post(
    "/login",
    response_model=schemas.TokenResponse,
)
def login(
    user: schemas.LoginUser,
    db: Session = Depends(get_db),
):
    db_user = (
        db.query(models.User)
        .filter(models.User.email == user.email)
        .first()
    )

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(
        user.password,
        db_user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(
        {
            "sub": str(db_user.id),
            "email": db_user.email,
            "is_admin": db_user.is_admin,
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": db_user,
    }

@router.get(
    "/me",
    response_model=schemas.UserResponse,
)
def get_me(
    current_user=Depends(get_current_user),
):
    return current_user