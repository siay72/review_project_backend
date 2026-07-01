from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models

from app.database import get_db
from app import crud, schemas
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/api/reviews",
    tags=["Reviews"]
)

@router.get("/")
def get_reviews(
    db: Session = Depends(get_db),
):
    return crud.get_reviews(db)


@router.post("/")
def create_review(
    review: schemas.ReviewWithUserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.create_review(db, review, current_user)

@router.put("/{review_id}")
def update_review(
    review_id: int,
    review: schemas.ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.update_review(
        db,
        review_id,
        review,
        current_user.id,
    )


@router.delete("/{review_id}")
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    deleted = crud.delete_review(
        db,
        review_id,
        current_user.id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    return deleted