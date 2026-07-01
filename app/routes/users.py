from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas
from app.dependencies import get_current_admin

router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)


@router.post(
    "/",
    response_model=schemas.UserResponse
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    return crud.create_user(db, user)


@router.get("/")
def get_users(
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    return crud.get_users(db)


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    deleted = crud.delete_user(db, user_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return deleted